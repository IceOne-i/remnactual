from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models.internal_squads import (
    AddManyUsersToInternalSquadBodyDto,
    CreateInternalSquadBodyDto,
    CreateInternalSquadResponseDto,
    DeleteManyUsersFromInternalSquadBodyDto,
    GetInternalSquadAccessibleNodesResponseDto,
    GetInternalSquadResponseDto,
    GetInternalSquadsResponseDto,
    ReorderInternalSquadsBodyDto,
    ReorderInternalSquadsResponseDto,
    UpdateInternalSquadBodyDto,
    UpdateInternalSquadResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class InternalSquadsController(BaseController):
    @get("/internal-squads", response_class=GetInternalSquadsResponseDto)
    async def get_internal_squads(self) -> GetInternalSquadsResponseDto:
        """Get all internal squads"""
        ...

    @post("/internal-squads", response_class=CreateInternalSquadResponseDto)
    async def create_internal_squad(
        self,
        body: Annotated[CreateInternalSquadBodyDto, PydanticBody()],
    ) -> CreateInternalSquadResponseDto:
        """Create internal squad"""
        ...

    @patch("/internal-squads", response_class=UpdateInternalSquadResponseDto)
    async def update_internal_squad(
        self,
        body: Annotated[UpdateInternalSquadBodyDto, PydanticBody()],
    ) -> UpdateInternalSquadResponseDto:
        """Update internal squad"""
        ...

    @get("/internal-squads/{uuid}", response_class=GetInternalSquadResponseDto)
    async def get_internal_squad_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> GetInternalSquadResponseDto:
        """Get internal squad by uuid"""
        ...

    @delete("/internal-squads/{uuid}", response_class=None)
    async def delete_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> None:
        """Delete internal squad (204, без тела)"""
        ...

    @post("/internal-squads/{uuid}/bulk-actions/add-users", response_class=None)
    async def add_users_to_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> None:
        """Add all users to internal squad (202, без тела)"""
        ...

    @post("/internal-squads/{uuid}/bulk-actions/add-many-users", response_class=None)
    async def add_many_users_to_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        body: Annotated[AddManyUsersToInternalSquadBodyDto, PydanticBody()],
    ) -> None:
        """Add many users to internal squad by user ids (202, без тела)"""
        ...

    @delete("/internal-squads/{uuid}/bulk-actions/remove-users", response_class=None)
    async def remove_users_from_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> None:
        """Delete users from internal squad (202, без тела)"""
        ...

    @delete("/internal-squads/{uuid}/bulk-actions/remove-many-users", response_class=None)
    async def remove_many_users_from_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        body: Annotated[DeleteManyUsersFromInternalSquadBodyDto, PydanticBody()],
    ) -> None:
        """Delete many users from internal squad by user ids (202, без тела)"""
        ...

    @get(
        "/internal-squads/{uuid}/accessible-nodes",
        response_class=GetInternalSquadAccessibleNodesResponseDto,
    )
    async def get_accessible_nodes(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> GetInternalSquadAccessibleNodesResponseDto:
        """Get accessible nodes for internal squad"""
        ...

    # GET /bandwidth-stats/internal-squads/{uuid}/usage живёт под префиксом
    # /bandwidth-stats — см. BandWidthStatsController.get_internal_squad_usage.

    @post("/internal-squads/actions/reorder", response_class=ReorderInternalSquadsResponseDto)
    async def reorder_internal_squads(
        self,
        body: Annotated[ReorderInternalSquadsBodyDto, PydanticBody()],
    ) -> ReorderInternalSquadsResponseDto:
        """Reorder internal squads"""
        ...
