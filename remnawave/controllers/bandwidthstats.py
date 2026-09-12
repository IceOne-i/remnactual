from typing import Annotated, Optional

from pydantic import Field
from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models.bandwidthstats import (
    GetInternalSquadUsageResponseDto,
    GetInternalSquadUserUsageResponseDto,
    GetNodeUsageBodyDto,
    GetNodeUsageResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsNodesUsersUsageBodyDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
)
from remnawave.rapid import BaseController, get, post


class BandWidthStatsController(BaseController):
    # ============ Stats Endpoints ============

    @get("/bandwidth-stats/nodes/{uuid}/users", response_class=GetStatsNodeUsersUsageResponseDto)
    async def get_stats_node_users_usage(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the node")],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        top_users_limit: Annotated[
            Optional[int],
            Query(alias="topUsersLimit"), Field(default=None, ge=1, description="Limit of top users to return (server default 100)"),
        ] = None,
    ) -> GetStatsNodeUsersUsageResponseDto:
        """Get Node Users Usage by Node UUID"""
        ...

    @post("/bandwidth-stats/nodes/users", response_class=GetStatsNodesUsersUsageResponseDto)
    async def get_stats_nodes_users_usage(
        self,
        body: Annotated[GetStatsNodesUsersUsageBodyDto, PydanticBody()],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        top_users_limit: Annotated[
            Optional[int],
            Query(alias="topUsersLimit"), Field(default=None, ge=1, description="Limit of top users to return (server default 100)"),
        ] = None,
    ) -> GetStatsNodesUsersUsageResponseDto:
        """Get Nodes Users Usage by Nodes UUIDs"""
        ...

    @post("/bandwidth-stats/nodes/usage", response_class=GetNodeUsageResponseDto)
    async def get_node_usage(
        self,
        body: Annotated[GetNodeUsageBodyDto, PydanticBody()],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        min_total_bytes: Annotated[
            Optional[int],
            Query(alias="minTotalBytes"), Field(default=None, ge=0, description="Only include users whose total usage over the period is >= this "
                              "(bytes, server default 0)"),
        ] = None,
    ) -> GetNodeUsageResponseDto:
        """Get users exceeding a traffic threshold on the given nodes for a period"""
        ...

    @get("/bandwidth-stats/users/{userId}", response_class=GetStatsUserUsageResponseDto)
    async def get_stats_user_usage(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="ID of the user")],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        top_nodes_limit: Annotated[
            Optional[int],
            Query(alias="topNodesLimit"), Field(default=None, ge=1, description="Limit of top nodes to return (server default 20)"),
        ] = None,
    ) -> GetStatsUserUsageResponseDto:
        """Get User Usage by Range"""
        ...

    @get("/bandwidth-stats/nodes", response_class=GetStatsNodesUsageResponseDto)
    async def get_stats_nodes_usage(
        self,
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        top_nodes_limit: Annotated[
            Optional[int],
            Query(alias="topNodesLimit"), Field(default=None, ge=1, description="Limit of top nodes to return (server default 20)"),
        ] = None,
    ) -> GetStatsNodesUsageResponseDto:
        """Get Nodes Usage by Range"""
        ...

    # ============ Internal Squads Endpoints ============

    @get(
        "/bandwidth-stats/internal-squads/{squadUuid}/usage",
        response_class=GetInternalSquadUsageResponseDto,
    )
    async def get_internal_squad_usage(
        self,
        squad_uuid: Annotated[str, Path(alias="squadUuid"), Field(description="Internal squad UUID")],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
        min_total_bytes: Annotated[
            Optional[int],
            Query(alias="minTotalBytes"), Field(default=None, ge=0, description="Only include users whose total usage over the period is >= this "
                              "(bytes, server default 0)"),
        ] = None,
        limit: Annotated[
            Optional[int],
            Query(), Field(default=None, ge=1, le=1000, description="Number of users to return, no more than 1000 (server default 250)"),
        ] = None,
        cursor: Annotated[
            Optional[int],
            Query(), Field(default=None, description="Pass the nextCursor from the previous response. "
                              "Omit on the first request."),
        ] = None,
    ) -> GetInternalSquadUsageResponseDto:
        """Get internal squad users traffic usage for a period"""
        ...

    @get(
        "/bandwidth-stats/internal-squads/{squadUuid}/users/{userId}/usage",
        response_class=GetInternalSquadUserUsageResponseDto,
    )
    async def get_internal_squad_user_usage(
        self,
        squad_uuid: Annotated[str, Path(alias="squadUuid"), Field(description="Internal squad UUID")],
        user_id: Annotated[int, Path(alias="userId"), Field(description="ID of the user")],
        start: Annotated[str, Query(), Field(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(), Field(description="End date (YYYY-MM-DD)")],
    ) -> GetInternalSquadUserUsageResponseDto:
        """Get a single user daily traffic usage on the internal squad nodes for a period"""
        ...
