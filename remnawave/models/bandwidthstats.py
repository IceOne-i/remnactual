from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


# ============ Legacy Models (Deprecated) ============

class NodeUsageResponseDto(BaseModel):
    """Deprecated: Old node usage model"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    total: float
    total_download: float = Field(alias="totalDownload")
    total_upload: float = Field(alias="totalUpload")
    human_readable_total: str = Field(alias="humanReadableTotal")
    human_readable_total_download: str = Field(alias="humanReadableTotalDownload")
    human_readable_total_upload: str = Field(alias="humanReadableTotalUpload")
    date: date


class NodesUsageResponseDto(RootModel[List[NodeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class GetNodesUsageByRangeResponseDto(RootModel[List[NodeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class NodeRealtimeUsageResponseDto(BaseModel):
    """Deprecated: Use NodeRealtimeUsageItem instead"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class NodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesRealtimeUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class GetNodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesRealtimeUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


# ============ New Stats Models ============

# Realtime Stats

class NodeRealtimeUsageItem(BaseModel):
    """Node realtime usage item"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class GetStatsNodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageItem]]):
    """Response for nodes realtime usage"""
    @property
    def response(self) -> List[NodeRealtimeUsageItem]:
        return self.root
    
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# Stats Nodes Usage (with charts)

class TopNodeItem(BaseModel):
    """Top node item"""
    uuid: UUID
    color: str
    name: str
    country_code: str = Field(alias="countryCode")
    total: float


class NodeSeriesItem(BaseModel):
    """Node series item for charts"""
    uuid: UUID
    name: str
    color: str
    country_code: str = Field(alias="countryCode")
    total: float
    data: List[float]


class StatsNodesUsageData(BaseModel):
    """Stats nodes usage data"""
    categories: List[str]
    sparkline_data: List[float] = Field(alias="sparklineData")
    top_nodes: List[TopNodeItem] = Field(alias="topNodes")
    series: List[NodeSeriesItem]


class GetStatsNodesUsageResponseDto(RootModel[StatsNodesUsageData]):
    """Response for stats nodes usage"""
    @property
    def response(self) -> StatsNodesUsageData:
        return self.root


# Stats Node Users Usage (with charts)

class TopUserItem(BaseModel):
    """Top user item"""
    color: str
    username: str
    total: float


class StatsNodeUsersUsageData(BaseModel):
    """Stats node users usage data"""
    categories: List[str]
    sparkline_data: List[float] = Field(alias="sparklineData")
    top_users: List[TopUserItem] = Field(alias="topUsers")


class GetStatsNodeUsersUsageResponseDto(RootModel[StatsNodeUsersUsageData]):
    """Response for stats node users usage"""
    @property
    def response(self) -> StatsNodeUsersUsageData:
        return self.root


# Stats Nodes Users Usage by Nodes UUIDs (POST /bandwidth-stats/nodes/users)

class GetStatsNodesUsersUsageBodyDto(BaseModel):
    """Request for nodes users usage by nodes UUIDs"""
    nodes_uuids: List[UUID] = Field(serialization_alias="nodesUuids", min_length=1)


class TopNodesUserItem(BaseModel):
    """Top user item for nodes users usage"""
    color: str
    username: str
    total: float


class StatsNodesUsersUsageData(BaseModel):
    """Stats nodes users usage data"""
    categories: List[str]
    sparkline_data: List[float] = Field(alias="sparklineData")
    top_users: List[TopNodesUserItem] = Field(alias="topUsers")


class GetStatsNodesUsersUsageResponseDto(RootModel[StatsNodesUsersUsageData]):
    """Response for stats nodes users usage by nodes UUIDs"""
    @property
    def response(self) -> StatsNodesUsersUsageData:
        return self.root


# Stats User Usage (with charts)

class StatsUserUsageData(BaseModel):
    """Stats user usage data"""
    categories: List[str]
    sparkline_data: List[float] = Field(alias="sparklineData")
    top_nodes: List[TopNodeItem] = Field(alias="topNodes")
    series: List[NodeSeriesItem]


class GetStatsUserUsageResponseDto(RootModel[StatsUserUsageData]):
    """Response for stats user usage"""
    @property
    def response(self) -> StatsUserUsageData:
        return self.root


# ============ Node Usage by Threshold (POST /bandwidth-stats/nodes/usage) ============


class GetNodeUsageBodyDto(BaseModel):
    """Request for users exceeding a traffic threshold on the given nodes"""
    nodes_uuids: List[UUID] = Field(serialization_alias="nodesUuids", min_length=1)


class NodeUsageUserItem(BaseModel):
    """User total usage on a node over the requested period"""
    id: int
    total_bytes: float = Field(alias="totalBytes")


class NodeUsageNodeItem(BaseModel):
    """Per-node bucket of users exceeding the requested threshold"""
    uuid: UUID
    users: List[NodeUsageUserItem]


class GetNodeUsageResponseDto(BaseModel):
    """Response for users exceeding a traffic threshold on the given nodes"""
    nodes: List[NodeUsageNodeItem]


# ============ Internal Squad Usage (3.0) ============


class InternalSquadUsageUserItem(BaseModel):
    """User total usage on the internal squad nodes over the requested period"""
    id: int
    total_bytes: float = Field(alias="totalBytes")


class GetInternalSquadUsageResponseDto(BaseModel):
    """Response for internal squad users traffic usage"""
    squad_uuid: UUID = Field(alias="squadUuid")
    users: List[InternalSquadUsageUserItem]
    # Курсор возвращается строкой (stringified user id), хотя в запрос уходит числом.
    next_cursor: Optional[str] = Field(None, alias="nextCursor")
    has_more: bool = Field(alias="hasMore")


class InternalSquadUserUsageNodeItem(BaseModel):
    """Used bytes on a single node for a single day"""
    uuid: UUID
    total_bytes: float = Field(alias="totalBytes")


class InternalSquadUserUsageDayItem(BaseModel):
    """Daily usage bucket, zero-filled for every day in the range"""
    date: str
    nodes: List[InternalSquadUserUsageNodeItem]


class GetInternalSquadUserUsageResponseDto(BaseModel):
    """Response for a single user daily usage on the internal squad nodes"""
    days: List[InternalSquadUserUsageDayItem]


# ============ Backwards-compatible aliases (pre-3.0 names) ============

GetStatsNodesUsersUsageRequestDto = GetStatsNodesUsersUsageBodyDto