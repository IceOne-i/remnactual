"""Regression tests for the Remnawave 3.3.x contract delta.

Each test pins something `@remnawave/backend-contract` changed between 3.2.3 and
3.3.2. They run offline — no panel required.

Дельта целиком аддитивная:

* Node Integrations — новый контроллер (`/node-integrations`, 5 эндпоинтов);
* Shared Lists — общие списки плагинов нод (`/node-plugins/shared-lists`, 6 эндпоинтов);
* ``POST /node-plugins/actions/sync`` — раскатка плагина по нодам;
* geocheck ноды — ``POST/GET /connections/geocheck/...``;
* Host Mapper — правка сгенерированного конфига хоста по типам клиентов;
* ``integrationUuids`` у ноды — в ответе и в телах ``POST``/``PATCH``/``bulk-actions``;
* ``respondWithRemarks`` в модификациях SRR-правила.

Пол панели остаётся 3.0.0, поэтому каждое новое поле обязано парситься и когда его
нет: панель до 3.3.0 его просто не присылает.
"""
import ast
import pathlib
from uuid import UUID

import pytest
from pydantic import ValidationError

from remnawave.models import NodeConfigProfileBodyDto, NodeResponseDto, WebhookNodeDto

REPO = pathlib.Path(__file__).resolve().parent.parent

NODE_UUID = UUID("b1f0e2b4-1f5c-4c9a-9b2e-2f2f6a7c8d90")
INTEGRATION_UUID = UUID("6f1c2f3a-4b5c-4d6e-8f90-1a2b3c4d5e6f")

