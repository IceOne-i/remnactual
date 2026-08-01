from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateHostBodyDto,
    GetHostsResponseDto,
    GetHostsTagsResponseDto,
    HostResponseDto,
    ReorderHostsBodyDto,
    ReorderHostsResponseDto,
    UpdateHostBodyDto,
)
from remnawave.rapid import BaseController, delete, get, post, patch


class HostsController(BaseController):
    @post("/hosts", response_class=HostResponseDto)
    async def create_host(
        self,
        body: Annotated[CreateHostBodyDto, PydanticBody()],
    ) -> HostResponseDto:
        """Create Host (201)"""
        ...

    @patch("/hosts", response_class=HostResponseDto)
    async def update_host(
        self,
        body: Annotated[UpdateHostBodyDto, PydanticBody()],
    ) -> HostResponseDto:
        """Update Host"""
        ...

    @get("/hosts", response_class=GetHostsResponseDto)
    async def get_all_hosts(
        self,
    ) -> GetHostsResponseDto:
        """Get All Hosts"""
        ...

    @get("/hosts/tags", response_class=GetHostsTagsResponseDto)
    async def get_hosts_tags(
        self,
    ) -> GetHostsTagsResponseDto:
        """Get Hosts Tags"""
        ...

    @delete("/hosts/{uuid}", response_class=None)
    async def delete_host(
        self,
        uuid: Annotated[str, Path(description="UUID of the host")],
    ) -> None:
        """Delete Host.

        3.0: отвечает ``204 No Content`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @get("/hosts/{uuid}", response_class=HostResponseDto)
    async def get_one_host(
        self,
        uuid: Annotated[str, Path(description="UUID of the host")],
    ) -> HostResponseDto:
        """Get One Host"""
        ...

    @post("/hosts/actions/reorder", response_class=ReorderHostsResponseDto)
    async def reorder_hosts(
        self,
        body: Annotated[ReorderHostsBodyDto, PydanticBody()],
    ) -> ReorderHostsResponseDto:
        """Reorder Hosts"""
        ...
