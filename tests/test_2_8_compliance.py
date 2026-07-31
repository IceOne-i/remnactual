"""Regression tests for the Remnawave 2.8 contract.

Each test pins a divergence that was found when auditing the SDK against
`@remnawave/backend-contract` 2.8.35 (backend tag 2.8.1). They run offline —
no panel required.
"""
import collections
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

import remnawave.models as models
from remnawave.enums import ErrorCode
from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES
from remnawave.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    ServerError,
    UnauthorizedError,
)
from remnawave.exceptions.handler import ERRORS as ERROR_EXCEPTIONS
from remnawave.models import (
    BulkAllUpdateUsersRequestDto,
    ConvertedUserInfo,
    CreateInfraBillingNodeRequestDto,
    CreateInternalSquadRequestDto,
    DeleteApiTokenResponseDto,
    DropByIpAddresses,
    DropByUserUuids,
    DropConnectionsRequestDto,
    GetSubpageConfigByShortUuidRequestBodyDto,
    ResolveUserRequestBodyDto,
    RevokeUserRequestDto,
    TargetAllNodes,
    TargetSpecificNodes,
    UpdateHostRequestDto,
    GetHwidStatisticsResponseDto,
    GetUserAccessibleNodesResponseDto,
    HwidDeviceDto,
    InfraBillingHistoryDto,
    InfraBillingNodeDto,
    RestartNodeRequestBodyDto,
    SubscriptionRequestHistoryRecord,
    UpdateInternalSquadRequestDto,
    UpdateUserRequestDto,
    WebhookPayloadDto,
)


def _dump(model):
    """Serialize the way remnawave.rapid.client serializes request bodies."""
    return model.model_dump(exclude_unset=True, by_alias=True, mode="json")


# --------------------------------------------------------------------------- #
# userUuid -> userId (number)
# --------------------------------------------------------------------------- #

class TestUserIdRename:
    def test_hwid_device_uses_user_id_and_request_ip(self):
        device = HwidDeviceDto.model_validate(
            {
                "hwid": "h1",
                "userId": 42,
                "platform": None,
                "osVersion": None,
                "deviceModel": None,
                "userAgent": None,
                "requestIp": "10.0.0.1",
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
            }
        )
        assert device.user_id == 42
        assert device.request_ip == "10.0.0.1"
        assert not hasattr(device, "user_uuid")

    def test_subscription_request_history_uses_user_id(self):
        record = SubscriptionRequestHistoryRecord.model_validate(
            {
                "id": 1,
                "userId": 7,
                "requestIp": None,
                "userAgent": None,
                "requestAt": "2026-01-01T00:00:00Z",
            }
        )
        assert record.user_id == 7


# --------------------------------------------------------------------------- #
# HWID stats: byApp moved inside byPlatform
# --------------------------------------------------------------------------- #

class TestHwidStats:
    PAYLOAD = {
        "byPlatform": [
            {"platform": "ios", "count": 3, "byApp": [{"app": "happ", "count": 2}]},
            {"platform": "android", "count": 1, "byApp": [{"app": "happ", "count": 1}]},
        ],
        "stats": {
            "totalUniqueDevices": 4,
            "totalHwidDevices": 4,
            "averageHwidDevicesPerUser": 1.0,
        },
    }

    def test_parses_nested_by_app(self):
        stats = GetHwidStatisticsResponseDto.model_validate(self.PAYLOAD)
        assert stats.by_platform[0].by_app[0].app == "happ"

    def test_top_level_by_app_is_aggregated(self):
        stats = GetHwidStatisticsResponseDto.model_validate(self.PAYLOAD)
        assert [(i.app, i.count) for i in stats.by_app] == [("happ", 3)]


# --------------------------------------------------------------------------- #
# Subscriptions: hwidCheckup replaced isHwidLimited
# --------------------------------------------------------------------------- #