NODE_PAYLOAD = {
    "uuid": str(NODE_UUID),
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

HOST_PAYLOAD = {
    "uuid": "1c1f0f0a-1111-4222-8333-444455556666",
    "viewPosition": 1,
    "remark": "de-1",
    "address": "example.com",
    "port": 443,
    "path": None,
    "sni": None,
    "host": None,
    "alpn": None,
    "fingerprint": None,
    "muxParams": None,
    "sockoptParams": None,
    "inbound": {"configProfileUuid": None, "configProfileInboundUuid": None},
    "serverDescription": None,
    "tags": [],
    "vlessRouteId": None,
    "shuffleHost": False,
    "mihomoX25519": False,
    "nodes": [],
    "xrayJsonTemplateUuid": None,
}

# ClientOverridesSchema из resolved-proxy-config: ключи обязательны, но nullable.
CLIENT_OVERRIDES_PAYLOAD = {
    "shuffleHost": False,
    "mihomoX25519": False,
    "mihomoIpVersion": None,
    "serverDescription": None,
    "xrayJsonTemplate": None,
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


def _route(controller_module: str, method_name: str):
    """(HTTP-метод, путь) эндпоинта контроллера."""
    decorators = _endpoint_decorators(controller_module, method_name)
    assert len(decorators) == 1, f"{method_name}: ожидался ровно один декоратор"
    dec = decorators[0]
    method = getattr(dec.func, "id", None)
    path = dec.args[0].value if dec.args else None
    return method, path


def _response_class(controller_module: str, method_name: str):
    """AST-узел аргумента `response_class` эндпоинта."""
    return [
        kw.value
        for dec in _endpoint_decorators(controller_module, method_name)
        for kw in dec.keywords
        if kw.arg == "response_class"
    ]


def _declares_empty_response(controller_module: str, method_name: str) -> bool:
    """Панель отвечает 202/204 без тела — значит `response_class=None`."""
    classes = _response_class(controller_module, method_name)
    return (
        len(classes) == 1
        and isinstance(classes[0], ast.Constant)
        and classes[0].value is None
    )


# --------------------------------------------------------------------------- #
# 3.3.0: Node Integrations controller
# --------------------------------------------------------------------------- #

class TestNodeIntegrationsController:
    def test_controller_is_importable(self):
        from remnawave.controllers import NodeIntegrationsController

        assert NodeIntegrationsController is not None

    def test_sdk_exposes_the_controller(self):
        from remnawave import RemnawaveSDK

        sdk = RemnawaveSDK(base_url="https://panel.example.com", token="t")
        assert sdk.node_integrations is not None

    @pytest.mark.parametrize(
        ("method_name", "http_method", "path"),
        [
            ("get_all_node_integrations", "get", "/node-integrations"),
            ("get_node_integration", "get", "/node-integrations/{uuid}"),
            ("create_node_integration", "post", "/node-integrations"),
            ("update_node_integration", "patch", "/node-integrations"),
            ("delete_node_integration", "delete", "/node-integrations/{uuid}"),
        ],
    )
    def test_endpoints_are_registered_on_the_contract_paths(
        self, method_name, http_method, path
    ):
        from remnawave.controllers import NodeIntegrationsController

        assert callable(getattr(NodeIntegrationsController, method_name, None))
        assert _route("node_integrations", method_name) == (http_method, path)

    def test_delete_declares_an_empty_response(self):
        """DELETE отвечает 204 No Content."""
        assert _declares_empty_response("node_integrations", "delete_node_integration")


class TestNodeIntegrationModels:
    def test_response_parses_the_contract_payload(self):
        from remnawave.models import NodeIntegrationDto

        integration = NodeIntegrationDto.model_validate(
            {
                "uuid": str(INTEGRATION_UUID),
                "name": "warp",
                "description": None,
                "config": {"outbounds": []},
            }
        )
        assert integration.uuid == INTEGRATION_UUID
        assert integration.name == "warp"
        assert integration.description is None
        assert integration.config == {"outbounds": []}

    def test_list_response_parses_total_and_items(self):
        from remnawave.models import GetNodeIntegrationsResponseDto

        response = GetNodeIntegrationsResponseDto.model_validate(
            {
                "total": 1,
                "nodeIntegrations": [
                    {
                        "uuid": str(INTEGRATION_UUID),
                        "name": "warp",
                        "description": "wg",
                        "config": {},
                    }
                ],
            }
        )
        assert response.total == 1
        assert response.node_integrations[0].name == "warp"

    def test_create_body_serializes_the_contract_keys(self):
        from remnawave.models import CreateNodeIntegrationBodyDto

        body = CreateNodeIntegrationBodyDto(name="warp", config={"outbounds": []})
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "name": "warp",
            "config": {"outbounds": []},
        }

    @pytest.mark.parametrize("name", ["w", "w" * 31])
    def test_create_body_rejects_names_outside_2_30(self, name):
        from remnawave.models import CreateNodeIntegrationBodyDto

        with pytest.raises(ValidationError):
            CreateNodeIntegrationBodyDto(name=name, config={})

    def test_create_body_rejects_too_long_description(self):
        from remnawave.models import CreateNodeIntegrationBodyDto

        with pytest.raises(ValidationError):
            CreateNodeIntegrationBodyDto(name="warp", description="d" * 256, config={})

    def test_update_body_sends_restart_nodes(self):
        from remnawave.models import UpdateNodeIntegrationBodyDto

        body = UpdateNodeIntegrationBodyDto(uuid=INTEGRATION_UUID, restart_nodes=True)
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "uuid": str(INTEGRATION_UUID),
            "restartNodes": True,
        }

    def test_update_body_omits_untouched_fields(self):
        """`exclude_unset` — нетронутый config не должен затирать конфиг на панели."""
        from remnawave.models import UpdateNodeIntegrationBodyDto

        dumped = UpdateNodeIntegrationBodyDto(uuid=INTEGRATION_UUID).model_dump(
            exclude_unset=True, by_alias=True
        )
        assert dumped == {"uuid": INTEGRATION_UUID}


