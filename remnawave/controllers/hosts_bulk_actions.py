from typing import Annotated, List
from uuid import UUID

from rapid_api_client import PydanticBody

from remnawave.models import UpdateManyHostsBodyDto
from remnawave.rapid import AttributeBody, BaseController, patch, post


class HostsBulkActionsController(BaseController):
    """Все четыре bulk-эндпоинта в 3.0 отвечают ``204 No Content`` с пустым телом."""

    @post("/hosts/bulk/delete", response_class=None)
    async def delete_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Delete many hosts (204)"""
        ...

    @post("/hosts/bulk/disable", response_class=None)
    async def disable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Disable many hosts (204)"""
        ...

    @post("/hosts/bulk/enable", response_class=None)
    async def enable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Enable many hosts (204)"""
        ...

    @patch("/hosts/bulk/update", response_class=None)
    async def update_hosts(
        self,
        body: Annotated[UpdateManyHostsBodyDto, PydanticBody()],
    ) -> None:
        """Update many hosts (204)"""
        ...
