"""Regression tests for the Remnawave 3.0 contract.

Each test pins something the 2.8 → 3.0 migration changed. They run offline —
no panel required.
"""
import ast
import collections
import pathlib
import re
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import pytest

import remnawave.models as models
from remnawave import RemnawaveSDK
from remnawave.models import (
    BulkDeleteUsersBodyDto,
    DropByUserIds,
    DropConnectionsBodyDto,
    ExtendUserBodyDto,
    GetApiTokensResponseDto,
    GetNodeSecretKeyResponseDto,
    ResolveUserRequestBodyDto,
    SubscriptionSettingsResponseDto,
    UpdateExternalSquadBodyDto,
    UserResponseDto,
)
from remnawave.rapid.client import BaseController

REPO = pathlib.Path(__file__).resolve().parent.parent


def _dump(model):
    """Serialize the way remnawave.rapid.client serializes request bodies."""
    return model.model_dump(exclude_unset=True, by_alias=True, mode="json")


# --------------------------------------------------------------------------- #
# Users are identified by a numeric id; uuid is gone
# --------------------------------------------------------------------------- #

class TestUserIdentity:
    def test_user_model_has_no_uuid(self):
        assert "uuid" not in UserResponseDto.model_fields
        assert UserResponseDto.model_fields["id"].annotation is int

    def test_resolve_accepts_only_id_short_uuid_username(self):
        assert set(ResolveUserRequestBodyDto.model_fields) == {"id", "short_uuid", "username"}

    def test_bulk_bodies_use_user_ids(self):
        body = _dump(BulkDeleteUsersBodyDto(user_ids=[1, 2, 3]))
        assert body == {"userIds": [1, 2, 3]}

    def test_user_path_params_are_ints(self):
        """Every {userId} path param must be typed int, never str/UUID."""
        offenders = []
        for py in sorted((REPO / "remnawave" / "controllers").glob("*.py")):
            tree = ast.parse(py.read_text(encoding="utf-8"))
            for fn in [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]:
                paths = [
                    d.args[0].value
                    for d in fn.decorator_list
                    if isinstance(d, ast.Call) and d.args and isinstance(d.args[0], ast.Constant)
                ]
                if not any("{userId}" in p for p in paths):
                    continue
                for arg in fn.args.args:
                    if arg.annotation is None:
                        continue
                    src = ast.unparse(arg.annotation)
                    if "userId" in src and "int" not in src:
                        offenders.append(f"{py.name}:{fn.lineno} {fn.name}")
        assert offenders == []


# --------------------------------------------------------------------------- #
# 202 / 204: no response body
# --------------------------------------------------------------------------- #

class TestEmptyBodyResponses:
    @pytest.mark.parametrize("status", [202, 204])
    def test_transport_returns_none(self, status):
        controller = BaseController.__new__(BaseController)
        request = httpx.Request("DELETE", "https://panel.example.com/api/users/1")
        response = httpx.Response(status, request=request)
        assert controller._handle_response(response, UserResponseDto) is None

    def test_response_class_none_returns_none(self):
        controller = BaseController.__new__(BaseController)
        request = httpx.Request("POST", "https://panel.example.com/api/users/bulk/update")
        response = httpx.Response(200, json={"response": {}}, request=request)
        assert controller._handle_response(response, None) is None

    def test_delete_endpoints_declare_no_response_class(self):
        """Every @delete must be response_class=None — all DELETEs are 204 in 3.0."""
        offenders = []
        for py in sorted((REPO / "remnawave" / "controllers").glob("*.py")):
            src = py.read_text(encoding="utf-8")
            for m in re.finditer(r"@delete\(\s*([^)]*)\)", src, re.S):
                if "response_class=None" not in m.group(1):
                    offenders.append(f"{py.name}: {m.group(1).strip()[:70]}")
        assert offenders == []


# --------------------------------------------------------------------------- #
# /api/ip-control → /api/connections
# --------------------------------------------------------------------------- #

class TestConnectionsModule:
    def test_sdk_exposes_connections(self):
        sdk = RemnawaveSDK(base_url="https://panel.example.com", token="t")
        assert hasattr(sdk, "connections")
        assert not hasattr(sdk, "ip_control")

    def test_old_module_is_gone(self):
        assert not (REPO / "remnawave" / "controllers" / "ip_control.py").exists()
        assert not (REPO / "remnawave" / "models" / "ip_control.py").exists()

    def test_drop_body_uses_user_ids(self):
        from remnawave.models import TargetAllNodes

        body = _dump(
            DropConnectionsBodyDto(
                drop_by=DropByUserIds(user_ids=[7]),
                target_nodes=TargetAllNodes(),
            )
        )
        assert body["dropBy"]["userIds"] == [7]
        # дискриминаторы обязаны уходить даже при значении по умолчанию
        assert body["dropBy"]["by"] == "userIds"
        assert body["targetNodes"]["target"] == "allNodes"