class TestNodeIntegrationScopesAndErrors:
    def test_scopes_are_grantable(self):
        from remnawave.enums import Scope

        assert Scope.NODE_INTEGRATIONS_ALL == "node-integrations:*"
        assert Scope.NODE_INTEGRATIONS_READ == "node-integrations:read"
        assert Scope.NODE_INTEGRATIONS_WRITE == "node-integrations:write"
        assert Scope.NODE_INTEGRATIONS_LIST == "node-integrations:list"
        assert Scope.NODE_INTEGRATIONS_GET == "node-integrations:get"
        assert Scope.NODE_INTEGRATIONS_CREATE == "node-integrations:create"
        assert Scope.NODE_INTEGRATIONS_UPDATE == "node-integrations:update"
        assert Scope.NODE_INTEGRATIONS_DELETE == "node-integrations:delete"

    def test_error_codes_are_known(self):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES

        assert ErrorCode.NODE_INTEGRATION_NOT_FOUND == "A238"
        assert ERROR_MESSAGES["A238"] == "Node integration not found"
        assert ERROR_HTTP_CODES["A238"] == 404

        assert ErrorCode.NODE_INTEGRATION_NAME_ALREADY_EXISTS == "A244"
        assert ERROR_HTTP_CODES["A244"] == 400


# --------------------------------------------------------------------------- #
# 3.3.0: Shared Lists (node plugins)
# --------------------------------------------------------------------------- #

class TestSharedListsEndpoints:
    @pytest.mark.parametrize(
        ("method_name", "http_method", "path"),
        [
            ("get_shared_lists", "get", "/node-plugins/shared-lists"),
            ("get_shared_list", "get", "/node-plugins/shared-lists/{name}"),
            ("create_shared_list", "post", "/node-plugins/shared-lists"),
            ("update_shared_list", "patch", "/node-plugins/shared-lists"),
            ("delete_shared_list", "delete", "/node-plugins/shared-lists/{name}"),
            (
                "sync_shared_list",
                "post",
                "/node-plugins/shared-lists/actions/sync",
            ),
            ("sync_node_plugin", "post", "/node-plugins/actions/sync"),
        ],
    )
    def test_endpoints_are_registered_on_the_contract_paths(
        self, method_name, http_method, path
    ):
        from remnawave.controllers import NodePluginsController

        assert callable(getattr(NodePluginsController, method_name, None))
        assert _route("node_plugins", method_name) == (http_method, path)

    @pytest.mark.parametrize(
        "method_name", ["delete_shared_list", "sync_shared_list", "sync_node_plugin"]
    )
    def test_empty_responses(self, method_name):
        """DELETE отвечает 204, обе синхронизации — 202, тела нет."""
        assert _declares_empty_response("node_plugins", method_name)