class TestHwidCheckup:
    def test_parses_hwid_checkup(self):
        info = ConvertedUserInfo.model_validate(
            {
                "daysLeft": 5,
                "trafficLimit": "10 GB",
                "trafficUsed": "1 GB",
                "lifetimeTrafficUsed": "3 GB",
                "hwidCheckup": {
                    "subscriptionAllowed": False,
                    "maxDeviceReached": True,
                    "hwidNotSupported": False,
                    "limitBypassed": False,
                },
            }
        )
        assert info.hwid_checkup.max_device_reached is True
        assert info.is_hwid_limited is True

    def test_null_hwid_checkup(self):
        info = ConvertedUserInfo.model_validate(
            {
                "daysLeft": 5,
                "trafficLimit": "10 GB",
                "trafficUsed": "1 GB",
                "lifetimeTrafficUsed": "3 GB",
                "hwidCheckup": None,
            }
        )
        assert info.hwid_checkup is None
        assert info.is_hwid_limited is False


# --------------------------------------------------------------------------- #
# Infra billing: custom billing nodes
# --------------------------------------------------------------------------- #

class TestInfraBilling:
    def test_billing_node_allows_null_node(self):
        node = InfraBillingNodeDto.model_validate(
            {
                "uuid": str(uuid4()),
                "nodeUuid": None,
                "name": "Custom line",
                "providerUuid": str(uuid4()),
                "provider": {
                    "uuid": str(uuid4()),
                    "name": "Hetzner",
                    "loginUrl": None,
                    "faviconLink": None,
                },
                "node": None,
                "nextBillingAt": "2026-02-01T00:00:00Z",
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
            }
        )
        assert node.node_uuid is None and node.node is None

    def test_history_record_uses_billed_at_and_provider(self):
        record = InfraBillingHistoryDto.model_validate(
            {
                "uuid": str(uuid4()),
                "providerUuid": str(uuid4()),
                "amount": 12.5,
                "billedAt": "2026-01-15T00:00:00Z",
                "provider": {"uuid": str(uuid4()), "name": "Hetzner", "faviconLink": None},
            }
        )
        assert record.billed_at.year == 2026
        assert not hasattr(record, "payment_date")

    def test_nullable_keys_always_sent(self):
        body = _dump(
            CreateInfraBillingNodeRequestDto(
                provider_uuid=uuid4(),
                name="Custom line",
                next_billing_at=datetime.now(tz=timezone.utc),
            )
        )
        assert body["nodeUuid"] is None
        assert body["name"] == "Custom line"


# --------------------------------------------------------------------------- #
# Request serialization: exclude_unset semantics
# --------------------------------------------------------------------------- #

class TestRequestSerialization:
    def test_explicit_null_is_sent(self):
        body = _dump(UpdateUserRequestDto(uuid=uuid4(), telegram_id=None))
        assert body["telegramId"] is None

    def test_untouched_fields_are_omitted(self):
        body = _dump(UpdateUserRequestDto(uuid=uuid4()))
        assert set(body) == {"uuid"}

    def test_bulk_all_update_has_no_implicit_status(self):
        assert "status" not in _dump(BulkAllUpdateUsersRequestDto(traffic_limit_bytes=100.0))

    def test_squad_update_does_not_wipe_inbounds(self):
        assert "inbounds" not in _dump(UpdateInternalSquadRequestDto(uuid=uuid4(), name="squad"))

    def test_force_restart_always_present(self):
        assert _dump(RestartNodeRequestBodyDto())["forceRestart"] is False
        assert _dump(RestartNodeRequestBodyDto(force_restart=True))["forceRestart"] is True

    def test_drop_connections_discriminators_always_present(self):
        body = _dump(
            DropConnectionsRequestDto(
                drop_by=DropByUserUuids(user_uuids=[uuid4()]),
                target_nodes=TargetAllNodes(),
            )
        )
        assert body["dropBy"]["by"] == "userUuids"
        assert body["targetNodes"]["target"] == "allNodes"

        body = _dump(
            DropConnectionsRequestDto(
                drop_by=DropByIpAddresses(ip_addresses=["1.2.3.4"]),
                target_nodes=TargetSpecificNodes(node_uuids=[uuid4()]),
            )
        )
        assert body["dropBy"]["by"] == "ipAddresses"
        assert body["targetNodes"]["target"] == "specificNodes"

    def test_create_squad_always_sends_inbounds(self):
        assert _dump(CreateInternalSquadRequestDto(name="My Squad"))["inbounds"] == []

    def test_subpage_body_always_sends_request_headers(self):
        assert _dump(GetSubpageConfigByShortUuidRequestBodyDto())["requestHeaders"] == {}

    def test_legacy_tag_none_does_not_emit_null_tags(self):
        assert "tags" not in _dump(UpdateHostRequestDto(uuid=uuid4(), tag=None))
        assert _dump(UpdateHostRequestDto(uuid=uuid4(), tag="EU"))["tags"] == ["EU"]

    def test_branding_settings_always_sends_both_nullable_keys(self):
        from remnawave.models import RemnawaveBrandingSettings

        body = _dump(RemnawaveBrandingSettings(title="Panel"))
        assert body == {"title": "Panel", "logoUrl": None}


