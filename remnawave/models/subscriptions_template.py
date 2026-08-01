from typing import Annotated, Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.enums import TemplateType


class TemplateResponseDto(BaseModel):
    uuid: UUID
    name: str
    view_position: int = Field(alias="viewPosition")
    template_type: TemplateType = Field(alias="templateType")
    template_json: Any | None = Field(alias="templateJson")
    encoded_template_yaml: str | None = Field(alias="encodedTemplateYaml")


class TemplateInfoDto(BaseModel):
    """Template entry as returned by list endpoints.

    Контракт 3.0 отдаёт в списках полную ``SubscriptionTemplateSchema``, поэтому
    ``templateJson`` / ``encodedTemplateYaml`` здесь тоже могут прийти; они
    объявлены необязательными для совместимости.
    """
    uuid: UUID
    name: str
    view_position: int = Field(alias="viewPosition")
    template_type: TemplateType = Field(alias="templateType")
    template_json: Optional[Any] = Field(None, alias="templateJson")
    encoded_template_yaml: Optional[str] = Field(None, alias="encodedTemplateYaml")


class GetTemplateResponseDto(TemplateResponseDto):
    pass

class GetTemplatesData(BaseModel):
    total: float
    templates: List[TemplateInfoDto]

class GetTemplatesResponseDto(GetTemplatesData):
    pass


class CreateSubscriptionTemplateBodyDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]
    template_type: TemplateType = Field(serialization_alias="templateType")


class CreateSubscriptionTemplateResponseDto(TemplateResponseDto):
    pass


class UpdateTemplateBodyDto(BaseModel):
    uuid: UUID
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None
    template_json: Optional[dict] = Field(None, serialization_alias="templateJson")
    encoded_template_yaml: Optional[str] = Field(
        None, serialization_alias="encodedTemplateYaml"
    )


class UpdateTemplateResponseDto(TemplateResponseDto):
    pass


class ReorderTemplateItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderSubscriptionTemplatesBodyDto(BaseModel):
    items: List[ReorderTemplateItem]


class ReorderSubscriptionTemplatesResponseDto(GetTemplatesData):
    pass


# Backward compatibility aliases
CreateSubscriptionTemplateRequestDto = CreateSubscriptionTemplateBodyDto
UpdateTemplateRequestDto = UpdateTemplateBodyDto
ReorderSubscriptionTemplatesRequestDto = ReorderSubscriptionTemplatesBodyDto