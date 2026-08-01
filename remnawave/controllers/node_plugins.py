from typing import Annotated, Optional

from rapid_api_client import Path, PydanticBody, Query


from remnawave.models.node_plugins import (
    CloneNodePluginBodyDto,
    CloneNodePluginResponseDto,
    CreateNodePluginBodyDto,
    CreateNodePluginResponseDto,
    GetNodePluginResponseDto,
    GetNodePluginsResponseDto,
    GetTorrentBlockerReportsResponseDto,
    GetTorrentBlockerReportsStatsResponseDto,
    PluginExecutorBodyDto,
    ReorderNodePluginsBodyDto,
    ReorderNodePluginsResponseDto,
    UpdateNodePluginBodyDto,
    UpdateNodePluginResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodePluginsController(BaseController):
    @get("/node-plugins/torrent-blocker", response_class=GetTorrentBlockerReportsResponseDto)
    async def get_torrent_blocker_reports(
        self,
        size: Annotated[
            Optional[int], Query(default=None, ge=1, le=1000, description="Page size, 1..1000")
        ] = None,
        start: Annotated[Optional[int], Query(default=None, ge=0, description="Offset")] = None,
        filters: Annotated[
            Optional[str], Query(default=None, description="JSON array of filters")
        ] = None,
        filter_modes: Annotated[
            Optional[str],
            Query(default=None, alias="filterModes", description="JSON object of filter modes"),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(default=None, alias="globalFilterMode", description="Global filter mode"),
        ] = None,
        sorting: Annotated[
            Optional[str], Query(default=None, description="JSON array of sorting rules")
        ] = None,
    ) -> GetTorrentBlockerReportsResponseDto:
        """Get Torrent Blocker Reports"""
        ...

    @get("/node-plugins/torrent-blocker/stats", response_class=GetTorrentBlockerReportsStatsResponseDto)
    async def get_torrent_blocker_reports_stats(
        self,
    ) -> GetTorrentBlockerReportsStatsResponseDto:
        """Get Torrent Blocker Reports Stats"""
        ...

    @delete("/node-plugins/torrent-blocker/truncate", response_class=None)
    async def truncate_torrent_blocker_reports(
        self,
    ) -> None:
        """Truncate Torrent Blocker Reports (204 No Content)"""
        ...

    @get("/node-plugins", response_class=GetNodePluginsResponseDto)
    async def get_all_node_plugins(self) -> GetNodePluginsResponseDto:
        """Get all Node Plugins"""
        ...

    @patch("/node-plugins", response_class=UpdateNodePluginResponseDto)
    async def update_node_plugin(
        self,
        body: Annotated[UpdateNodePluginBodyDto, PydanticBody()],
    ) -> UpdateNodePluginResponseDto:
        """Update Node Plugin"""
        ...

    @post("/node-plugins", response_class=CreateNodePluginResponseDto)
    async def create_node_plugin(
        self,
        body: Annotated[CreateNodePluginBodyDto, PydanticBody()],
    ) -> CreateNodePluginResponseDto:
        """Create Node Plugin (201 Created)"""
        ...

    @get("/node-plugins/{uuid}", response_class=GetNodePluginResponseDto)
    async def get_node_plugin_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> GetNodePluginResponseDto:
        """Get Node Plugin by uuid"""
        ...

    @delete("/node-plugins/{uuid}", response_class=None)
    async def delete_node_plugin(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> None:
        """Delete Node Plugin (204 No Content)"""
        ...

    @post("/node-plugins/actions/reorder", response_class=ReorderNodePluginsResponseDto)
    async def reorder_node_plugins(
        self,
        body: Annotated[ReorderNodePluginsBodyDto, PydanticBody()],
    ) -> ReorderNodePluginsResponseDto:
        """Reorder Node Plugins"""
        ...

    @post("/node-plugins/actions/clone", response_class=CloneNodePluginResponseDto)
    async def clone_node_plugin(
        self,
        body: Annotated[CloneNodePluginBodyDto, PydanticBody()],
    ) -> CloneNodePluginResponseDto:
        """Clone Node Plugin"""
        ...

    @post("/node-plugins/executor", response_class=None)
    async def plugin_executor(
        self,
        body: Annotated[PluginExecutorBodyDto, PydanticBody()],
    ) -> None:
        """Execute command on node plugins (202 Accepted)"""
        ...
