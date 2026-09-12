from typing import Annotated

from pydantic import Field
from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models.subscription import (
    GetAllSubscriptionsResponseDto,
    GetConnectionKeysByUserIdResponseDto,
    GetRawSubscriptionByShortUuidResponseDto,
    GetSubscriptionByIdResponseDto,
    GetSubscriptionByShortUuidProtectedResponseDto,
    GetSubscriptionByUsernameResponseDto,
)
from remnawave.models.subscription_page import (
    GetSubpageConfigByShortUuidRequestBodyDto,
    GetSubpageConfigByShortUuidResponseDto,
)
from remnawave.rapid import BaseController, get


class SubscriptionsController(BaseController):
    # Protected endpoints below
    @get("/subscriptions", response_class=GetAllSubscriptionsResponseDto)
    async def get_all_subscriptions(
        self,
        start: Annotated[
            int, Query(), Field(default=0, ge=0, description="Index to start pagination from")
        ],
        size: Annotated[
            int,
            Query(), Field(default=25, ge=1, le=500, description="Number of subscriptions, no more than 500"),
        ],
    ) -> GetAllSubscriptionsResponseDto:
        """None"""
        ...

    @get("/subscriptions/by-username/{username}", response_class=GetSubscriptionByUsernameResponseDto)
    async def get_subscription_by_username(
        self,
        username: Annotated[str, Path(), Field(description="Username of the user")],
    ) -> GetSubscriptionByUsernameResponseDto:
        """None"""
        ...

    @get("/subscriptions/by-short-uuid/{shortUuid}", response_class=GetSubscriptionByShortUuidProtectedResponseDto)
    async def get_subscription_by_short_uuid(
        self,
        short_uuid: Annotated[str, Path(alias="shortUuid"), Field(description="Short UUID of the subscription")],
    ) -> GetSubscriptionByShortUuidProtectedResponseDto:
        """None"""
        ...

    @get("/subscriptions/by-id/{userId}", response_class=GetSubscriptionByIdResponseDto)
    async def get_subscription_by_id(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="User ID")],
    ) -> GetSubscriptionByIdResponseDto:
        """Get subscription by User ID"""
        ...

    @get("/subscriptions/subpage-config/{shortUuid}", response_class=GetSubpageConfigByShortUuidResponseDto)
    async def get_subpage_config(
        self,
        short_uuid: Annotated[str, Path(alias="shortUuid"), Field(description="Short UUID of the subscription")],
        body: Annotated[GetSubpageConfigByShortUuidRequestBodyDto, PydanticBody()],
    ) -> GetSubpageConfigByShortUuidResponseDto:
        """Get subscription page config by short UUID"""
        ...

    @get("/subscriptions/by-short-uuid/{shortUuid}/raw", response_class=GetRawSubscriptionByShortUuidResponseDto)
    async def get_raw_subscription(
        self,
        short_uuid: Annotated[str, Path(alias="shortUuid"), Field(description="Short UUID of the user")],
        with_disabled_hosts: Annotated[
            str,
            Query(alias="withDisabledHosts"), Field(default="false", description='Include disabled hosts, "true" or "false" (3.0: string, not boolean)'),
        ] = "false",
    ) -> GetRawSubscriptionByShortUuidResponseDto:
        """None"""
        ...

    @get("/subscriptions/connection-keys/{userId}", response_class=GetConnectionKeysByUserIdResponseDto)
    async def get_connection_keys_by_user_id(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="User ID")],
    ) -> GetConnectionKeysByUserIdResponseDto:
        """Get connection keys (base64 format) by user id"""
        ...
