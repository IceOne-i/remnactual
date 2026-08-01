from typing import Annotated, Optional

from remnawave.models import (
    CreateUserHwidDeviceBodyDto,
    CreateUserHwidDeviceResponseDto,
    DeleteAllUserHwidDevicesBodyDto,
    DeleteAllUserHwidDevicesResponseDto,
    DeleteUserHwidDeviceBodyDto,
    DeleteUserHwidDeviceResponseDto,
    GetHwidDevicesStatsResponseDto,
    GetTopUsersByHwidDevicesResponseDto,
    GetUserHwidDevicesResponseDto,
)
from rapid_api_client import Path, PydanticBody, Query
from remnawave.rapid import BaseController, post, get


class HWIDUserController(BaseController):
    @get("/hwid/devices", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_users(
        self,
        size: Annotated[
            Optional[int],
            Query(default=None, ge=1, le=1000, description="Page size, 1..1000 (default 25)"),
        ] = None,
        start: Annotated[
            Optional[int], Query(default=None, description="Offset for pagination (default 0)")
        ] = None,
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
    ) -> GetUserHwidDevicesResponseDto:
        """Get all user HWID devices"""
        ...

    @get("/hwid/devices/stats", response_class=GetHwidDevicesStatsResponseDto)
    async def get_hwid_stats(
        self,
    ) -> GetHwidDevicesStatsResponseDto:
        """Get HWID statistics"""
        ...

    @post("/hwid/devices", response_class=CreateUserHwidDeviceResponseDto)
    async def add_hwid_to_users(
        self,
        body: Annotated[CreateUserHwidDeviceBodyDto, PydanticBody()],
    ) -> CreateUserHwidDeviceResponseDto:
        """Create a user HWID device"""
        ...

    @post("/hwid/devices/delete", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_hwid_to_user(
        self,
        body: Annotated[DeleteUserHwidDeviceBodyDto, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete a user HWID device"""
        ...

    @post("/hwid/devices/delete-all", response_class=DeleteAllUserHwidDevicesResponseDto)
    async def delete_all_hwid_user(
        self,
        body: Annotated[DeleteAllUserHwidDevicesBodyDto, PydanticBody()],
    ) -> DeleteAllUserHwidDevicesResponseDto:
        """Delete all user HWID devices"""
        ...

    @get("/hwid/devices/{userId}", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_user(
        self,
        user_id: Annotated[int, Path(description="ID of the User", alias="userId")],
    ) -> GetUserHwidDevicesResponseDto:
        """Get a user HWID device"""
        ...

    @get("/hwid/devices/top-users", response_class=GetTopUsersByHwidDevicesResponseDto)
    async def get_top_users_by_hwid_devices(
        self,
        size: Annotated[
            Optional[int],
            Query(default=None, ge=1, le=100, description="Page size, 1..100 (default 5)"),
        ] = None,
        start: Annotated[
            Optional[int], Query(default=None, description="Offset for pagination (default 0)")
        ] = None,
    ) -> GetTopUsersByHwidDevicesResponseDto:
        """Get top users by HWID devices"""
        ...
