"""Regression tests for the Remnawave 3.2.3 contract delta.

Each test pins something `@remnawave/backend-contract` changed between 3.2.0 and
3.2.3. They run offline — no panel required.

Дельта целиком аддитивная:

* ``POST /snippets/actions/sync`` — 202 без тела, скоуп ``snippets:sync``, ошибка ``A237``;
* ``ips`` у ноды — в ответе и в телах ``POST``/``PATCH /nodes``;
* ``cipherSuites`` в TLS-опциях raw-подписки.

Пол панели остаётся 3.0.0, поэтому каждое новое поле обязано парситься и когда его
нет: панель до 3.2.3 его просто не присылает.
"""
import ast
import pathlib
from uuid import UUID

import pytest
from pydantic import ValidationError

from remnawave.controllers.snippets import SnippetsController
from remnawave.models import NodeConfigProfileBodyDto, NodeResponseDto, WebhookNodeDto

REPO = pathlib.Path(__file__).resolve().parent.parent

NODE_PAYLOAD = {
    "uuid": "b1f0e2b4-1f5c-4c9a-9b2e-2f2f6a7c8d90",
    "id": 7,
    "name": "de-1",
    "address": "10.0.0.1",
    "port": 3000,
    "isConnected": True,
    "isDisabled": False,
    "isConnecting": False,
    "isTrafficTrackingActive": False,
    "viewPosition": 1,
    "countryCode": "DE",
    "consumptionMultiplier": 1.0,
    "createdAt": "2026-08-01T00:00:00.000Z",
    "updatedAt": "2026-08-01T00:00:00.000Z",
    "configProfile": {"activeConfigProfileUuid": None, "activeInbounds": []},
}

# TlsSecurityOptionsSchema из resolved-proxy-config: все ключи обязательны, но nullable.
TLS_PAYLOAD = {
    "pinnedPeerCertSha256": None,
    "verifyPeerCertByName": None,
    "alpn": "h2",
    "enableSessionResumption": False,
    "fingerprint": "chrome",
    "serverName": "example.com",
    "echConfigList": None,
    "echForceQuery": None,
    "echSockopt": None,
}


def _endpoint_decorators(controller_module: str, method_name: str):
    """Декораторы-вызовы конкретного метода контроллера, прочитанные из исходника."""
    tree = ast.parse(
        (REPO / "remnawave" / "controllers" / f"{controller_module}.py").read_text(
            encoding="utf-8"
        )
    )
    return [
        dec
        for fn in ast.walk(tree)
        if isinstance(fn, ast.AsyncFunctionDef) and fn.name == method_name
        for dec in fn.decorator_list
        if isinstance(dec, ast.Call)
    ]


# --------------------------------------------------------------------------- #
# 3.2.3: POST /snippets/actions/sync
# --------------------------------------------------------------------------- #

class TestSnippetSyncEndpoint:
    def test_controller_exposes_the_endpoint(self):
        assert callable(getattr(SnippetsController, "sync_snippet", None))

    def test_endpoint_is_registered_on_the_contract_path(self):
        decorators = _endpoint_decorators("snippets", "sync_snippet")
        methods = {getattr(dec.func, "id", None) for dec in decorators}
        paths = {
            dec.args[0].value
            for dec in decorators
            if dec.args and isinstance(dec.args[0], ast.Constant)
        }
        assert methods == {"post"}
        assert paths == {"/snippets/actions/sync"}

    def test_endpoint_declares_an_empty_response(self):
        """Панель отвечает 202 Accepted без тела — значит `response_class=None`."""
        response_classes = [
            kw.value
            for dec in _endpoint_decorators("snippets", "sync_snippet")
            for kw in dec.keywords
            if kw.arg == "response_class"
        ]
        assert len(response_classes) == 1
        assert isinstance(response_classes[0], ast.Constant)
        assert response_classes[0].value is None


class TestSyncSnippetBody:
    def test_body_serializes_the_name(self):
        from remnawave.models import SyncSnippetBodyDto

        body = SyncSnippetBodyDto(name="geodata-snippet")
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "name": "geodata-snippet"
        }

    def test_name_shorter_than_two_characters_is_rejected(self):
        from remnawave.models import SyncSnippetBodyDto

        with pytest.raises(ValidationError):
            SyncSnippetBodyDto(name="g")

    def test_name_with_illegal_characters_is_rejected(self):
        """Контракт: ^[A-Za-z0-9_\\s-]+$ — те же ограничения, что у create/update/delete."""
        from remnawave.models import SyncSnippetBodyDto

        with pytest.raises(ValidationError):
            SyncSnippetBodyDto(name="geodata/snippet")


class TestSnippetSyncScopeAndError:
    def test_scope_is_grantable(self):
        from remnawave.enums import Scope

        assert Scope.SNIPPETS_SYNC == "snippets:sync"

    def test_error_code_is_known(self):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES

        assert ErrorCode.SYNC_SNIPPET_ERROR == "A237"
        assert ERROR_MESSAGES["A237"] == "Sync snippet error"
        assert ERROR_HTTP_CODES["A237"] == 500


# --------------------------------------------------------------------------- #
# 3.2.3: nodes carry a list of IP addresses
# --------------------------------------------------------------------------- #

