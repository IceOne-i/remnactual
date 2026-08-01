from datetime import datetime
from typing import List, Optional, Literal, Union
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from remnawave.models.node_plugins import TorrentBlockerReportPayloadDto
from remnawave.models.nodes import (
    NodeNetworkInterfaceDto as NodeSystemInterfaceDto,
    NodeSystemDto,
    NodeSystemInfoDto,
    NodeSystemStatsDto,
    NodeVersionsDto,
)
from remnawave.enums import (
    TUsersStatus, TUserEvents, TUserHwidDevicesEvents, TServiceEvents, TNodeEvents, TErrorsEvents, TCRMEvents, TTorrentBlockerEvents, TResetPeriods
)
# ---------------- USER ---------------- #

class LastConnectedNodeDto(BaseModel):
    """Оставлена только для обратной совместимости.

    В 3.0 панель не присылает `lastConnectedNode` в webhook-событиях (см.
    `ExtendedUsersSchema`); последний узел доступен как
    `user_traffic.last_connected_node_uuid`.
    """

    node_name: str
    country_code: str
    connected_at: datetime

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookInternalSquadDto(BaseModel):
    uuid: UUID
    name: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}



class WebhookUserTrafficDto(BaseModel):
    """User traffic information for webhooks"""
    used_traffic_bytes: int
    lifetime_used_traffic_bytes: int
    online_at: Optional[datetime] = None
    first_connected_at: Optional[datetime] = None
    last_connected_node_uuid: Optional[UUID] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class BaseUserDto(BaseModel):
    # 3.0: у пользователя больше нет `uuid` — идентификатор это числовой `id`.
    id: int
    short_uuid: str
    username: str
    status: TUsersStatus
    user_traffic: WebhookUserTrafficDto

    traffic_limit_bytes: int
    traffic_limit_strategy: TResetPeriods

    expire_at: datetime
    sub_revoked_at: Optional[datetime] = None
    last_traffic_reset_at: Optional[datetime] = None

    trojan_password: str
    vless_uuid: UUID
    ss_password: str

    description: Optional[str] = None
    tag: Optional[str] = None
    telegram_id: Optional[int] = None
    email: Optional[str] = None
    external_squad_uuid: Optional[UUID] = None

    hwid_device_limit: Optional[int] = None
    last_triggered_threshold: int

    subscription_url: str

    created_at: datetime
    updated_at: datetime


    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    # Backward compatibility properties
    @property
    def used_traffic_bytes(self) -> int:
        """Backward compatibility property"""
        return self.user_traffic.used_traffic_bytes
    
    @property
    def lifetime_used_traffic_bytes(self) -> int:
        """Backward compatibility property"""
        return self.user_traffic.lifetime_used_traffic_bytes
    
    @property
    def online_at(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.online_at
    
    @property
    def first_connected_at(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.first_connected_at
    
    @property
    def last_connected_node_uuid(self) -> Optional[UUID]:
        """Backward compatibility property"""
        return self.user_traffic.last_connected_node_uuid



class UserDto(BaseUserDto):
    """`ExtendedUsersSchema` контракта 3.0 — тело `data` во всех user-событиях.

    3.0: панель больше не присылает `uuid`, `subLastUserAgent`, `subLastOpenedAt`
    и `lastConnectedNode` — эти поля удалены.
    Для `user.not_connected` `activeInternalSquads` всегда пуст.
    """

    active_internal_squads: List[WebhookInternalSquadDto] = Field(default_factory=list)

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserEventDto(BaseModel):
    event_name: TUserEvents
    user: UserDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- HWID DEVICES ---------------- #

class HwidUserDeviceDto(BaseModel):
    hwid: str
    # 2.8: userUuid заменён на числовой userId
    user_id: int
    platform: Optional[str] = None
    os_version: Optional[str] = None
    device_model: Optional[str] = None
    user_agent: Optional[str] = None
    request_ip: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserHwidDeviceEventDto(BaseModel):
    data: dict
    event_name: TUserHwidDevicesEvents

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    @classmethod
    def build(cls, user: UserDto, hwid_device: HwidUserDeviceDto, event: TUserHwidDevicesEvents):
        return cls(data={"user": user, "hwidUserDevice": hwid_device}, event_name=event)
    
    @property
    def user(self) -> UserDto:
        return self.data["user"]

    @property
    def hwid_user_device(self) -> HwidUserDeviceDto:
        return self.data["hwidUserDevice"]

# ---------------- SERVICE EVENTS ---------------- #

class LoginAttemptDto(BaseModel):
    username: str
    ip: str
    user_agent: str
    description: Optional[str] = None
    password: Optional[str] = None
    
    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ServiceEventDto(BaseModel):
    event_name: TServiceEvents
    data: dict

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- NODE ENTITIES ---------------- #

class ConfigProfileInboundDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID

    tag: str
    type: str
    network: Optional[str]
    security: Optional[str]
    port: Optional[int]

    raw_inbound: Optional[dict]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookInfraBillingHistoryDto(BaseModel):
    total_amount: int
    total_bills: int

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookInfraBillingNodeDto(BaseModel):
    node_uuid: UUID
    name: str
    country_code: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookInfraProviderDto(BaseModel):
    name: str
    uuid: UUID
    favicon_link: Optional[str] = None
    login_url: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    billing_history: Optional[WebhookInfraBillingHistoryDto] = None
    billing_nodes: Optional[List[WebhookInfraBillingNodeDto]] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookNodeConfigProfileDto(BaseModel):
    """Nested config profile for node webhook events"""
    active_config_profile_uuid: Optional[UUID] = None
    active_inbounds: List[ConfigProfileInboundDto] = Field(default_factory=list)

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookNodeDto(BaseModel):
    uuid: UUID
    name: str
    address: str
    port: Optional[int] = None
    is_connected: bool
    is_connecting: bool
    is_disabled: bool
    last_status_change: Optional[datetime] = None
    last_status_message: Optional[str] = None

    xray_uptime: float = 0
    users_online: Optional[float] = None

    is_traffic_tracking_active: bool
    traffic_reset_day: Optional[int] = None
    traffic_limit_bytes: Optional[float] = None
    traffic_used_bytes: Optional[float] = None
    notify_percent: Optional[int] = None

    view_position: int
    country_code: str
    consumption_multiplier: float
    node_consumption_multiplier: Optional[float] = None
    proxy_url: Optional[str] = None
    note: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime

    config_profile: WebhookNodeConfigProfileDto

    provider_uuid: Optional[UUID] = None
    provider: Optional[WebhookInfraProviderDto] = None

    active_plugin_uuid: Optional[UUID] = None
    system: Optional[NodeSystemDto] = None
    versions: Optional[NodeVersionsDto] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    # Backward-compat shims for code that used the flat fields directly
    @property
    def active_config_profile_uuid(self) -> Optional[UUID]:
        return self.config_profile.active_config_profile_uuid

    @property
    def active_inbounds(self) -> List[ConfigProfileInboundDto]:
        return self.config_profile.active_inbounds


class NodeEventDto(BaseModel):
    event_name: TNodeEvents
    data: WebhookNodeDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

# ---------------- ERROR EVENTS ---------------- #

# https://github.com/remnawave/backend/blob/main/src/queue/user-jobs/user-jobs.processor.ts#L224
# Not implemented yet!

class ErrorDto(BaseModel):
    description: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class CustomErrorEventDto(BaseModel):
    event_name: TErrorsEvents
    data: ErrorDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- CRM EVENTS ---------------- #

class BillingNodeDto(BaseModel):
    provider_name: str
    node_name: str
    next_billing_at: datetime
    login_url: str

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class CrmEventDto(BaseModel):
    event_name: TCRMEvents
    data: BillingNodeDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- TORRENT BLOCKER EVENTS ---------------- #

class TorrentBlockerReportDto(BaseModel):
    node: WebhookNodeDto
    user: Optional[UserDto] = None
    report: Optional[TorrentBlockerReportPayloadDto] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class TorrentBlockerEventDto(BaseModel):
    event_name: TTorrentBlockerEvents
    data: TorrentBlockerReportDto

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


# ---------------- WEBHOOK PAYLOAD ---------------- #

class WebhookMetaDto(BaseModel):
    """Дополнительные данные события (`user.not_connected`, `user.expiration`)"""
    not_connected_after_hours: Optional[float] = None
    expiration: Optional[float] = None

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class WebhookPayloadDto(BaseModel):
    event: str
    timestamp: datetime
    scope: Optional[str] = None
    meta: Optional[WebhookMetaDto] = None
    data: Union[
        UserDto,
        WebhookNodeDto,
        HwidUserDeviceDto,
        LoginAttemptDto,
        UserHwidDeviceEventDto,
        BillingNodeDto,
        ErrorDto,
        TorrentBlockerReportDto,
        dict
    ]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    @classmethod
    def from_dict(cls, payload: dict) -> "WebhookPayloadDto":
        event = payload.get("event", "")
        data_raw = payload.get("data", {})

        if event.startswith("user."):
            data = UserDto(**data_raw)
        elif event.startswith("user_hwid_devices."):
            user = UserDto(**data_raw["user"])
            hwid_device = HwidUserDeviceDto(**data_raw["hwidUserDevice"])
            data = UserHwidDeviceEventDto.build(
                user=user,
                hwid_device=hwid_device,
                event=event,
            )
        elif event.startswith("node."):
            data = WebhookNodeDto(**data_raw)
        elif event.startswith("service."):
            login_attempt_data = (
                data_raw.get("loginAttempt") if isinstance(data_raw, dict) else None
            )
            if event.startswith("service.login_attempt") and login_attempt_data:
                data = LoginAttemptDto(**login_attempt_data)
            else:
                # service.panel_started / subpage_config_changed / api_token_* —
                # отдаём сырой словарь, как объявлено в union
                data = data_raw
        elif event.startswith("errors."):
            data = ErrorDto(**data_raw)
        elif event.startswith("crm."):
            data = BillingNodeDto(**data_raw)
        elif event.startswith("torrent_blocker."):
            data = TorrentBlockerReportDto(**data_raw)
        else:
            data = data_raw

        timestamp_raw = payload.get("timestamp")
        if isinstance(timestamp_raw, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp_raw)
        else:
            timestamp = timestamp_raw

        meta_raw = payload.get("meta")
        meta = WebhookMetaDto(**meta_raw) if isinstance(meta_raw, dict) else None

        return cls(
            event=event,
            data=data,
            timestamp=timestamp,
            scope=payload.get("scope"),
            meta=meta,
        )


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# Эти имена конфликтовали с одноимёнными REST-моделями в remnawave.models.
# Внутри модуля webhook они по-прежнему доступны под старыми именами.
InternalSquadDto = WebhookInternalSquadDto
UserTrafficDto = WebhookUserTrafficDto
InfraBillingHistoryDto = WebhookInfraBillingHistoryDto
InfraBillingNodeDto = WebhookInfraBillingNodeDto
InfraProviderDto = WebhookInfraProviderDto
NodeDto = WebhookNodeDto
