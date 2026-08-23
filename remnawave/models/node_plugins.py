from datetime import datetime
from typing import Any, Annotated, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models._serialization import AlwaysEmitModel


class TorrentBlockerUserDto(BaseModel):
    """3.0: у пользователя больше нет `uuid`, отчёт ссылается на него через `userId`."""

    username: str


class TorrentBlockerNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class TorrentBlockerActionReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    blocked: bool
    ip: str
    block_duration: float = Field(alias="blockDuration")
    will_unblock_at: datetime = Field(alias="willUnblockAt")
    user_id: str = Field(alias="userId")
    processed_at: datetime = Field(alias="processedAt")


class TorrentBlockerXrayReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: Optional[str] = None
    level: Optional[float] = None
    protocol: Optional[str] = None
    network: str
    source: Optional[str] = None
    destination: str
    route_target: Optional[str] = Field(default=None, alias="routeTarget")
    original_target: Optional[str] = Field(default=None, alias="originalTarget")
    inbound_tag: Optional[str] = Field(default=None, alias="inboundTag")
    inbound_name: Optional[str] = Field(default=None, alias="inboundName")
    inbound_local: Optional[str] = Field(default=None, alias="inboundLocal")
    outbound_tag: Optional[str] = Field(default=None, alias="outboundTag")
    ts: float


class TorrentBlockerReportPayloadDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action_report: TorrentBlockerActionReportDto = Field(alias="actionReport")
    xray_report: TorrentBlockerXrayReportDto = Field(alias="xrayReport")


class TorrentBlockerReportRecordDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: float
    user_id: int = Field(alias="userId")
    node_id: float = Field(alias="nodeId")
    user: TorrentBlockerUserDto
    node: TorrentBlockerNodeDto
    report: TorrentBlockerReportPayloadDto
    created_at: datetime = Field(alias="createdAt")


class TorrentBlockerReportsData(BaseModel):
    records: List[TorrentBlockerReportRecordDto]
    total: float


class GetTorrentBlockerReportsResponseDto(TorrentBlockerReportsData):
    pass


class TorrentBlockerStatsDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    distinct_nodes: float = Field(alias="distinctNodes")
    distinct_users: float = Field(alias="distinctUsers")
    total_reports: float = Field(alias="totalReports")
    reports_last_24_hours: float = Field(alias="reportsLast24Hours")


