from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models.users_bulk_actions import (
    BulkAllExtendExpirationDateBodyDto,
    BulkAllUpdateUsersBodyDto,
    BulkDeleteUsersBodyDto,
    BulkDeleteUsersByStatusBodyDto,
    BulkExtendExpirationDateBodyDto,
    BulkResetTrafficUsersBodyDto,
    BulkRevokeUsersSubscriptionBodyDto,
    BulkUpdateUsersBodyDto,
    BulkUpdateUsersSquadsBodyDto,
)
from remnawave.rapid import BaseController, post


class UsersBulkActionsController(BaseController):
    """3.0: каждый bulk-эндпоинт отвечает 202/204 с пустым телом — методы возвращают ``None``."""

    @post("/users/bulk/delete-by-status", response_class=None)
    async def bulk_delete_users_by_status(
        self,
        body: Annotated[BulkDeleteUsersByStatusBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Delete Users By Status (202 Accepted)"""
        ...

    @post("/users/bulk/delete", response_class=None)
    async def bulk_delete_users(
        self,
        body: Annotated[BulkDeleteUsersBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Delete Users By User IDs (204 No Content)"""
        ...

    @post("/users/bulk/revoke-subscription", response_class=None)
    async def bulk_revoke_users_subscription(
        self,
        body: Annotated[BulkRevokeUsersSubscriptionBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Revoke Users Subscription (202 Accepted)"""
        ...

    @post("/users/bulk/reset-traffic", response_class=None)
    async def bulk_reset_user_traffic(
        self,
        body: Annotated[BulkResetTrafficUsersBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Reset User Traffic (202 Accepted)"""
        ...

    @post("/users/bulk/update", response_class=None)
    async def bulk_update_users(
        self,
        body: Annotated[BulkUpdateUsersBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Update Users (202 Accepted)"""
        ...

    @post("/users/bulk/update-squads", response_class=None)
    async def bulk_update_users_internal_squads(
        self,
        body: Annotated[BulkUpdateUsersSquadsBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Update Users Internal Squads (204 No Content)"""
        ...

    @post("/users/bulk/extend-expiration-date", response_class=None)
    async def bulk_extend_expiration_date(
        self,
        body: Annotated[BulkExtendExpirationDateBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Extend Users Expiration Date (204 No Content)"""
        ...

    @post("/users/bulk/all/update", response_class=None)
    async def bulk_update_all_users(
        self,
        body: Annotated[BulkAllUpdateUsersBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Update All Users (202 Accepted)"""
        ...

    @post("/users/bulk/all/reset-traffic", response_class=None)
    async def bulk_all_reset_user_traffic(
        self,
    ) -> None:
        """Bulk Reset All Users Traffic (202 Accepted)"""
        ...

    @post("/users/bulk/all/extend-expiration-date", response_class=None)
    async def bulk_all_extend_expiration_date(
        self,
        body: Annotated[BulkAllExtendExpirationDateBodyDto, PydanticBody()],
    ) -> None:
        """Bulk Extend All Users Expiration Date (202 Accepted)"""
        ...
