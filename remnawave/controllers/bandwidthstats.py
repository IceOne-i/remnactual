from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models.bandwidthstats import (
    GetLegacyStatsNodesUsersUsageResponseDto,
    GetLegacyStatsUserUsageResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsNodesUsersUsageRequestDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
)
from remnawave.rapid import BaseController, get, post


class BandWidthStatsController(BaseController):
    # ============ Stats Endpoints ============

    @get("/bandwidth-stats/nodes/{uuid}/users/legacy", response_class=GetLegacyStatsNodesUsersUsageResponseDto)
    async def get_node_users_usage_legacy_stats(
        self,
        uuid: Annotated[str, Path(description="UUID of the node")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetLegacyStatsNodesUsersUsageResponseDto:
        """Get Node Users Usage by Range and Node UUID (Legacy Stats)"""
        ...

    @get("/bandwidth-stats/nodes/{uuid}/users", response_class=GetStatsNodeUsersUsageResponseDto)
    async def get_stats_node_users_usage(
        self,
        uuid: Annotated[str, Path(description="UUID of the node")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_users_limit: Annotated[
            Optional[int],
            Query(default=None, ge=1, alias="topUsersLimit",
                  description="Limit of top users to return (server default 100)"),
        ] = None,
    ) -> GetStatsNodeUsersUsageResponseDto:
        """Get Node Users Usage by Node UUID"""
        ...

    @post("/bandwidth-stats/nodes/users", response_class=GetStatsNodesUsersUsageResponseDto)
    async def get_stats_nodes_users_usage(
        self,
        body: Annotated[GetStatsNodesUsersUsageRequestDto, PydanticBody()],
        start: Annotated[str, Query(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(description="End date (YYYY-MM-DD)")],
        top_users_limit: Annotated[
            Optional[int],
            Query(default=None, ge=1, alias="topUsersLimit",
                  description="Limit of top users to return (server default 100)"),
        ] = None,
    ) -> GetStatsNodesUsersUsageResponseDto:
        """Get Nodes Users Usage by Nodes UUIDs"""
        ...

    @get("/bandwidth-stats/users/{uuid}", response_class=GetStatsUserUsageResponseDto)
    async def get_stats_user_usage(
        self,
        uuid: Annotated[str, Path(description="UUID of the user")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_nodes_limit: Annotated[
            Optional[int],
            Query(default=None, ge=1, alias="topNodesLimit",
                  description="Limit of top nodes to return (server default 20)"),
        ] = None,
    ) -> GetStatsUserUsageResponseDto:
        """Get User Usage by Range"""
        ...

    @get("/bandwidth-stats/nodes", response_class=GetStatsNodesUsageResponseDto)
    async def get_stats_nodes_usage(
        self,
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_nodes_limit: Annotated[
            Optional[int],
            Query(default=None, ge=1, alias="topNodesLimit",
                  description="Limit of top nodes to return (server default 20)"),
        ] = None,
    ) -> GetStatsNodesUsageResponseDto:
        """Get Nodes Usage by Range"""
        ...

    @get("/bandwidth-stats/users/{uuid}/legacy", response_class=GetLegacyStatsUserUsageResponseDto)
    async def get_user_usage_legacy_stats(
        self,
        uuid: Annotated[str, Path(description="UUID of the user")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetLegacyStatsUserUsageResponseDto:
        """Get User Usage by Range (Legacy Stats)"""
        ...