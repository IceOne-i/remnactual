from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    BulkNodesActionsBodyDto,
    BulkNodesUpdateBodyDto,
    CreateNodeBodyDto,
    GetNodesResponseDto,
    GetNodesTagsResponseDto,
    NodeResponseDto,
    ProfileModificationBodyDto,
    ReorderNodesBodyDto,
    ReorderNodesResponseDto,
    RestartAllNodesBodyDto,
    RestartNodeBodyDto,
    UpdateNodeBodyDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodesController(BaseController):
    @get("/nodes/tags", response_class=GetNodesTagsResponseDto)
    async def get_all_nodes_tags(
        self,
    ) -> GetNodesTagsResponseDto:
        """Get nodes tags"""
        ...

    @post("/nodes", response_class=NodeResponseDto)
    async def create_node(
        self,
        body: Annotated[CreateNodeBodyDto, PydanticBody()],
    ) -> NodeResponseDto:
        """Create a new node (201)"""
        ...

    @get("/nodes", response_class=GetNodesResponseDto)
    async def get_all_nodes(
        self,
    ) -> GetNodesResponseDto:
        """Get nodes"""
        ...

    @get("/nodes/{uuid}", response_class=NodeResponseDto)
    async def get_one_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Get node by UUID"""
        ...

    @delete("/nodes/{uuid}", response_class=None)
    async def delete_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> None:
        """Delete a node. Отвечает 204 без тела."""
        ...

    @patch("/nodes", response_class=NodeResponseDto)
    async def update_node(
        self,
        body: Annotated[UpdateNodeBodyDto, PydanticBody()],
    ) -> NodeResponseDto:
        """Update node"""
        ...

    @post("/nodes/{uuid}/actions/enable", response_class=NodeResponseDto)
    async def enable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Enable a node"""
        ...

    @post("/nodes/{uuid}/actions/disable", response_class=NodeResponseDto)
    async def disable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Disable a node"""
        ...

    @post("/nodes/{uuid}/actions/restart", response_class=None)
    async def restart_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
        body: Annotated[RestartNodeBodyDto, PydanticBody()] = RestartNodeBodyDto(
            force_restart=False
        ),
    ) -> None:
        """Restart node. `forceRestart` обязателен в теле запроса.
        Отвечает 202 без тела."""
        ...

    @post("/nodes/actions/restart-all", response_class=None)
    async def restart_all_nodes(
        self,
        body: Annotated[RestartAllNodesBodyDto, PydanticBody()],
    ) -> None:
        """Restart all nodes. Отвечает 202 без тела."""
        ...

    @post("/nodes/actions/reorder", response_class=ReorderNodesResponseDto)
    async def reorder_nodes(
        self,
        body: Annotated[ReorderNodesBodyDto, PydanticBody()],
    ) -> ReorderNodesResponseDto:
        """Reorder nodes"""
        ...

    @post("/nodes/{uuid}/actions/reset-traffic", response_class=None)
    async def reset_node_traffic(
        self,
        uuid: Annotated[str, Path(description="UUID of the node")],
    ) -> None:
        """Reset Node Traffic. Отвечает 204 без тела."""
        ...

    @post("/nodes/bulk-actions/profile-modification", response_class=None)
    async def profile_modification(
        self,
        body: Annotated[ProfileModificationBodyDto, PydanticBody()],
    ) -> None:
        """Modify Inbounds & Profile for many nodes. Отвечает 204 без тела."""
        ...

    @post("/nodes/bulk-actions", response_class=None)
    async def nodes_bulk_actions(
        self,
        body: Annotated[BulkNodesActionsBodyDto, PydanticBody()],
    ) -> None:
        """Perform actions for many nodes (ENABLE, DISABLE, RESTART, RESET_TRAFFIC).
        Отвечает 204 без тела."""
        ...

    @post("/nodes/bulk-actions/update", response_class=None)
    async def bulk_nodes_update(
        self,
        body: Annotated[BulkNodesUpdateBodyDto, PydanticBody()],
    ) -> None:
        """Update many nodes. Отвечает 204 без тела."""
        ...