class TestNodeIpStatusEnum:
    def test_matches_the_contract(self):
        from remnawave.enums import NodeIpStatus

        assert {status.value for status in NodeIpStatus} == {
            "INBOUND",
            "OUTBOUND",
            "MANAGEMENT",
            "TRANSIT",
            "MONITORING",
            "RESERVE",
            "BLOCKED",
            "FLAGGED",
            "DEPRECATED",
            "UNKNOWN",
        }


class TestNodeIpsInResponses:
    def test_rest_node_parses_ips(self):
        from remnawave.enums import NodeIpStatus

        node = NodeResponseDto.model_validate(
            {**NODE_PAYLOAD, "ips": [{"ip": "10.0.0.1", "status": "INBOUND"}]}
        )
        assert str(node.ips[0].ip) == "10.0.0.1"
        assert node.ips[0].status is NodeIpStatus.INBOUND

    def test_rest_node_parses_ipv6(self):
        node = NodeResponseDto.model_validate(
            {**NODE_PAYLOAD, "ips": [{"ip": "2001:db8::1", "status": "OUTBOUND"}]}
        )
        assert str(node.ips[0].ip) == "2001:db8::1"

    def test_rest_node_without_ips_still_parses(self):
        """Панель до 3.2.3 поля не присылает."""
        assert NodeResponseDto.model_validate(NODE_PAYLOAD).ips == []

    def test_webhook_node_parses_ips(self):
        """События ноды используют полный NodesSchema."""
        from remnawave.enums import NodeIpStatus

        node = WebhookNodeDto.model_validate(
            {**NODE_PAYLOAD, "ips": [{"ip": "10.0.0.2", "status": "RESERVE"}]}
        )
        assert node.ips[0].status is NodeIpStatus.RESERVE

    def test_webhook_node_without_ips_still_parses(self):
        assert WebhookNodeDto.model_validate(NODE_PAYLOAD).ips == []


class TestNodeIpsInRequestBodies:
    CONFIG_PROFILE = {
        "activeConfigProfileUuid": UUID("b1f0e2b4-1f5c-4c9a-9b2e-2f2f6a7c8d90"),
        "activeInbounds": [],
    }

    def _create_body(self, **extra):
        from remnawave.models import CreateNodeBodyDto

        return CreateNodeBodyDto(
            name="de-1",
            address="10.0.0.1",
            config_profile=NodeConfigProfileBodyDto.model_validate(self.CONFIG_PROFILE),
            **extra,
        )

    def _update_body(self, **extra):
        from remnawave.models import UpdateNodeBodyDto

        return UpdateNodeBodyDto(
            uuid=UUID("b1f0e2b4-1f5c-4c9a-9b2e-2f2f6a7c8d90"), **extra
        )

    def test_create_body_sends_ips(self):
        from remnawave.enums import NodeIpStatus
        from remnawave.models import NodeIpDto

        body = self._create_body(
            ips=[NodeIpDto(ip="10.0.0.1", status=NodeIpStatus.MANAGEMENT)]
        )
        dumped = body.model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["ips"] == [{"ip": "10.0.0.1", "status": "MANAGEMENT"}]

    def test_update_body_sends_ips(self):
        from remnawave.enums import NodeIpStatus
        from remnawave.models import NodeIpDto

        body = self._update_body(
            ips=[NodeIpDto(ip="2001:db8::1", status=NodeIpStatus.BLOCKED)]
        )
        dumped = body.model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["ips"] == [{"ip": "2001:db8::1", "status": "BLOCKED"}]

    def test_bodies_omit_ips_when_untouched(self):
        """`exclude_unset` — нетронутое поле не должно затирать список на панели."""
        assert "ips" not in self._create_body().model_dump(
            exclude_unset=True, by_alias=True
        )
        assert "ips" not in self._update_body().model_dump(
            exclude_unset=True, by_alias=True
        )

    def test_more_than_64_ips_is_rejected(self):
        from remnawave.enums import NodeIpStatus
        from remnawave.models import NodeIpDto

        ips = [
            NodeIpDto(ip=f"10.0.0.{n}", status=NodeIpStatus.UNKNOWN) for n in range(65)
        ]
        with pytest.raises(ValidationError):
            self._create_body(ips=ips)

    def test_malformed_ip_is_rejected(self):
        from remnawave.enums import NodeIpStatus
        from remnawave.models import NodeIpDto

        with pytest.raises(ValidationError):
            NodeIpDto(ip="10.0.0.256", status=NodeIpStatus.UNKNOWN)


# --------------------------------------------------------------------------- #
# 3.2.3: cipherSuites reaches the raw subscription
# --------------------------------------------------------------------------- #

class TestTlsCipherSuites:
    def test_tls_options_parse_cipher_suites(self):
        from remnawave.models import TlsSecurityOptions

        options = TlsSecurityOptions.model_validate(
            {**TLS_PAYLOAD, "cipherSuites": "TLS_AES_128_GCM_SHA256"}
        )
        assert options.cipher_suites == "TLS_AES_128_GCM_SHA256"

    def test_cipher_suites_is_nullable(self):
        from remnawave.models import TlsSecurityOptions

        options = TlsSecurityOptions.model_validate({**TLS_PAYLOAD, "cipherSuites": None})
        assert options.cipher_suites is None

    def test_tls_options_without_cipher_suites_still_parse(self):
        """Панель до 3.2.3 ключа не присылает."""
        from remnawave.models import TlsSecurityOptions

        assert TlsSecurityOptions.model_validate(TLS_PAYLOAD).cipher_suites is None
