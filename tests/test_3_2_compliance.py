"""Regression tests for the Remnawave 3.1 / 3.2 contract deltas.

Each test pins something `@remnawave/backend-contract` changed between 3.0.0 and
3.2.0. They run offline — no panel required.

The panel floor stays at 3.0.0, so every additive field must also parse when it is
absent: a 3.0.x panel simply does not send it.
"""
import ast
import pathlib

from remnawave.controllers.system import SystemController
from remnawave.models import (
    GetConfigurationResponseDto,
    NodeResponseDto,
    SubscriptionRequestHistoryRecord,
    SubscriptionRequestRecord,
    WebhookNodeDto,
)

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


# --------------------------------------------------------------------------- #
# 3.1: nodes expose a numeric id next to the uuid
# --------------------------------------------------------------------------- #

class TestNodeNumericId:
    def test_rest_node_parses_id(self):
        node = NodeResponseDto.model_validate(NODE_PAYLOAD)
        assert node.id == 7
        # {uuid} остаётся ключом маршрутов — id ничего не заменил
        assert str(node.uuid) == NODE_PAYLOAD["uuid"]

    def test_rest_node_without_id_still_parses(self):
        """Панель 3.0.x числовой id не присылает."""
        payload = {k: v for k, v in NODE_PAYLOAD.items() if k != "id"}
        assert NodeResponseDto.model_validate(payload).id is None

    def test_webhook_node_event_parses_id(self):
        """`data.id` событий ноды и `data.node.id` событий torrent-blocker —
        обе схемы контракта используют полный NodesSchema."""
        node = WebhookNodeDto.model_validate(NODE_PAYLOAD)
        assert node.id == 7

    def test_webhook_node_without_id_still_parses(self):
        payload = {k: v for k, v in NODE_PAYLOAD.items() if k != "id"}
        assert WebhookNodeDto.model_validate(payload).id is None


# --------------------------------------------------------------------------- #
# 3.1: subscription request history reports the matched SRR rule
# --------------------------------------------------------------------------- #

class TestSubscriptionRequestHistorySrrFields:
    RECORD = {
        "id": 1,
        "userId": 42,
        "srrResponseType": "XRAY_JSON",
        "srrRuleName": "default",
        "requestIp": "10.0.0.9",
        "userAgent": "Happ/1.0",
        "requestAt": "2026-08-01T00:00:00.000Z",
    }

    def test_history_record_parses_srr_fields(self):
        record = SubscriptionRequestHistoryRecord.model_validate(self.RECORD)
        assert record.srr_response_type == "XRAY_JSON"
        assert record.srr_rule_name == "default"

    def test_user_scoped_record_parses_srr_fields(self):
        """`GET /users/{userId}/subscription-request-history` отдаёт те же поля."""
        record = SubscriptionRequestRecord.model_validate(self.RECORD)
        assert record.srr_response_type == "XRAY_JSON"
        assert record.srr_rule_name == "default"

    def test_rule_name_is_nullable(self):
        record = SubscriptionRequestHistoryRecord.model_validate(
            {**self.RECORD, "srrRuleName": None}
        )
        assert record.srr_rule_name is None

    def test_records_without_srr_fields_still_parse(self):
        payload = {
            k: v
            for k, v in self.RECORD.items()
            if k not in ("srrResponseType", "srrRuleName")
        }
        for model in (SubscriptionRequestHistoryRecord, SubscriptionRequestRecord):
            record = model.model_validate(payload)
            assert record.srr_response_type is None, model.__name__
            assert record.srr_rule_name is None, model.__name__


# --------------------------------------------------------------------------- #
# 3.2: GET /system/configuration
# --------------------------------------------------------------------------- #

class TestSystemConfigurationEndpoint:
    RESPONSE = {
        "notifications": {
            "webhook": True,
            "bandwidthUsage": [80, 100],
            "notConnectedAfter": [24],
            "expirationNotifications": [1, 3, 7],
        },
        "service": {
            "cleanUsageHistory": True,
            "disableUserUsageRecords": False,
            "disableSrhRecords": False,
            "exportToRedisStream": True,
        },
        "misc": {
            "shortUuidLength": 16,
            "subPublicDomain": "sub.example.com",
            "userUsageIgnoreBelowBytes": 1024,
        },
    }

    def test_controller_exposes_the_endpoint(self):
        assert callable(getattr(SystemController, "get_configuration", None))

    def test_endpoint_is_registered_on_the_contract_path(self):
        tree = ast.parse(
            (REPO / "remnawave" / "controllers" / "system.py").read_text(encoding="utf-8")
        )
        paths = {
            dec.args[0].value
            for fn in ast.walk(tree)
            if isinstance(fn, ast.AsyncFunctionDef) and fn.name == "get_configuration"
            for dec in fn.decorator_list
            if isinstance(dec, ast.Call) and dec.args and isinstance(dec.args[0], ast.Constant)
        }
        assert paths == {"/system/configuration"}

    def test_response_parses(self):
        dto = GetConfigurationResponseDto.model_validate(self.RESPONSE)
        assert dto.notifications.webhook is True
        assert dto.notifications.expiration_notifications == [1, 3, 7]
        assert dto.service.disable_srh_records is False
        assert dto.service.export_to_redis_stream is True
        assert dto.misc.short_uuid_length == 16
        assert dto.misc.sub_public_domain == "sub.example.com"
        assert dto.misc.user_usage_ignore_below_bytes == 1024

    def test_notification_thresholds_are_nullable(self):
        response = {
            **self.RESPONSE,
            "notifications": {
                "webhook": False,
                "bandwidthUsage": None,
                "notConnectedAfter": None,
                "expirationNotifications": None,
            },
        }
        dto = GetConfigurationResponseDto.model_validate(response)
        assert dto.notifications.bandwidth_usage is None

    def test_scope_is_grantable(self):
        from remnawave.enums import Scope

        assert Scope.SYSTEM_CONFIGURATION == "system:configuration"


# --------------------------------------------------------------------------- #
# 3.1: A084 renamed
# --------------------------------------------------------------------------- #

class TestErrorCodeRename:
    def test_new_name_and_message(self):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_MESSAGES

        assert ErrorCode.BULK_DELETE_USERS_BY_USER_IDS_ERROR == "A084"
        assert ERROR_MESSAGES["A084"] == "Bulk delete users by user IDs error"

    def test_old_name_survives_as_an_alias(self):
        from remnawave.enums import ErrorCode

        assert (
            ErrorCode.BULK_DELETE_USERS_BY_UUID_ERROR
            is ErrorCode.BULK_DELETE_USERS_BY_USER_IDS_ERROR
        )
