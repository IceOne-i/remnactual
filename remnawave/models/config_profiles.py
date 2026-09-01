from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class InboundDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")

class NodesProfileDto(BaseModel):
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")

class ConfigProfileDto(BaseModel):
    #: Метки сущности (панель 3.4.0+). До 3.4 поле не приходит и остаётся
    #: пустым — пол панели у форка 3.0.0.
    tags: List[str] = Field(default_factory=list, alias="tags")
    uuid: UUID
    name: str
    view_position: int = Field(alias="viewPosition")
    config: Any
    inbounds: List[InboundDto]
    nodes: List[NodesProfileDto] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateConfigProfileBodyDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    config: Any


class CreateConfigProfileResponseDto(ConfigProfileDto):
    pass


class UpdateConfigProfileBodyDto(BaseModel):
    uuid: UUID
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None
    config: Optional[Dict[str, Any]] = None


class UpdateConfigProfileResponseDto(ConfigProfileDto):
    pass


class GetAllConfigProfilesResponsePaginated(BaseModel):
    total: float
    config_profiles: List[ConfigProfileDto] = Field(alias="configProfiles")


class GetConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass


class GetConfigProfileByUuidResponseDto(ConfigProfileDto):
    pass


class GetComputedConfigProfileByUuidResponseDto(ConfigProfileDto):
    pass


# 3.0: DELETE /api/config-profiles/{uuid} отвечает 204 без тела —
# DeleteConfigProfileResponseDto удалён.


# GetAllInboundsResponseDto / GetInboundsByProfileUuidResponseDto живут в
# remnawave.models.inbounds — обе ручки отдают {total, inbounds[]}, а не голый список.


class ReorderConfigProfileItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_position: int = Field(alias="viewPosition")
    uuid: UUID


class ReorderConfigProfilesBodyDto(BaseModel):
    items: List[ReorderConfigProfileItem]


class ReorderConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# 3.0 переименовал тела запросов в *BodyDto, а список профилей — в
# GetConfigProfilesResponseDto. Старые имена сохранены как алиасы.
CreateConfigProfileRequestDto = CreateConfigProfileBodyDto
UpdateConfigProfileRequestDto = UpdateConfigProfileBodyDto
ReorderConfigProfilesRequestDto = ReorderConfigProfilesBodyDto
GetAllConfigProfilesResponseDto = GetConfigProfilesResponseDto