class TestRequestValidation:
    def test_resolve_requires_exactly_one_identifier(self):
        with pytest.raises(ValidationError):
            ResolveUserRequestBodyDto()
        with pytest.raises(ValidationError):
            ResolveUserRequestBodyDto(uuid=uuid4(), username="u")
        assert ResolveUserRequestBodyDto(username="u").username == "u"

    def test_update_user_requires_uuid_or_username(self):
        with pytest.raises(ValidationError):
            UpdateUserRequestDto(description="x")
        assert UpdateUserRequestDto(username="u").username == "u"

    def test_update_user_status_limited_to_active_disabled(self):
        with pytest.raises(ValidationError):
            UpdateUserRequestDto(uuid=uuid4(), status="LIMITED")
        assert _dump(UpdateUserRequestDto(uuid=uuid4(), status="DISABLED"))["status"] == "DISABLED"

    def test_revoke_short_uuid_has_no_charset_restriction(self):
        dto = RevokeUserRequestDto(short_uuid="ab.cd-EF")
        assert dto.short_uuid == "ab.cd-EF"


# --------------------------------------------------------------------------- #
# Renamed response fields
# --------------------------------------------------------------------------- #

class TestRenamedResponseFields:
    def test_accessible_nodes_uses_active_nodes_and_node_name(self):
        resp = GetUserAccessibleNodesResponseDto.model_validate(
            {
                "userUuid": str(uuid4()),
                "activeNodes": [
                    {
                        "uuid": str(uuid4()),
                        "nodeName": "de-1",
                        "countryCode": "DE",
                        "configProfileUuid": str(uuid4()),
                        "configProfileName": "default",
                        "activeSquads": [],
                    }
                ],
            }
        )
        assert len(resp.active_nodes) == 1
        assert resp.active_nodes[0].name == "de-1"
        assert resp.nodes == resp.active_nodes

    def test_delete_api_token_accepts_bare_boolean(self):
        assert DeleteApiTokenResponseDto.model_validate(True).is_deleted is True
        assert DeleteApiTokenResponseDto.model_validate({"isDeleted": False}).is_deleted is False


# --------------------------------------------------------------------------- #
# Error codes
# --------------------------------------------------------------------------- #

