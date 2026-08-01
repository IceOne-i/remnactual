from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field

from remnawave.models._serialization import AlwaysEmitModel


# ─────────────────────────────────────────────────────────────────────────────
# Connections by user – step 1: start the job
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionsByUserJobData(BaseModel):
    """Returned job ID after requesting the connections of a user"""
    job_id: str = Field(alias="jobId")


class ConnectionsByUserResponseDto(ConnectionsByUserJobData):
    """Response for POST /api/connections/by-user/{userId}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Connections by user – step 2: poll the job result
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionsProgressData(BaseModel):
    """Progress information for a connections job"""
    total: int
    completed: int
    percent: float


class IpEntry(BaseModel):
    """IP-адрес с меткой последнего появления"""
    ip: str
    last_seen: datetime = Field(alias="lastSeen")


class ConnectionsByUserNodeResult(BaseModel):
    """Per-node IP list for a user"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    ips: List[IpEntry]


class ConnectionsByUserResult(BaseModel):
    """Full result payload when the job is completed"""
    success: bool
    user_id: int = Field(alias="userId")
    nodes: List[ConnectionsByUserNodeResult]


class ConnectionsByUserResultData(BaseModel):
    """Job state + optional result"""
    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    progress: ConnectionsProgressData
    result: Optional[ConnectionsByUserResult] = None


class ConnectionsByUserResultResponseDto(ConnectionsByUserResultData):
    """Response for GET /api/connections/by-user/{jobId}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Drop Connections request – discriminated unions for dropBy / targetNodes
# ─────────────────────────────────────────────────────────────────────────────

class DropByUserIds(AlwaysEmitModel):
    """Drop connections for specific user IDs"""
    __always_emit__ = ("by",)

    by: Literal["userIds"] = "userIds"
    user_ids: List[int] = Field(
        ...,
        serialization_alias="userIds",
        min_length=1,
        description="List of user IDs whose connections should be dropped",
    )


class DropByIpAddresses(AlwaysEmitModel):
    """Drop connections from specific IP addresses"""
    __always_emit__ = ("by",)

    by: Literal["ipAddresses"] = "ipAddresses"
    ip_addresses: List[str] = Field(
        ...,
        serialization_alias="ipAddresses",
        min_length=1,
        description="List of IP addresses (IPv4 or IPv6) to disconnect",
    )


# Discriminated union – use `by` field as the discriminator
DropBy = Annotated[
    Union[DropByUserIds, DropByIpAddresses],
    Field(discriminator="by"),
]


class TargetAllNodes(AlwaysEmitModel):
    """Send the drop-connections event to all connected nodes"""
    __always_emit__ = ("target",)

    target: Literal["allNodes"] = "allNodes"


class TargetSpecificNodes(AlwaysEmitModel):
    """Send the drop-connections event to specific nodes only"""
    __always_emit__ = ("target",)

    target: Literal["specificNodes"] = "specificNodes"
    node_uuids: List[UUID] = Field(
        ...,
        serialization_alias="nodeUuids",
        min_length=1,
        description="List of node UUIDs to target",
    )


# Discriminated union – use `target` field as the discriminator
TargetNodes = Annotated[
    Union[TargetAllNodes, TargetSpecificNodes],
    Field(discriminator="target"),
]


class DropConnectionsBodyDto(BaseModel):
    """Request body for POST /api/connections/drop"""
    drop_by: DropBy = Field(
        ...,
        serialization_alias="dropBy",
        description="Selector for whose connections to drop",
    )
    target_nodes: TargetNodes = Field(
        ...,
        serialization_alias="targetNodes",
        description="Selector for which nodes to send the drop event to",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Connections by node – step 1: start the job
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionsByNodeJobData(BaseModel):
    """Returned job ID after requesting the connections of a node"""
    job_id: str = Field(alias="jobId")


class ConnectionsByNodeResponseDto(ConnectionsByNodeJobData):
    """Response for POST /api/connections/by-node/{nodeUuid}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Connections by node – step 2: poll the job result
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionsByNodeUserIp(BaseModel):
    """IP entry with last seen timestamp"""
    ip: str
    last_seen: datetime = Field(alias="lastSeen")


class ConnectionsByNodeUser(BaseModel):
    """Per-user IP list"""
    user_id: int = Field(alias="userId")
    ips: List[ConnectionsByNodeUserIp]


class ConnectionsByNodeResult(BaseModel):
    """Full result payload when the job is completed"""
    success: bool
    node_uuid: UUID = Field(alias="nodeUuid")
    users: List[ConnectionsByNodeUser]


class ConnectionsByNodeResultData(BaseModel):
    """Job state + optional result"""
    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    result: Optional[ConnectionsByNodeResult] = None


class ConnectionsByNodeResultResponseDto(ConnectionsByNodeResultData):
    """Response for GET /api/connections/by-node/{jobId}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Обратная совместимость: старые имена (2.8, /api/ip-control) — алиасы
# ─────────────────────────────────────────────────────────────────────────────

FetchIpsJobData = ConnectionsByUserJobData
FetchIpsResponseDto = ConnectionsByUserResponseDto
FetchIpsProgressData = ConnectionsProgressData
FetchIpsNodeResult = ConnectionsByUserNodeResult
FetchIpsResult = ConnectionsByUserResult
FetchIpsResultData = ConnectionsByUserResultData
FetchIpsResultResponseDto = ConnectionsByUserResultResponseDto

FetchUsersIpsJobData = ConnectionsByNodeJobData
FetchUsersIpsResponseDto = ConnectionsByNodeResponseDto
FetchUsersIpsUserIp = ConnectionsByNodeUserIp
FetchUsersIpsUser = ConnectionsByNodeUser
FetchUsersIpsResult = ConnectionsByNodeResult
FetchUsersIpsResultData = ConnectionsByNodeResultData
FetchUsersIpsResultResponseDto = ConnectionsByNodeResultResponseDto

# ВНИМАНИЕ: тело запроса изменилось — `userUuids` (UUID) → `userIds` (числа).
DropByUserUuids = DropByUserIds
DropConnectionsRequestDto = DropConnectionsBodyDto