class TorrentBlockerTopUserDto(BaseModel):
    """3.0: `uuid` заменён на числовой `userId`."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    color: str
    username: str
    total: float


class TorrentBlockerTopNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    country_code: str = Field(alias="countryCode")
    color: str
    name: str
    total: float


class GetTorrentBlockerReportsStatsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    stats: TorrentBlockerStatsDto
    top_users: List[TorrentBlockerTopUserDto] = Field(alias="topUsers")
    top_nodes: List[TorrentBlockerTopNodeDto] = Field(alias="topNodes")


class NodePluginDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    plugin_config: Any | None = Field(alias="pluginConfig")


class GetNodePluginsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: float
    node_plugins: List[NodePluginDto] = Field(alias="nodePlugins")


class GetNodePluginResponseDto(NodePluginDto):
    pass


class UpdateNodePluginBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Optional[
        Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    ] = None
    plugin_config: Optional[Any] = Field(default=None, alias="pluginConfig")


class UpdateNodePluginResponseDto(NodePluginDto):
    pass


class CreateNodePluginBodyDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]


class CreateNodePluginResponseDto(NodePluginDto):
    pass


class ReorderNodePluginItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_position: int = Field(alias="viewPosition")
    uuid: UUID


class ReorderNodePluginsBodyDto(BaseModel):
    items: List[ReorderNodePluginItem]


class ReorderNodePluginsResponseDto(GetNodePluginsResponseDto):
    pass


class CloneNodePluginBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    clone_from_uuid: UUID = Field(alias="cloneFromUuid")


class CloneNodePluginResponseDto(NodePluginDto):
    pass


class BlockIpItemDto(BaseModel):
    ip: str
    timeout: float


class BlockIpsCommandDto(BaseModel):
    command: Literal["blockIps"]
    ips: List[BlockIpItemDto]


class UnblockIpsCommandDto(BaseModel):
    command: Literal["unblockIps"]
    ips: List[str]


class RecreateTablesCommandDto(BaseModel):
    command: Literal["recreateTables"]


PluginCommandDto = Union[BlockIpsCommandDto, UnblockIpsCommandDto, RecreateTablesCommandDto]


class TargetAllNodesDto(BaseModel):
    target: Literal["allNodes"]


class TargetSpecificNodesDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    target: Literal["specificNodes"]
    node_uuids: List[UUID] = Field(alias="nodeUuids")


PluginTargetNodesDto = Union[TargetAllNodesDto, TargetSpecificNodesDto]


class PluginExecutorBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    command: PluginCommandDto
    target_nodes: PluginTargetNodesDto = Field(alias="targetNodes")


# ---------------------------------------------------------------------------
# 3.3.0: Shared Lists — общие списки, на которые ссылаются конфиги плагинов
# ---------------------------------------------------------------------------

#: Имя общего списка: ^[A-Za-z0-9_-]+$, 2..255. Префикс `ext:` панель добавляет сама.
SharedListName = Annotated[
    str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_-]+$")
]


class SharedListIpListConfig(AlwaysEmitModel):
    """Общий список IP-адресов и CIDR-диапазонов"""
    model_config = ConfigDict(populate_by_name=True)

    __always_emit__ = ("type",)

    type: Literal["ipList"] = "ipList"
    items: List[str]


class SharedListAsListConfig(AlwaysEmitModel):
    """Общий список номеров автономных систем (ASN без префикса `AS`)"""
    model_config = ConfigDict(populate_by_name=True)

    __always_emit__ = ("type",)

    type: Literal["asList"] = "asList"
    items: List[Annotated[int, Field(ge=1, le=4294967295)]]


#: Тело общего списка. Неизвестный SDK тип остаётся словарём: контракт объявляет
#: `config` произвольным объектом и валидирует его уже на панели (ошибка A252).
SharedListConfig = Annotated[
    Union[SharedListIpListConfig, SharedListAsListConfig, Dict[str, Any]],
    Field(union_mode="left_to_right"),
]


class SharedListDto(BaseModel):
    """Общий список целиком"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    config: SharedListConfig


class SharedListPreviewDto(BaseModel):
    """Общий список без элементов — только имя, тип и их количество"""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str
    items_count: int = Field(alias="itemsCount")


class GetSharedListsResponseDto(BaseModel):
    """GET /node-plugins/shared-lists"""
    model_config = ConfigDict(populate_by_name=True)

    total: int
    shared_lists: List[SharedListPreviewDto] = Field(alias="sharedLists")


class GetSharedListResponseDto(SharedListDto):
    """GET /node-plugins/shared-lists/{name}"""


class CreateSharedListBodyDto(BaseModel):
    """POST /node-plugins/shared-lists"""
    name: SharedListName
    config: SharedListConfig


class CreateSharedListResponseDto(SharedListDto):
    """Ответ POST /node-plugins/shared-lists"""


class UpdateSharedListBodyDto(BaseModel):
    """PATCH /node-plugins/shared-lists"""
    name: SharedListName
    config: SharedListConfig


class UpdateSharedListResponseDto(SharedListDto):
    """Ответ PATCH /node-plugins/shared-lists"""


class SyncSharedListBodyDto(BaseModel):
    """POST /node-plugins/shared-lists/actions/sync

    Раскатывает каждый плагин, ссылающийся на список, по нодам, где он активен.
    """
    name: SharedListName


class SyncNodePluginBodyDto(BaseModel):
    """POST /node-plugins/actions/sync

    Отправляет текущий конфиг плагина (вместе с общими списками) на все
    подключённые ноды, где плагин активен.
    """
    uuid: UUID


# DELETE /node-plugins/shared-lists/{name} отвечает 204 без тела — DTO не нужен.


# Legacy aliases (имена 2.8)
UpdateNodePluginRequestDto = UpdateNodePluginBodyDto
CreateNodePluginRequestDto = CreateNodePluginBodyDto
ReorderNodePluginsRequestDto = ReorderNodePluginsBodyDto
CloneNodePluginRequestDto = CloneNodePluginBodyDto
PluginExecutorRequestDto = PluginExecutorBodyDto