class TestErrorCodes:
    def test_every_code_has_http_code_and_message(self):
        for member in ErrorCode:
            assert member.value in ERROR_HTTP_CODES
            assert member.value in ERROR_MESSAGES

    @pytest.mark.parametrize(
        "code,expected",
        [
            (ErrorCode.INTERNAL_SERVER_ERROR, ServerError),  # 500
            (ErrorCode.UNAUTHORIZED, UnauthorizedError),  # 401
            (ErrorCode.FORBIDDEN_ROLE_ERROR, ForbiddenError),  # 403
            (ErrorCode.NODE_NOT_FOUND, NotFoundError),  # 404
            # 400, а не 409 — так объявлено в контракте
            (ErrorCode.USER_USERNAME_ALREADY_EXISTS, BadRequestError),
            (ErrorCode.INTERNAL_SQUAD_NAME_ALREADY_EXISTS, ConflictError),  # 409
        ],
    )
    def test_exception_class_matches_contract_http_code(self, code, expected):
        assert ERROR_EXCEPTIONS[code] is expected

    def test_exception_class_is_consistent_with_http_code(self):
        by_http = {400, 401, 403, 404, 409, 500}
        for code, http in ERROR_HTTP_CODES.items():
            assert http in by_http, f"{code} has unexpected httpCode {http}"

    def test_ambiguous_code_follows_actual_http_status(self):
        """Контракт переиспользует A089 для 500 и 400 — решает реальный статус."""
        from remnawave.exceptions.handler import _resolve_exception

        assert _resolve_exception("A089", 500) is ServerError
        assert _resolve_exception("A089", 400) is BadRequestError
        assert _resolve_exception("A219", 404) is NotFoundError
        assert _resolve_exception("A219", 500) is ServerError
        assert _resolve_exception("UNKNOWN_CODE", 404) is NotFoundError

    def test_handle_api_error_raises_for_every_non_2xx(self):
        import httpx

        from remnawave.exceptions import ApiError
        from remnawave.exceptions.handler import handle_api_error

        request = httpx.Request("GET", "https://panel.example.com/api/users")
        for status in (302, 400, 404, 500):
            response = httpx.Response(status, json={"message": "x"}, request=request)
            with pytest.raises(ApiError):
                handle_api_error(response)

        ok = httpx.Response(200, json={"response": {}}, request=request)
        assert handle_api_error(ok) is None


# --------------------------------------------------------------------------- #
# Webhooks
# --------------------------------------------------------------------------- #

USER_PAYLOAD = {
    "uuid": str(uuid4()),
    "id": 1,
    "shortUuid": "abc",
    "username": "u",
    "status": "ACTIVE",
    "expireAt": "2026-08-01T00:00:00Z",
    "trafficLimitBytes": 0,
    "trafficLimitStrategy": "NO_RESET",
    "lastTriggeredThreshold": 0,
    "trojanPassword": "x",
    "vlessUuid": str(uuid4()),
    "ssPassword": "y",
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z",
    "subscriptionUrl": "https://example.com/s",
    "activeInternalSquads": [],
    "userTraffic": {"usedTrafficBytes": 0, "lifetimeUsedTrafficBytes": 0},
}


class TestWebhooks:
    def test_user_expiration_carries_scope_and_meta(self):
        payload = WebhookPayloadDto.from_dict(
            {
                "scope": "user",
                "event": "user.expiration",
                "timestamp": "2026-07-31T10:00:00Z",
                "meta": {"expiration": -24},
                "data": USER_PAYLOAD,
            }
        )
        assert payload.scope == "user"
        assert payload.meta.expiration == -24

    def test_errors_event_parses(self):
        payload = WebhookPayloadDto.from_dict(
            {
                "scope": "errors",
                "event": "errors.bandwidth_usage_threshold_reached_max_notifications",
                "timestamp": "2026-07-31T10:00:00Z",
                "data": {"description": "boom"},
            }
        )
        assert payload.data.description == "boom"

    def test_hwid_event_exposes_user_id(self):
        from remnawave.controllers.webhooks import WebhookUtility

        payload = WebhookPayloadDto.from_dict(
            {
                "scope": "user_hwid_devices",
                "event": "user_hwid_devices.added",
                "timestamp": "2026-07-31T10:00:00Z",
                "data": {
                    "user": USER_PAYLOAD,
                    "hwidUserDevice": {
                        "hwid": "h1",
                        "userId": 42,
                        "platform": None,
                        "osVersion": None,
                        "deviceModel": None,
                        "userAgent": None,
                        "requestIp": "1.2.3.4",
                        "createdAt": "2026-01-01T00:00:00Z",
                        "updatedAt": "2026-01-01T00:00:00Z",
                    },
                },
            }
        )
        _, device = WebhookUtility.extract_user_hwid_event_data(payload)
        assert device.user_id == 42

    def test_service_event_without_login_attempt_falls_back_to_dict(self):
        payload = WebhookPayloadDto.from_dict(
            {
                "scope": "service",
                "event": "service.login_attempt_success",
                "timestamp": "2026-07-31T10:00:00Z",
                "data": {},
            }
        )
        assert payload.data == {}

    def test_api_token_service_event_parses(self):
        payload = WebhookPayloadDto.from_dict(
            {
                "scope": "service",
                "event": "service.api_token_created",
                "timestamp": "2026-07-31T10:00:00Z",
                "data": {"apiToken": {"name": "ci", "uuid": str(uuid4()), "scopes": ["*"]}},
            }
        )
        assert payload.data["apiToken"]["name"] == "ci"

    def test_signature_uses_raw_body_verbatim(self):
        import hashlib
        import hmac

        from remnawave.controllers.webhooks import WebhookUtility

        secret = "s3cr3t"
        raw = b'{"event":"user.created","data":{"name":"\xd0\xb0\xd0\xb1\xd0\xb2"}}'
        signature = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
        assert WebhookUtility.validate_webhook(raw, signature, secret) is True


