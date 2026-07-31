from typing import Annotated, Optional

from remnawave.models import (
    CreateUserHwidDeviceResponseDto,
    DeleteUserHwidDeviceResponseDto,
    GetUserHwidDevicesResponseDto,
    GetHwidStatisticsResponseDto,
    CreateHWIDUser,
    HWIDDeleteRequest,
    DeleteUserAllHwidDeviceRequestDto,
    GetTopUsersByHwidDevicesResponseDto
)
from rapid_api_client import Path, PydanticBody, Query
from remnawave.rapid import BaseController, post, get


class HWIDUserController(BaseController):
    @get("/hwid/devices", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_users(
        self,
        size: Annotated[
            Optional[int], Query(default=None, ge=1, le=1000, description="Page size, 1..1000")
        ] = None,
        start: Annotated[
            Optional[int], Query(default=None, description="Offset for pagination")
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

    @get("/hwid/devices/stats", response_class=GetHwidStatisticsResponseDto)
    async def get_hwid_stats(
        self,
    ) -> GetHwidStatisticsResponseDto:
        """Get HWID statistics"""
        ...

    @post("/hwid/devices", response_class=CreateUserHwidDeviceResponseDto)
    async def add_hwid_to_users(
        self,
        body: Annotated[CreateHWIDUser, PydanticBody()],
    ) -> CreateUserHwidDeviceResponseDto:
        """Create a user HWID device"""
        ...

    @post("/hwid/devices/delete", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_hwid_to_user(
        self,
        body: Annotated[HWIDDeleteRequest, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete a user HWID device"""
        ...

    @post("/hwid/devices/delete-all", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_all_hwid_user(
        self,
        body: Annotated[DeleteUserAllHwidDeviceRequestDto, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete all user HWID devices"""
        ...

    @get("/hwid/devices/{userUuid}", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_user(
        self,
        uuid: Annotated[str, Path(description="UUID of the User", alias="userUuid")],
    ) -> GetUserHwidDevicesResponseDto:
        """Get a user HWID device"""
        ...

    @get("/hwid/devices/top-users", response_class=GetTopUsersByHwidDevicesResponseDto)
    async def get_top_users_by_hwid_devices(
        self,
        size: Annotated[Optional[int], Query(default=None, description="Page size for pagination")] = None,
        start: Annotated[Optional[int], Query(default=None, description="Offset for pagination")] = None,
    ) -> GetTopUsersByHwidDevicesResponseDto:
        """Get top users by HWID devices"""
        ...