# --------------------------------------------------------------------------- #
# Renamed / removed fields
# --------------------------------------------------------------------------- #

class TestRenamedFields:
    def test_keygen_returns_secret_key(self):
        dto = GetNodeSecretKeyResponseDto.model_validate({"secretKey": "s3cr3t"})
        assert dto.secret_key == "s3cr3t"
        assert "pub_key" not in GetNodeSecretKeyResponseDto.model_fields

    def test_tokens_response_has_no_docs(self):
        assert set(GetApiTokensResponseDto.model_fields) == {"tokens"}

    def test_subscription_settings_dropped_header_fields(self):
        for gone in (
            "profile_title",
            "profile_update_interval",
            "support_link",
            "is_profile_webpage_url_enabled",
            "happ_announce",
            "happ_routing",
        ):
            assert gone not in SubscriptionSettingsResponseDto.model_fields, gone

    def test_external_squad_response_headers_split(self):
        fields = UpdateExternalSquadBodyDto.model_fields
        assert "response_headers_add" in fields
        assert "response_headers_remove" in fields
        assert "response_headers" not in fields

    def test_extend_user_body(self):
        assert _dump(ExtendUserBodyDto(days=7)) == {"days": 7}


# --------------------------------------------------------------------------- #
# Package surface
# --------------------------------------------------------------------------- #

class TestScopesAndErrorCodes:
    def test_scope_enum_matches_the_grantable_catalog(self):
        """Set equality against the catalog the panel actually accepts.

        The grantable catalog is built by `ScopeCatalogService` from controllers decorated
        with `@ApiScopeResource` only — `auth`, `passkeys`, `api-tokens`, `remnawave-settings`
        and the public `subscription` controller are NOT in it, so inventing scopes for them
        makes `POST /api/tokens` fail. The fixture is derived from the 3.0 contract.
        """
        import json

        from remnawave.enums import Scope

        fixture = json.loads(
            (pathlib.Path(__file__).parent / "fixtures" / "scopes_3.0.json").read_text(
                encoding="utf-8"
            )
        )
        expected = set(fixture["scopes"])
        actual = {s.value for s in Scope}
        assert actual - expected == set(), f"scopes the panel would reject: {sorted(actual - expected)}"
        assert expected - actual == set(), f"scopes missing from the enum: {sorted(expected - actual)}"

    def test_connections_scopes_replaced_ip_control(self):
        from remnawave.enums import Scope

        values = {s.value for s in Scope}
        assert "connections:*" in values
        assert not any(v.startswith("ip-control:") for v in values)

    def test_error_codes_have_status_and_message(self):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES

        for member in ErrorCode:
            assert member.value in ERROR_HTTP_CODES
            assert member.value in ERROR_MESSAGES

    def test_new_3_0_error_codes(self):
        from remnawave.enums import ErrorCode

        for name in (
            "GET_STATS_DIGEST_ERROR",
            "GET_INTERNAL_SQUAD_USAGE_ERROR",
            "ADD_MANY_USERS_TO_INTERNAL_SQUAD_ERROR",
            "REMOVE_MANY_USERS_FROM_INTERNAL_SQUAD_ERROR",
        ):
            assert hasattr(ErrorCode, name), name
        # 3.0 исправил опечатку REMNAAWAVE -> REMNAWAVE
        assert hasattr(ErrorCode, "GET_REMNAWAVE_SETTINGS_ERROR")
        assert not hasattr(ErrorCode, "GET_REMNAAWAVE_SETTINGS_ERROR")


class TestPackageSurface:
    def test_all_exports_resolve(self):
        assert [n for n in models.__all__ if not hasattr(models, n)] == []

    def test_no_duplicate_exports(self):
        assert [n for n, c in collections.Counter(models.__all__).items() if c > 1] == []

    def test_webhook_models_do_not_shadow_rest_models(self):
        assert models.InternalSquadDto.__module__ == "remnawave.models.internal_squads"
        assert models.InfraProviderDto.__module__ == "remnawave.models.infra_billing"
        assert models.UserTrafficDto.__module__ == "remnawave.models.users"

    def test_legacy_request_dto_aliases_still_import(self):
        """Renaming *RequestDto -> *BodyDto kept backwards-compatible aliases."""
        from remnawave.models.users import CreateUserBodyDto

        assert getattr(models, "CreateUserRequestDto", CreateUserBodyDto) is CreateUserBodyDto