# --------------------------------------------------------------------------- #
# Package surface
# --------------------------------------------------------------------------- #

class TestPackageSurface:
    def test_all_exports_resolve(self):
        missing = [name for name in models.__all__ if not hasattr(models, name)]
        assert missing == []

    def test_no_duplicate_exports(self):
        dupes = [n for n, c in collections.Counter(models.__all__).items() if c > 1]
        assert dupes == []

    def test_webhook_models_do_not_shadow_rest_models(self):
        assert models.InternalSquadDto.__module__ == "remnawave.models.internal_squads"
        assert models.InfraProviderDto.__module__ == "remnawave.models.infra_billing"
        assert models.UserTrafficDto.__module__ == "remnawave.models.users"
        assert models.GetMetadataResponseDto.__module__ == "remnawave.models.system"

    def test_removed_controllers_are_gone(self):
        from remnawave import RemnawaveSDK

        for attr in ("xray_config", "inbounds_bulk_actions"):
            assert not hasattr(RemnawaveSDK, attr)

    def test_removed_endpoints_are_gone(self):
        from remnawave.controllers.bandwidthstats import BandWidthStatsController
        from remnawave.controllers.auth import AuthController
        from remnawave.controllers.nodes import NodesController
        from remnawave.controllers.subscription import SubscriptionController

        assert not hasattr(NodesController, "reset_traffic_all_nodes")
        assert not hasattr(AuthController, "oauth2_tg_callback")
        assert not hasattr(SubscriptionController, "get_subscription_with_type")
        assert not hasattr(BandWidthStatsController, "get_nodes_realtime_usage")


# --------------------------------------------------------------------------- #
# Enums
# --------------------------------------------------------------------------- #

class TestEnums:
    def test_no_singbox_legacy(self):
        from remnawave.enums import ClientType, TemplateType

        assert not hasattr(TemplateType, "SINGBOX_LEGACY")
        assert not hasattr(ClientType, "SINGBOX_LEGACY")

    def test_client_type_values(self):
        from remnawave.enums import ClientType

        assert {c.value for c in ClientType} == {
            "stash",
            "singbox",
            "mihomo",
            "json",
            "v2ray-json",
            "clash",
        }

    def test_template_type_values(self):
        from remnawave.enums import TemplateType

        assert {t.value for t in TemplateType} == {
            "XRAY_JSON",
            "XRAY_BASE64",
            "MIHOMO",
            "STASH",
            "CLASH",
            "SINGBOX",
        }

    def test_expired_webhook_events_removed(self):
        import typing

        from remnawave.enums.webhook import TUserEvents

        values = set(typing.get_args(TUserEvents))
        assert "user.expiration" in values
        assert not any(v.startswith("user.expires_in_") for v in values)
