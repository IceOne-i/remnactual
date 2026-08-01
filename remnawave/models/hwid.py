from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, StringConstraints


class CreateUserHwidDeviceBodyDto(BaseModel):
    """3.0: устройство привязывается к числовому `userId`, а не к `userUuid`."""

    hwid: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9=-]{10,64}$")]
    user_id: int = Field(serialization_alias="userId")
    platform: Optional[str] = None
    os_version: Optional[str] = Field(None, serialization_alias="osVersion")
    device_model: Optional[str] = Field(None, serialization_alias="deviceModel")
    user_agent: Optional[str] = Field(None, serialization_alias="userAgent")
    request_ip: Optional[str] = Field(None, serialization_alias="requestIp")


class DeleteUserHwidDeviceBodyDto(BaseModel):
    user_id: int = Field(serialization_alias="userId")
    hwid: str


class DeleteAllUserHwidDevicesBodyDto(BaseModel):
    user_id: int = Field(serialization_alias="userId")


class HwidDeviceDto(BaseModel):
    hwid: str
    user_id: int = Field(alias="userId")
    platform: Optional[str] = None
    os_version: Optional[str] = Field(None, alias="osVersion")
    device_model: Optional[str] = Field(None, alias="deviceModel")
    user_agent: Optional[str] = Field(None, alias="userAgent")
    request_ip: Optional[str] = Field(None, alias="requestIp")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class HwidDevicesData(BaseModel):
    total: float
    devices: List[HwidDeviceDto]


class CreateUserHwidDeviceResponseDto(BaseModel):
    total: float
    devices: List[HwidDeviceDto]


class DeleteUserHwidDeviceResponseDto(BaseModel):
    total: float
    devices: List[HwidDeviceDto]


class DeleteAllUserHwidDevicesResponseDto(BaseModel):
    total: float
    devices: List[HwidDeviceDto]


class GetUserHwidDevicesResponseDto(BaseModel):
    total: float
    devices: List[HwidDeviceDto]

class AppStatItem(BaseModel):
    app: str
    count: float


class PlatformStatItem(BaseModel):
    platform: str
    count: float
    # 2.8: byApp переехал внутрь каждой платформы
    by_app: List[AppStatItem] = Field(default_factory=list, alias="byApp")


class HwidStats(BaseModel):
    total_unique_devices: float = Field(alias="totalUniqueDevices")
    total_hwid_devices: float = Field(alias="totalHwidDevices")
    average_hwid_devices_per_user: float = Field(alias="averageHwidDevicesPerUser")


class HwidStatisticsData(BaseModel):
    by_platform: List[PlatformStatItem] = Field(alias="byPlatform")
    stats: HwidStats

    @property
    def by_app(self) -> List[AppStatItem]:
        """До 2.8 `byApp` был на верхнем уровне — собираем из платформ."""
        merged: dict[str, float] = {}
        for platform in self.by_platform:
            for item in platform.by_app:
                merged[item.app] = merged.get(item.app, 0.0) + item.count
        return [AppStatItem(app=app, count=count) for app, count in merged.items()]


class GetHwidDevicesStatsResponseDto(HwidStatisticsData):
    pass

class TopUserByHwidDevicesDto(BaseModel):
    """Top user by HWID devices"""
    id: int
    username: str
    devices_count: float = Field(alias="devicesCount")


class TopUsersByHwidDevicesData(BaseModel):
    """Top users by HWID devices data"""
    users: list[TopUserByHwidDevicesDto]
    total: float


class GetTopUsersByHwidDevicesResponseDto(TopUsersByHwidDevicesData):
    """Response for get top users by HWID devices"""
    pass

# Legacy aliases for backward compatibility
GetHwidStatisticsResponseDto = GetHwidDevicesStatsResponseDto
CreateUserHwidDeviceRequestDto = CreateUserHwidDeviceBodyDto
DeleteUserHwidDeviceRequestDto = DeleteUserHwidDeviceBodyDto
DeleteUserAllHwidDeviceRequestDto = DeleteAllUserHwidDevicesBodyDto
CreateHWIDUser = CreateUserHwidDeviceBodyDto
HWIDUserResponseDto = HwidDeviceDto
HWIDUserResponseDtoList = HwidDevicesData
HWIDDeleteRequest = DeleteUserHwidDeviceBodyDto
