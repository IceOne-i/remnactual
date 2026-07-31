from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateUserHwidDeviceRequestDto(BaseModel):
    hwid: str
    user_uuid: UUID = Field(serialization_alias="userUuid")
    platform: Optional[str] = None
    os_version: Optional[str] = Field(None, serialization_alias="osVersion")
    device_model: Optional[str] = Field(None, serialization_alias="deviceModel")
    user_agent: Optional[str] = Field(None, serialization_alias="userAgent")
    request_ip: Optional[str] = Field(None, serialization_alias="requestIp")


class DeleteUserHwidDeviceRequestDto(BaseModel):
    user_uuid: UUID = Field(serialization_alias="userUuid")
    hwid: str


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


class GetHwidStatisticsResponseDto(HwidStatisticsData):
    pass

class DeleteUserAllHwidDeviceRequestDto(BaseModel):
    user_uuid: UUID = Field(serialization_alias="userUuid")
    
class TopUserByHwidDevicesDto(BaseModel):
    """Top user by HWID devices"""
    user_uuid: UUID = Field(alias="userUuid")
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
CreateHWIDUser = CreateUserHwidDeviceRequestDto
HWIDUserResponseDto = HwidDeviceDto
HWIDUserResponseDtoList = HwidDevicesData
HWIDDeleteRequest = DeleteUserHwidDeviceRequestDto
