from typing import Annotated

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models.external_squads import (
    CreateExternalSquadBodyDto,
    CreateExternalSquadResponseDto,
    GetExternalSquadByUuidResponseDto,
    GetExternalSquadsResponseDto,
    ReorderExternalSquadsBodyDto,
    ReorderExternalSquadsResponseDto,
    UpdateExternalSquadBodyDto,
    UpdateExternalSquadResponseDto,
)
from remnawave.models.tags import (
    GetEntityTagsResponseDto,
    SetEntityTagsBodyDto,
    SetEntityTagsResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class ExternalSquadsController(BaseController):
    @get("/external-squads", response_class=GetExternalSquadsResponseDto)
    async def get_external_squads(
        self,
    ) -> GetExternalSquadsResponseDto:
        """Get all external squads"""
        ...

    @post("/external-squads", response_class=CreateExternalSquadResponseDto)
    async def create_external_squad(
        self,
        body: Annotated[CreateExternalSquadBodyDto, PydanticBody()],
    ) -> CreateExternalSquadResponseDto:
        """Create external squad"""
        ...

    @patch("/external-squads", response_class=UpdateExternalSquadResponseDto)
    async def update_external_squad(
        self,
        body: Annotated[UpdateExternalSquadBodyDto, PydanticBody()],
    ) -> UpdateExternalSquadResponseDto:
        """Update external squad"""
        ...

    @get("/external-squads/{uuid}", response_class=GetExternalSquadByUuidResponseDto)
    async def get_external_squad_by_uuid(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the external squad")],
    ) -> GetExternalSquadByUuidResponseDto:
        """Get external squad by uuid"""
        ...

    @delete("/external-squads/{uuid}", response_class=None)
    async def delete_external_squad(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the external squad")],
    ) -> None:
        """Delete external squad (204, без тела)"""
        ...

    @post("/external-squads/{uuid}/bulk-actions/add-users", response_class=None)
    async def add_users_to_external_squad(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the external squad")],
    ) -> None:
        """Add all users to external squad (202, без тела)"""
        ...

    @delete("/external-squads/{uuid}/bulk-actions/remove-users", response_class=None)
    async def remove_users_from_external_squad(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the external squad")],
    ) -> None:
        """Delete users from external squad (202, без тела)"""
        ...

    @post("/external-squads/actions/reorder", response_class=ReorderExternalSquadsResponseDto)
    async def reorder_external_squads(
        self,
        body: Annotated[ReorderExternalSquadsBodyDto, PydanticBody()],
    ) -> ReorderExternalSquadsResponseDto:
        """Reorder external squads"""
        ...

    @get("/external-squads/tags", response_class=GetEntityTagsResponseDto)
    async def get_tags(self) -> GetEntityTagsResponseDto:
        """Get tags of External Squads (панель 3.4.0+)

        Отдаёт ВСЕ метки, встречающиеся у сущностей этого вида, а не метки
        одной из них: у конкретной они лежат в её собственном поле ``tags``.
        """
        ...

    @patch("/external-squads/tags", response_class=SetEntityTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetEntityTagsBodyDto, PydanticBody()],
    ) -> SetEntityTagsResponseDto:
        """Set tags of External Squad (панель 3.4.0+)

        ЗАМЕНЯЕТ набор меток целиком: пустой список снимает все.
        """
        ...
