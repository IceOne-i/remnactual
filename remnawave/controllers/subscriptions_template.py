from typing import Annotated

from rapid_api_client.annotations import Path, PydanticBody

from remnawave.models import (
    CreateSubscriptionTemplateBodyDto,
    CreateSubscriptionTemplateResponseDto,
    GetTemplateResponseDto,
    GetTemplatesResponseDto,
    ReorderSubscriptionTemplatesBodyDto,
    ReorderSubscriptionTemplatesResponseDto,
    UpdateTemplateBodyDto,
    UpdateTemplateResponseDto,
)
from remnawave.models.tags import (
    GetEntityTagsResponseDto,
    SetEntityTagsBodyDto,
    SetEntityTagsResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class SubscriptionsTemplateController(BaseController):
    @get("/subscription-templates", response_class=GetTemplatesResponseDto)
    async def get_all_templates(self) -> GetTemplatesResponseDto:
        """Get all subscription templates (without content)"""
        ...

    @post("/subscription-templates", response_class=CreateSubscriptionTemplateResponseDto)
    async def create_template(
        self,
        body: Annotated[CreateSubscriptionTemplateBodyDto, PydanticBody()],
    ) -> CreateSubscriptionTemplateResponseDto:
        """Create subscription template.

        3.0: отвечает 201 Created, тело ответа сохранено.
        """
        ...

    @patch("/subscription-templates", response_class=UpdateTemplateResponseDto)
    async def update_template(
        self,
        body: Annotated[UpdateTemplateBodyDto, PydanticBody()],
    ) -> UpdateTemplateResponseDto:
        """Update subscription template"""
        ...

    @get("/subscription-templates/{uuid}", response_class=GetTemplateResponseDto)
    async def get_template_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Template UUID")],
    ) -> GetTemplateResponseDto:
        """Get subscription template by uuid"""
        ...

    @delete("/subscription-templates/{uuid}", response_class=None)
    async def delete_template(
        self,
        uuid: Annotated[str, Path(description="Template UUID")],
    ) -> None:
        """Delete subscription template.

        3.0: отвечает 204 No Content без тела, поэтому метод возвращает ``None``.
        """
        ...

    @post(
        "/subscription-templates/actions/reorder",
        response_class=ReorderSubscriptionTemplatesResponseDto,
    )
    async def reorder_templates(
        self,
        body: Annotated[ReorderSubscriptionTemplatesBodyDto, PydanticBody()],
    ) -> ReorderSubscriptionTemplatesResponseDto:
        """Reorder subscription templates"""
        ...

    @get("/subscription-templates/tags", response_class=GetEntityTagsResponseDto)
    async def get_tags(self) -> GetEntityTagsResponseDto:
        """Get tags of Subscription Templates (панель 3.4.0+)

        Отдаёт ВСЕ метки, встречающиеся у сущностей этого вида, а не метки
        одной из них: у конкретной они лежат в её собственном поле ``tags``.
        """
        ...

    @patch("/subscription-templates/tags", response_class=SetEntityTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetEntityTagsBodyDto, PydanticBody()],
    ) -> SetEntityTagsResponseDto:
        """Set tags of Subscription Template (панель 3.4.0+)

        ЗАМЕНЯЕТ набор меток целиком: пустой список снимает все.
        """
        ...