class TestSharedListModels:
    def test_preview_response_parses_the_contract_payload(self):
        from remnawave.models import GetSharedListsResponseDto

        response = GetSharedListsResponseDto.model_validate(
            {
                "total": 1,
                "sharedLists": [{"name": "ext:geo_ru", "type": "ipList", "itemsCount": 3}],
            }
        )
        assert response.total == 1
        assert response.shared_lists[0].name == "ext:geo_ru"
        assert response.shared_lists[0].items_count == 3

    def test_ip_list_config_is_typed(self):
        from remnawave.models import GetSharedListResponseDto, SharedListIpListConfig

        shared_list = GetSharedListResponseDto.model_validate(
            {
                "name": "ext:geo_ru",
                "config": {"type": "ipList", "items": ["1.1.1.1", "10.0.0.0/8"]},
            }
        )
        assert isinstance(shared_list.config, SharedListIpListConfig)
        assert shared_list.config.items == ["1.1.1.1", "10.0.0.0/8"]

    def test_as_list_config_is_typed(self):
        from remnawave.models import GetSharedListResponseDto, SharedListAsListConfig

        shared_list = GetSharedListResponseDto.model_validate(
            {"name": "ext:asn", "config": {"type": "asList", "items": [13335, 15169]}}
        )
        assert isinstance(shared_list.config, SharedListAsListConfig)
        assert shared_list.config.items == [13335, 15169]

    def test_unknown_config_type_stays_a_dict(self):
        """Панель вправе добавить новый тип списка — SDK не должен падать."""
        from remnawave.models import GetSharedListResponseDto

        shared_list = GetSharedListResponseDto.model_validate(
            {"name": "ext:domains", "config": {"type": "domainList", "items": ["a.com"]}}
        )
        assert shared_list.config == {"type": "domainList", "items": ["a.com"]}

    def test_create_body_serializes_the_contract_keys(self):
        from remnawave.models import CreateSharedListBodyDto

        body = CreateSharedListBodyDto(
            name="geo_ru", config={"type": "ipList", "items": ["1.1.1.1"]}
        )
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "name": "geo_ru",
            "config": {"type": "ipList", "items": ["1.1.1.1"]},
        }

    @pytest.mark.parametrize("name", ["g", "geo ru", "ext:geo_ru", "geo/ru"])
    def test_name_outside_the_contract_pattern_is_rejected(self, name):
        """^[A-Za-z0-9_-]+$, 2..255 — префикс `ext:` панель добавляет сама."""
        from remnawave.models import CreateSharedListBodyDto

        with pytest.raises(ValidationError):
            CreateSharedListBodyDto(name=name, config={"type": "ipList", "items": []})

    def test_sync_body_serializes_the_name(self):
        from remnawave.models import SyncSharedListBodyDto

        body = SyncSharedListBodyDto(name="geo_ru")
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "name": "geo_ru"
        }

    def test_sync_node_plugin_body_serializes_the_uuid(self):
        from remnawave.models import SyncNodePluginBodyDto

        body = SyncNodePluginBodyDto(uuid=NODE_UUID)
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "uuid": str(NODE_UUID)
        }


class TestSharedListScopesAndErrors:
    def test_scopes_are_grantable(self):
        from remnawave.enums import Scope

        assert Scope.NODE_PLUGINS_SYNC == "node-plugins:sync"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_LIST == "node-plugins:shared-lists-list"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_GET == "node-plugins:shared-lists-get"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_CREATE == "node-plugins:shared-lists-create"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_UPDATE == "node-plugins:shared-lists-update"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_DELETE == "node-plugins:shared-lists-delete"
        assert Scope.NODE_PLUGINS_SHARED_LISTS_SYNC == "node-plugins:shared-lists-sync"

    def test_error_codes_are_known(self):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES

        assert ErrorCode.SHARED_LIST_NOT_FOUND == "A245"
        assert ERROR_MESSAGES["A245"] == "Shared list not found"
        assert ERROR_HTTP_CODES["A245"] == 404

        assert ErrorCode.INVALID_SHARED_LIST_CONFIG == "A252"
        assert ERROR_HTTP_CODES["A252"] == 400


# --------------------------------------------------------------------------- #
# 3.3.0: geocheck by node
# --------------------------------------------------------------------------- #

class TestGeocheckEndpoints:
    @pytest.mark.parametrize(
        ("method_name", "http_method", "path"),
        [
            ("geocheck_by_node", "post", "/connections/geocheck/{nodeUuid}"),
            ("geocheck_by_node_result", "get", "/connections/geocheck/{jobId}"),
        ],
    )
    def test_endpoints_are_registered_on_the_contract_paths(
        self, method_name, http_method, path
    ):
        from remnawave.controllers import ConnectionsController

        assert callable(getattr(ConnectionsController, method_name, None))
        assert _route("connections", method_name) == (http_method, path)


