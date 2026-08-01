from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from remnawave.enums import TemplateType
from remnawave.models.subscriptions_settings import CustomRemarksDto, HwidSettingsDto


class ExternalSquadInfoDto(BaseModel):
    """External squad info"""
    members_count: float = Field(alias="membersCount")


class ExternalSquadTemplateDto(BaseModel):
    """External squad template"""
    model_config = ConfigDict(populate_by_name=True)

    template_uuid: UUID = Field(alias="templateUuid")
    template_type: TemplateType = Field(alias="templateType")


class ExternalSquadSubscriptionSettingsDto(BaseModel):
    """External squad subscription settings.

    3.0: контракт оставил только три ключа. `profileTitle`, `supportLink`,
    `profileUpdateInterval`, `isProfileWebpageUrlEnabled`, `happAnnounce` и `happRouting`
    переехали в кастомные заголовки ответа подписки и здесь больше не принимаются.
    """
    model_config = ConfigDict(populate_by_name=True)

    serve_json_at_base_subscription: Optional[bool] = Field(None, alias="serveJsonAtBaseSubscription")
    is_show_custom_remarks: Optional[bool] = Field(None, alias="isShowCustomRemarks")
    randomize_hosts: Optional[bool] = Field(None, alias="randomizeHosts")


class ExternalSquadHostOverridesDto(BaseModel):
    """External squad host overrides"""
    model_config = ConfigDict(populate_by_name=True)

    server_description: Optional[str] = Field(None, alias="serverDescription", max_length=30)
    vless_route_id: Optional[int] = Field(None, alias="vlessRouteId", ge=0, le=65535)


class ExternalSquadDto(BaseModel):
    """External squad data model"""
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    info: ExternalSquadInfoDto
    templates: List[ExternalSquadTemplateDto]
    subscription_settings: Optional[ExternalSquadSubscriptionSettingsDto] = Field(None, alias="subscriptionSettings")
    host_overrides: Optional[ExternalSquadHostOverridesDto] = Field(None, alias="hostOverrides")
    # 3.0: единый `responseHeaders` разделён на добавляемые и удаляемые заголовки
    response_headers_add: Dict[str, str] = Field(default_factory=dict, alias="responseHeadersAdd")
    response_headers_remove: List[str] = Field(default_factory=list, alias="responseHeadersRemove")
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    custom_remarks: Optional[CustomRemarksDto] = Field(None, alias="customRemarks")
    subpage_config_uuid: Optional[UUID] = Field(None, alias="subpageConfigUuid")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


# Request/Response models
class GetExternalSquadsResponseDto(BaseModel):
    """Response with all external squads"""
    total: float = Field(alias="total")
    external_squads: List[ExternalSquadDto] = Field(alias="externalSquads")


class GetExternalSquadByUuidResponseDto(ExternalSquadDto):
    """Response with external squad by UUID"""
    pass


class CreateExternalSquadBodyDto(BaseModel):
    """Request to create external squad"""
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")


class CreateExternalSquadResponseDto(ExternalSquadDto):
    """Response after creating external squad"""
    pass


class UpdateExternalSquadBodyDto(BaseModel):
    """Request to update external squad"""
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Optional[str] = Field(None, min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")
    templates: Optional[List[ExternalSquadTemplateDto]] = None
    subscription_settings: Optional[ExternalSquadSubscriptionSettingsDto] = Field(None, alias="subscriptionSettings")
    host_overrides: Optional[ExternalSquadHostOverridesDto] = Field(None, alias="hostOverrides")
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    custom_remarks: Optional[CustomRemarksDto] = Field(None, alias="customRemarks")
    # 3.0: `responseHeaders` заменён парой add/remove
    response_headers_add: Optional[Dict[str, str]] = Field(None, alias="responseHeadersAdd")
    response_headers_remove: Optional[List[str]] = Field(None, alias="responseHeadersRemove")
    subpage_config_uuid: Optional[UUID] = Field(None, alias="subpageConfigUuid")


class UpdateExternalSquadResponseDto(ExternalSquadDto):
    """Response after updating external squad"""
    pass


class ReorderExternalSquadItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderExternalSquadsBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: List[ReorderExternalSquadItem]


class ReorderExternalSquadsResponseDto(BaseModel):
    """Response after reordering external squads"""
    total: float = Field(alias="total")
    external_squads: List[ExternalSquadDto] = Field(alias="externalSquads")


# --- Совместимость с именами 2.8 ------------------------------------------------
CreateExternalSquadRequestDto = CreateExternalSquadBodyDto
UpdateExternalSquadRequestDto = UpdateExternalSquadBodyDto
ReorderExternalSquadsRequestDto = ReorderExternalSquadsBodyDto
