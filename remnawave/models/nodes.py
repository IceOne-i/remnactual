from datetime import datetime
from typing import Annotated, List, Optional, Union, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    StringConstraints,
    model_serializer,
)

from remnawave.models.internal_squads import InboundsDto


class ExcludedInbounds(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None


class RestartEventResponse(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class DeleteResponse(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class ReorderNodeItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class GetAllNodesTagsResponseDto(BaseModel):
    """Response with all nodes tags"""
    tags: List[str]


class NodeProviderDto(BaseModel):
    """Node provider information"""
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class NodeConfigProfileDto(BaseModel):
    active_config_profile_uuid: Optional[UUID] = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[InboundsDto] = Field(alias="activeInbounds")


class NodeNetworkInterfaceDto(BaseModel):
    interface: str
    rx_bytes_per_sec: float = Field(alias="rxBytesPerSec")
    tx_bytes_per_sec: float = Field(alias="txBytesPerSec")
    rx_total: float = Field(alias="rxTotal")
    tx_total: float = Field(alias="txTotal")


class NodeSystemInfoDto(BaseModel):
    arch: str
    cpus: int
    cpu_model: str = Field(alias="cpuModel")
    memory_total: float = Field(alias="memoryTotal")
    hostname: str
    platform: str
    release: str
    type: str
    version: str
    network_interfaces: List[str] = Field(alias="networkInterfaces")


class NodeSystemStatsDto(BaseModel):
    memory_free: float = Field(alias="memoryFree")
    memory_used: float = Field(alias="memoryUsed")
    uptime: float
    load_avg: List[float] = Field(alias="loadAvg")
    interface: Optional[NodeNetworkInterfaceDto] = None


class NodeSystemDto(BaseModel):
    info: NodeSystemInfoDto
    stats: NodeSystemStatsDto


class NodeVersionsDto(BaseModel):
    xray: str
    node: str


class NodeConfigProfileRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    active_config_profile_uuid: UUID = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[UUID] = Field(alias="activeInbounds")


class CreateNodeRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    address: Annotated[str, StringConstraints(min_length=2)]
    port: Optional[int] = Field(None, ge=1, le=65535)
    is_traffic_tracking_active: Optional[bool] = Field(
        False, 
        serialization_alias="isTrafficTrackingActive",
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[int] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[int] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        "XX",
        serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0, le=100
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    note: Optional[str] = Field(None, serialization_alias="note", max_length=255)
    proxy_url: Optional[str] = Field(
        None,
        serialization_alias="proxyUrl",
        pattern=r"^socks5://(?:[^:@/\s]+(?::[^@/\s]*)?@)?[^:@/\s]+:\d{1,5}$",
    )
    config_profile: NodeConfigProfileRequestDto = Field(
        serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[List[Annotated[str, StringConstraints(max_length=36, pattern=r'^[A-Z0-9_:]+$')]]] = Field(
        None, 
        serialization_alias="tags",
        max_length=10
    )
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )


class UpdateNodeRequestDto(BaseModel):
    uuid: UUID
    name: Annotated[Optional[str], StringConstraints(min_length=3, max_length=30)] = None
    address: Annotated[Optional[str], StringConstraints(min_length=2)] = None
    port: Optional[float] = Field(None, ge=1, le=65535)  # ИСПРАВЛЕН тип на float
    is_traffic_tracking_active: Optional[bool] = Field(
        None, serialization_alias="isTrafficTrackingActive"
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[float] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[float] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        None, serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0, le=100
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    note: Optional[str] = Field(None, serialization_alias="note", max_length=255)
    proxy_url: Optional[str] = Field(
        None,
        serialization_alias="proxyUrl",
        pattern=r"^socks5://(?:[^:@/\s]+(?::[^@/\s]*)?@)?[^:@/\s]+:\d{1,5}$",
    )
    config_profile: Optional[NodeConfigProfileRequestDto] = Field(
        None, serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[List[Annotated[str, StringConstraints(max_length=36, pattern=r'^[A-Z0-9_:]+$')]]] = Field(
        None,
        serialization_alias="tags",
        max_length=10
    )
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )


class ReorderNodeRequestDto(BaseModel):
    nodes: List[ReorderNodeItem]


class NodeResponseDto(BaseModel):
    uuid: UUID
    name: str
    address: str
    port: Optional[int] = None
    is_connected: bool = Field(alias="isConnected")
    is_disabled: bool = Field(alias="isDisabled")
    is_connecting: bool = Field(alias="isConnecting")
    last_status_change: Optional[datetime] = Field(None, alias="lastStatusChange")
    last_status_message: Optional[str] = Field(None, alias="lastStatusMessage")
    xray_uptime: float = Field(0, alias="xrayUptime")
    is_traffic_tracking_active: bool = Field(alias="isTrafficTrackingActive")
    traffic_reset_day: Optional[int] = Field(None, alias="trafficResetDay")
    traffic_limit_bytes: Optional[float] = Field(None, alias="trafficLimitBytes")
    traffic_used_bytes: Optional[float] = Field(None, alias="trafficUsedBytes")
    notify_percent: Optional[int] = Field(None, alias="notifyPercent")
    users_online: Optional[int] = Field(None, alias="usersOnline")
    view_position: int = Field(alias="viewPosition")
    country_code: str = Field(alias="countryCode")
    consumption_multiplier: float = Field(alias="consumptionMultiplier")
    node_consumption_multiplier: Optional[float] = Field(None, alias="nodeConsumptionMultiplier")
    note: Optional[str] = Field(None, alias="note")
    proxy_url: Optional[str] = Field(None, alias="proxyUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config_profile: NodeConfigProfileDto = Field(alias="configProfile")
    provider_uuid: Optional[UUID] = Field(None, alias="providerUuid")
    provider: Optional[NodeProviderDto] = None
    tags: List[str] = Field(default_factory=list, alias="tags")
    active_plugin_uuid: Optional[UUID] = Field(None, alias="activePluginUuid")
    system: Optional[NodeSystemDto] = None
    versions: Optional[NodeVersionsDto] = None

    # Плоские поля до 2.8 — теперь живут в system/versions
    @property
    def xray_version(self) -> Optional[str]:
        return self.versions.xray if self.versions else None

    @property
    def node_version(self) -> Optional[str]:
        return self.versions.node if self.versions else None

    @property
    def cpu_count(self) -> Optional[int]:
        return self.system.info.cpus if self.system else None

    @property
    def cpu_model(self) -> Optional[str]:
        return self.system.info.cpu_model if self.system else None

    @property
    def total_ram(self) -> Optional[float]:
        return self.system.info.memory_total if self.system else None


class CreateNodeResponseDto(NodeResponseDto):
    pass


class UpdateNodeResponseDto(NodeResponseDto):
    pass


class GetOneNodeResponseDto(NodeResponseDto):
    pass


class GetAllNodesResponseDto(RootModel[List[NodeResponseDto]]):
    root: List[NodeResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)
    
    def __len__(self):
        """Return length of list"""
        return len(self.root)



class EnableNodeResponseDto(NodeResponseDto):
    pass


class DisableNodeResponseDto(NodeResponseDto):
    pass


class RestartNodeResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class RestartAllNodesResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class ReorderNodeResponseDto(RootModel[List[NodeResponseDto]]):
    root: List[NodeResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)
    
    def __len__(self):
        """Return length of list"""
        return len(self.root)


class DeleteNodeResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")

    def __bool__(self):
        return self.is_deleted


class _ForceRestartBody(BaseModel):
    """`forceRestart` обязателен в теле запроса (2.8), поэтому ключ отправляется
    всегда — даже если вызывающий оставил значение по умолчанию."""
    model_config = ConfigDict(populate_by_name=True)

    force_restart: bool = Field(default=False, alias="forceRestart")

    @model_serializer(mode="wrap")
    def _always_emit_force_restart(self, handler, info):
        data = handler(self)
        data.setdefault(
            "forceRestart" if info.by_alias else "force_restart", self.force_restart
        )
        return data


class RestartAllNodesRequestBodyDto(_ForceRestartBody):
    pass


class RestartNodeRequestBodyDto(_ForceRestartBody):
    pass


class ResetNodeTrafficRequestDto(BaseModel):
    uuid: Union[str, UUID] = Field(alias="uuid")

class ResetNodeTrafficResponseDto(RestartEventResponse):
    pass

class ConfigProfileData(BaseModel):
    """Config profile data for modification"""
    model_config = ConfigDict(populate_by_name=True)

    active_config_profile_uuid: str = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[str] = Field(alias="activeInbounds", min_length=1)


class ProfileModificationRequestDto(BaseModel):
    """Request to modify profiles for multiple nodes"""
    model_config = ConfigDict(populate_by_name=True)

    uuids: List[str] = Field(min_length=1)
    config_profile: ConfigProfileData = Field(alias="configProfile")


class ProfileModificationResponseData(BaseModel):
    """Profile modification response data"""
    event_sent: bool = Field(alias="eventSent")


class ProfileModificationResponseDto(ProfileModificationResponseData):
    """Profile modification response"""
    pass

# Для обратной совместимости
RestartAllNodesRequestDto = RestartAllNodesRequestBodyDto
NodesResponseDto = NodeResponseDto


NodeBulkActionType = Literal["ENABLE", "DISABLE", "RESTART", "RESET_TRAFFIC"]


class NodesBulkActionsRequestDto(BaseModel):
    """Request for performing bulk actions on nodes"""
    uuids: List[UUID] = Field(min_length=1)
    action: NodeBulkActionType = Field(description="Action to perform on nodes")


class NodesBulkActionsResponseDto(BaseModel):
    """Response after performing bulk actions on nodes"""
    event_sent: bool = Field(alias="eventSent")


class BulkNodesUpdateFieldsDto(BaseModel):
    """Поля, применяемые к каждой ноде в POST /nodes/bulk-actions/update"""
    model_config = ConfigDict(populate_by_name=True)

    country_code: Optional[Annotated[str, StringConstraints(max_length=2)]] = Field(
        None, alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, alias="consumptionMultiplier", ge=0, le=100
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    provider_uuid: Optional[UUID] = Field(None, alias="providerUuid")
    tags: Optional[
        List[Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]]
    ] = Field(None, max_length=10)
    active_plugin_uuid: Optional[UUID] = Field(None, alias="activePluginUuid")
    note: Optional[Annotated[str, StringConstraints(max_length=255)]] = None


class BulkNodesUpdateRequestDto(BaseModel):
    """Request for POST /nodes/bulk-actions/update"""
    model_config = ConfigDict(populate_by_name=True)

    uuids: List[UUID] = Field(min_length=1)
    fields: BulkNodesUpdateFieldsDto


class BulkNodesUpdateResponseDto(NodesBulkActionsResponseDto):
    """OpenAPI alias for bulk nodes update response"""
    pass