class TestGeocheckModels:
    def test_body_sends_only_the_ip(self):
        from remnawave.models import GeocheckByNodeBodyDto

        body = GeocheckByNodeBodyDto(ip="1.2.3.4")
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "ip": "1.2.3.4"
        }

    def test_body_may_be_empty(self):
        from remnawave.models import GeocheckByNodeBodyDto

        assert GeocheckByNodeBodyDto().model_dump(exclude_unset=True, by_alias=True) == {}

    def test_ip_and_interface_together_are_rejected(self):
        """Контракт: `Only one of "ip" or "interface" can be specified`."""
        from remnawave.models import GeocheckByNodeBodyDto

        with pytest.raises(ValidationError):
            GeocheckByNodeBodyDto(ip="1.2.3.4", interface="eth0")

    def test_job_response_parses_the_job_id(self):
        from remnawave.models import GeocheckByNodeResponseDto

        assert GeocheckByNodeResponseDto.model_validate({"jobId": "job-1"}).job_id == "job-1"

    def test_result_parses_the_completed_payload(self):
        from remnawave.models import GeocheckByNodeResultResponseDto

        result = GeocheckByNodeResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": False,
                "result": {
                    "success": True,
                    "nodeUuid": str(NODE_UUID),
                    "image": {
                        "format": "svg",
                        "media_type": "image/svg+xml",
                        "encoding": "base64",
                        "data": "PHN2Zy8+",
                    },
                    "rawReport": {"country": "DE"},
                    "message": None,
                },
            }
        )
        assert result.is_completed is True
        assert result.result.node_uuid == NODE_UUID
        assert result.result.image.media_type == "image/svg+xml"
        assert result.result.image.data == "PHN2Zy8+"
        assert result.result.raw_report == {"country": "DE"}

    def test_result_is_nullable_while_the_job_runs(self):
        from remnawave.models import GeocheckByNodeResultResponseDto

        result = GeocheckByNodeResultResponseDto.model_validate(
            {"isCompleted": False, "isFailed": False, "result": None}
        )
        assert result.result is None

    def test_image_is_nullable(self):
        from remnawave.models import GeocheckByNodeResultResponseDto

        result = GeocheckByNodeResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": True,
                "result": {
                    "success": False,
                    "nodeUuid": str(NODE_UUID),
                    "image": None,
                    "rawReport": None,
                    "message": "node did not answer",
                },
            }
        )
        assert result.result.image is None
        assert result.result.message == "node did not answer"


class TestGeocheckScopes:
    def test_scopes_are_grantable(self):
        from remnawave.enums import Scope

        assert Scope.CONNECTIONS_GEOCHECK == "connections:geocheck"
        assert Scope.CONNECTIONS_GEOCHECK_RESULT == "connections:geocheck-result"


# --------------------------------------------------------------------------- #
# 3.3.0: Host Mapper
# --------------------------------------------------------------------------- #

class TestHostMapperOperations:
    def test_copy_serializes_from_as_the_reserved_key(self):
        from remnawave.models import HostMapperCopyOperation

        operation = HostMapperCopyOperation(
            from_="streamSettings.tlsSettings.cipherSuites",
            to="streamSettings.tlsSettings.cipherSuites",
        )
        assert operation.model_dump(mode="json", by_alias=True) == {
            "op": "copy",
            "from": "streamSettings.tlsSettings.cipherSuites",
            "to": "streamSettings.tlsSettings.cipherSuites",
        }

    def test_copy_accepts_the_panel_key(self):
        from remnawave.models import HostMapperCopyOperation

        operation = HostMapperCopyOperation.model_validate(
            {"op": "copy", "from": "$host.address", "to": "sni"}
        )
        assert operation.from_ == "$host.address"

    def test_set_carries_any_json_value(self):
        from remnawave.models import HostMapperSetOperation

        operation = HostMapperSetOperation(
            to="streamSettings.tlsSettings.enableSessionResumption", value=True
        )
        assert operation.model_dump(mode="json", by_alias=True) == {
            "op": "set",
            "to": "streamSettings.tlsSettings.enableSessionResumption",
            "value": True,
        }

    def test_unset_carries_only_the_target(self):
        from remnawave.models import HostMapperUnsetOperation

        assert HostMapperUnsetOperation(to="mux").model_dump(
            mode="json", by_alias=True
        ) == {"op": "unset", "to": "mux"}

    def test_mapper_parses_every_client_section(self):
        from remnawave.models import (
            HostMapperCopyOperation,
            HostMapperDto,
            HostMapperSetOperation,
        )

        mapper = HostMapperDto.model_validate(
            {
                "xrayJson": [
                    {
                        "op": "copy",
                        "from": "streamSettings.tlsSettings.cipherSuites",
                        "to": "streamSettings.tlsSettings.cipherSuites",
                    }
                ],
                "mihomo": [{"op": "set", "to": "ip-version", "value": "ipv4"}],
                "base64": [{"op": "unset", "to": "fm"}],
                "singbox": [{"op": "set", "to": "tls.utls.fingerprint", "value": "chrome"}],
            }
        )
        assert isinstance(mapper.xray_json[0], HostMapperCopyOperation)
        assert isinstance(mapper.mihomo[0], HostMapperSetOperation)
        assert mapper.base64[0].to == "fm"
        assert mapper.singbox[0].value == "chrome"

    def test_unknown_operation_is_rejected(self):
        from remnawave.models import HostMapperDto

        with pytest.raises(ValidationError):
            HostMapperDto.model_validate({"xrayJson": [{"op": "move", "to": "a"}]})

    def test_empty_mapper_parses(self):
        from remnawave.models import HostMapperDto

        mapper = HostMapperDto.model_validate({})
        assert mapper.xray_json is None
        assert mapper.mihomo is None
        assert mapper.base64 is None
        assert mapper.singbox is None


