from datetime import datetime
from typing import Any, Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models._serialization import AlwaysEmitModel


class InboundsDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")


class InfoDto(BaseModel):
    members_count: float = Field(alias="membersCount")
    inbounds_count: float = Field(alias="inboundsCount")


class InternalSquadDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    info: Optional[InfoDto] = Field(default=None)
    inbounds: List[InboundsDto] = Field(default_factory=list)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateInternalSquadBodyDto(AlwaysEmitModel):
    # `inbounds` обязателен в контракте, поэтому ключ уходит всегда
    __always_emit__ = ("inbounds",)

    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    inbounds: List[UUID] = Field(default_factory=list)


class CreateInternalSquadResponseDto(InternalSquadDto):
    pass


class UpdateInternalSquadBodyDto(BaseModel):
    uuid: UUID
    # `inbounds` опционален: если ключ отправлен, бэкенд ЗАМЕНЯЕТ набор inbound'ов,
    # поэтому пустой список стирает их все. Не отправляем, если вызывающий не задал.
    inbounds: Optional[List[UUID]] = None
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None


class UpdateInternalSquadResponseDto(InternalSquadDto):
    pass


class GetInternalSquadsResponse(BaseModel):
    total: float
    internal_squads: List[InternalSquadDto] = Field(alias="internalSquads")


class GetInternalSquadsResponseDto(GetInternalSquadsResponse):
    pass


class GetInternalSquadResponseDto(InternalSquadDto):
    pass


class AddManyUsersToInternalSquadBodyDto(BaseModel):
    """Тело POST /internal-squads/{uuid}/bulk-actions/add-many-users (3.0)."""
    model_config = ConfigDict(populate_by_name=True)

    user_ids: List[int] = Field(alias="userIds", min_length=1, max_length=1000)


class DeleteManyUsersFromInternalSquadBodyDto(BaseModel):
    """Тело DELETE /internal-squads/{uuid}/bulk-actions/remove-many-users (3.0)."""
    model_config = ConfigDict(populate_by_name=True)

    user_ids: List[int] = Field(alias="userIds", min_length=1, max_length=1000)


class AccessibleNodeDto(BaseModel):
    uuid: UUID
    name: str = Field(alias="nodeName")
    country_code: Optional[str] = Field(default=None, alias="countryCode")
    config_profile_uuid: Optional[UUID] = Field(default=None, alias="configProfileUuid")
    config_profile_name: Optional[str] = Field(default=None, alias="configProfileName")
    # activeInbounds — список ТЕГОВ inbound'ов (строки), а не UUID
    active_inbounds: List[str] = Field(default_factory=list, alias="activeInbounds")


class GetInternalSquadAccessibleNodesResponseDto(BaseModel):
    squad_uuid: UUID = Field(alias="squadUuid")
    accessible_nodes: List[AccessibleNodeDto] = Field(alias="accessibleNodes")


# Трафик внутреннего сквада (GET /bandwidth-stats/internal-squads/{uuid}/usage)
# живёт под префиксом /bandwidth-stats и описан в remnawave/models/bandwidthstats.py.


class ReorderInternalSquadItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderInternalSquadsBodyDto(BaseModel):
    items: List[ReorderInternalSquadItem]


class ReorderInternalSquadsResponseDto(GetInternalSquadsResponse):
    pass


# --- Совместимость с именами 2.8 ------------------------------------------------
CreateInternalSquadRequestDto = CreateInternalSquadBodyDto
UpdateInternalSquadRequestDto = UpdateInternalSquadBodyDto
ReorderInternalSquadsRequestDto = ReorderInternalSquadsBodyDto
GetAllInternalSquadsResponse = GetInternalSquadsResponse
GetAllInternalSquadsResponseDto = GetInternalSquadsResponseDto
GetInternalSquadByUuidResponseDto = GetInternalSquadResponseDto
