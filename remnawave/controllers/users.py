from typing import Annotated, Optional, Union

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.enums import TrafficLimitStrategy, UserStatus
from remnawave.models.nodes_usage_history import GetUserAccessibleNodesResponseDto
from remnawave.models.users import (
    CreateUserBodyDto,
    ExtendUserBodyDto,
    GetAllTagsResponseDto,
    GetAllUsersResponseDto,
    GetUserSubscriptionRequestHistoryResponseDto,
    GetUsersStreamResponseDto,
    ResolveUserBodyDto,
    ResolveUserResponseDto,
    RevokeUserBodyDto,
    UpdateUserBodyDto,
    UserResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class UsersController(BaseController):
    @post("/users", response_class=UserResponseDto)
    async def create_user(
        self,
        body: Annotated[CreateUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Create a new user"""
        ...

    @patch("/users", response_class=UserResponseDto)
    async def update_user(
        self,
        body: Annotated[UpdateUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Update a user by ID or username"""
        ...

    @get("/users", response_class=GetAllUsersResponseDto)
    async def get_all_users(
        self,
        start: Annotated[
            Optional[int],
            Query(default=None, description="Offset for pagination (default 0)")
        ] = None,
        size: Annotated[
            Optional[int],
            Query(default=None, description="Page size, 1..1000 (default 25)")
        ] = None,
        filters: Annotated[
            Optional[str],
            Query(
                default=None,
                description='JSON array of filters, e.g. \'[{"id":"username","value":"john"}]\'',
            ),
        ] = None,
        filter_modes: Annotated[
            Optional[str],
            Query(
                default=None,
                alias="filterModes",
                description='JSON object of per-column filter modes, e.g. \'{"username":"contains"}\'',
            ),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(default=None, alias="globalFilterMode", description="Global filter mode"),
        ] = None,
        sorting: Annotated[
            Optional[str],
            Query(
                default=None,
                description='JSON array of sorting rules, e.g. \'[{"id":"createdAt","desc":true}]\'',
            ),
        ] = None,
    ) -> GetAllUsersResponseDto:
        """Get all users using offset-based pagination"""
        ...

    @get("/users/stream", response_class=GetUsersStreamResponseDto)
    async def get_users_stream(
        self,
        size: Annotated[
            Optional[int],
            Query(default=None, description="Page size, 1..1000 (default 250)"),
        ] = None,
        cursor: Annotated[
            Optional[Union[int, str]],
            Query(
                default=None,
                description="Cursor from the previous response (nextCursor). Omit on the first request",
            ),
        ] = None,
        status: Annotated[
            Optional[UserStatus],
            Query(default=None, description="Status to filter users by"),
        ] = None,
        traffic_limit_strategy: Annotated[
            Optional[TrafficLimitStrategy],
            Query(
                default=None,
                alias="trafficLimitStrategy",
                description="Traffic limit strategy to filter users by",
            ),
        ] = None,
        telegram_id: Annotated[
            Optional[int],
            Query(default=None, alias="telegramId", description="Telegram ID to filter users by"),
        ] = None,
        email: Annotated[
            Optional[str],
            Query(default=None, description="Email to filter users by"),
        ] = None,
        tag: Annotated[
            Optional[str],
            Query(default=None, description="Tag to filter users by"),
        ] = None,
        external_squad_uuid: Annotated[
            Optional[str],
            Query(
                default=None,
                alias="externalSquadUuid",
                description="External squad UUID to filter users by",
            ),
        ] = None,
    ) -> GetUsersStreamResponseDto:
        """Get all users using cursor-based (keyset) pagination with filtering options"""
        ...

    @get("/users/tags", response_class=GetAllTagsResponseDto)
    async def get_all_tags(
        self,
    ) -> GetAllTagsResponseDto:
        """Get all existing user tags"""
        ...

    @post("/users/resolve", response_class=ResolveUserResponseDto)
    async def resolve_user(
        self,
        body: Annotated[ResolveUserBodyDto, PydanticBody()],
    ) -> ResolveUserResponseDto:
        """Resolve user by any identifier (id, shortUuid, username)"""
        ...

    @get("/users/by-short-uuid/{shortUuid}", response_class=UserResponseDto)
    async def get_user_by_short_uuid(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
    ) -> UserResponseDto:
        """Get user by Short UUID"""
        ...

    @get("/users/by-username/{username}", response_class=UserResponseDto)
    async def get_user_by_username(
        self,
        username: Annotated[str, Path(description="Username of the user")],
    ) -> UserResponseDto:
        """Get user by username"""
        ...

    @get("/users/{userId}", response_class=UserResponseDto)
    async def get_user_by_id(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> UserResponseDto:
        """Get user by ID"""
        ...

    @delete("/users/{userId}", response_class=None)
    async def delete_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> None:
        """Delete user (204 No Content)"""
        ...

    @get("/users/{userId}/accessible-nodes", response_class=GetUserAccessibleNodesResponseDto)
    async def get_user_accessible_nodes(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserAccessibleNodesResponseDto:
        """Get user accessible nodes"""
        ...

    @get(
        "/users/{userId}/subscription-request-history",
        response_class=GetUserSubscriptionRequestHistoryResponseDto,
    )
    async def get_user_subscription_request_history(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserSubscriptionRequestHistoryResponseDto:
        """Get user subscription request history, recent 24 records"""
        ...

    @post("/users/{userId}/actions/revoke", response_class=UserResponseDto)
    async def revoke_user_subscription(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
        body: Annotated[Optional[RevokeUserBodyDto], PydanticBody()] = None,
    ) -> UserResponseDto:
        """Revoke User Subscription"""
        ...

    @post("/users/{userId}/actions/disable", response_class=UserResponseDto)
    async def disable_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> UserResponseDto:
        """Disable User"""
        ...

    @post("/users/{userId}/actions/enable", response_class=UserResponseDto)
    async def enable_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> UserResponseDto:
        """Enable User"""
        ...

    @post("/users/{userId}/actions/reset-traffic", response_class=UserResponseDto)
    async def reset_user_traffic(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> UserResponseDto:
        """Reset User Traffic"""
        ...

    @post("/users/{userId}/actions/extend", response_class=UserResponseDto)
    async def extend_user_expiration_date(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
        body: Annotated[ExtendUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Extend user expiration date by the given number of days"""
        ...