class TestHostMapperOnHosts:
    def test_create_body_sends_the_mapper(self):
        from remnawave.models import (
            CreateHostBodyDto,
            CreateHostInboundData,
            HostMapperDto,
            HostMapperUnsetOperation,
        )

        body = CreateHostBodyDto(
            inbound=CreateHostInboundData(
                config_profile_uuid=NODE_UUID, config_profile_inbound_uuid=NODE_UUID
            ),
            remark="de-1",
            address="example.com",
            port=443,
            mapper=HostMapperDto(xray_json=[HostMapperUnsetOperation(to="mux")]),
        )
        dumped = body.model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["mapper"] == {"xrayJson": [{"op": "unset", "to": "mux"}]}

    def test_update_body_sends_the_mapper(self):
        from remnawave.models import (
            HostMapperDto,
            HostMapperSetOperation,
            UpdateHostBodyDto,
        )

        body = UpdateHostBodyDto(
            uuid=NODE_UUID,
            mapper=HostMapperDto(base64=[HostMapperSetOperation(to="fp", value="chrome")]),
        )
        dumped = body.model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["mapper"] == {"base64": [{"op": "set", "to": "fp", "value": "chrome"}]}

    def test_bodies_omit_the_mapper_when_untouched(self):
        from remnawave.models import UpdateHostBodyDto

        dumped = UpdateHostBodyDto(uuid=NODE_UUID).model_dump(
            exclude_unset=True, by_alias=True
        )
        assert "mapper" not in dumped

    def test_response_parses_the_mapper(self):
        from remnawave.models import HostResponseDto

        host = HostResponseDto.model_validate(
            {**HOST_PAYLOAD, "mapper": {"mihomo": [{"op": "unset", "to": "smux"}]}}
        )
        assert host.mapper.mihomo[0].to == "smux"

    def test_response_without_the_mapper_still_parses(self):
        """Панель до 3.3.0 поля не присылает."""
        from remnawave.models import HostResponseDto

        host = HostResponseDto.model_validate(HOST_PAYLOAD)
        assert host.mapper.xray_json is None

    def test_raw_subscription_client_overrides_parse_the_mapper(self):
        from remnawave.models import ResolvedProxyClientOverrides

        overrides = ResolvedProxyClientOverrides.model_validate(
            {
                **CLIENT_OVERRIDES_PAYLOAD,
                "mapper": {"singbox": [{"op": "unset", "to": "multiplex"}]},
            }
        )
        assert overrides.mapper.singbox[0].to == "multiplex"

    def test_raw_subscription_client_overrides_without_mapper_still_parse(self):
        from remnawave.models import ResolvedProxyClientOverrides

        overrides = ResolvedProxyClientOverrides.model_validate(CLIENT_OVERRIDES_PAYLOAD)
        assert overrides.mapper.singbox is None


# --------------------------------------------------------------------------- #
# 3.3.0: nodes carry integration UUIDs
# --------------------------------------------------------------------------- #

class TestNodeIntegrationUuids:
    CONFIG_PROFILE = {"activeConfigProfileUuid": NODE_UUID, "activeInbounds": []}

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

        return UpdateNodeBodyDto(uuid=NODE_UUID, **extra)

    def test_create_body_sends_integration_uuids(self):
        dumped = self._create_body(integration_uuids=[INTEGRATION_UUID]).model_dump(
            mode="json", exclude_unset=True, by_alias=True
        )
        assert dumped["integrationUuids"] == [str(INTEGRATION_UUID)]

    def test_update_body_sends_integration_uuids(self):
        dumped = self._update_body(integration_uuids=[INTEGRATION_UUID]).model_dump(
            mode="json", exclude_unset=True, by_alias=True
        )
        assert dumped["integrationUuids"] == [str(INTEGRATION_UUID)]

    def test_bodies_omit_integration_uuids_when_untouched(self):
        assert "integrationUuids" not in self._create_body().model_dump(
            exclude_unset=True, by_alias=True
        )
        assert "integrationUuids" not in self._update_body().model_dump(
            exclude_unset=True, by_alias=True
        )

    def test_more_than_20_integrations_is_rejected(self):
        with pytest.raises(ValidationError):
            self._create_body(integration_uuids=[INTEGRATION_UUID] * 21)

    def test_bulk_update_fields_send_integration_uuids(self):
        from remnawave.models import BulkNodesUpdateFieldsDto

        dumped = BulkNodesUpdateFieldsDto(
            integration_uuids=[INTEGRATION_UUID]
        ).model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["integrationUuids"] == [str(INTEGRATION_UUID)]

    def test_rest_node_parses_integration_uuids(self):
        node = NodeResponseDto.model_validate(
            {**NODE_PAYLOAD, "integrationUuids": [str(INTEGRATION_UUID)]}
        )
        assert node.integration_uuids == [INTEGRATION_UUID]

    def test_rest_node_without_integration_uuids_still_parses(self):
        """Панель до 3.3.0 поля не присылает."""
        assert NodeResponseDto.model_validate(NODE_PAYLOAD).integration_uuids == []

    def test_webhook_node_parses_integration_uuids(self):
        node = WebhookNodeDto.model_validate(
            {**NODE_PAYLOAD, "integrationUuids": [str(INTEGRATION_UUID)]}
        )
        assert node.integration_uuids == [INTEGRATION_UUID]

    def test_webhook_node_without_integration_uuids_still_parses(self):
        assert WebhookNodeDto.model_validate(NODE_PAYLOAD).integration_uuids == []


# --------------------------------------------------------------------------- #
# 3.3.0: respondWithRemarks in SRR modifications
# --------------------------------------------------------------------------- #

class TestRespondWithRemarks:
    def test_modifications_serialize_the_remarks(self):
        from remnawave.models import ResponseModifications

        modifications = ResponseModifications(respond_with_remarks=["Renew me"])
        dumped = modifications.model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped == {"respondWithRemarks": ["Renew me"]}

    def test_modifications_parse_the_panel_payload(self):
        from remnawave.models import ResponseModifications

        modifications = ResponseModifications.model_validate(
            {"respondWithRemarks": ["Renew me", "at example.com"]}
        )
        assert modifications.respond_with_remarks == ["Renew me", "at example.com"]

    def test_modifications_without_the_field_still_parse(self):
        from remnawave.models import ResponseModifications

        assert ResponseModifications.model_validate({}).respond_with_remarks is None
