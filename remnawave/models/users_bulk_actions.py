from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from remnawave.enums import UserStatus, TrafficLimitStrategy


# Type alias for tag validation
TagStr = Annotated[
    str,
    Field(min_length=1, max_length=16, pattern=r"^[A-Z0-9_]+$")
]


# ─────────────────────────────────────────────────────────────────────────────
# Тела запросов.
# 3.0: пользователи адресуются числовыми `userIds` вместо `uuids`, а все
# bulk-эндпоинты отвечают 202/204 с пустым телом — response-моделей больше нет.
# ─────────────────────────────────────────────────────────────────────────────
class BulkDeleteUsersByStatusBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/delete-by-status`.

    `status` обязателен в контракте и намеренно не имеет значения по умолчанию:
    неявный дефолт удалял бы всех ACTIVE-пользователей.
    """
    status: UserStatus


class BulkDeleteUsersBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/delete`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )


class BulkRevokeUsersSubscriptionBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/revoke-subscription`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )


class BulkResetTrafficUsersBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/reset-traffic`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )


class UpdateUserFields(BaseModel):
    """Fields to update for users"""
    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[float] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited"
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy"
    )
    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z"
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )
    hwid_device_limit: Optional[int] = Field(
        None,
        serialization_alias="hwidDeviceLimit",
        ge=0
    )
    external_squad_uuid: Optional[UUID] = Field(
        None,
        serialization_alias="externalSquadUuid",
        description="Optional. External squad UUID."
    )


class BulkUpdateUsersBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/update`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )
    fields: UpdateUserFields


class BulkUpdateUsersSquadsBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/update-squads`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )
    active_internal_squads: List[UUID] = Field(serialization_alias="activeInternalSquads")


class BulkExtendExpirationDateBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/extend-expiration-date`"""
    user_ids: List[int] = Field(
        serialization_alias="userIds", min_length=1, max_length=500
    )
    extend_days: int = Field(
        serialization_alias="extendDays",
        ge=1,
        le=9999
    )


class BulkAllUpdateUsersBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/all/update`"""
    # Без значения по умолчанию: иначе каждый вызов bulk/all/update
    # переводил бы ВСЕХ пользователей в ACTIVE.
    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[float] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited"
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy"
    )
    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z"
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )
    hwid_device_limit: Optional[int] = Field(
        None,
        serialization_alias="hwidDeviceLimit",
        ge=0
    )


class BulkAllExtendExpirationDateBodyDto(BaseModel):
    """Тело `POST /api/users/bulk/all/extend-expiration-date`"""
    extend_days: int = Field(
        serialization_alias="extendDays",
        ge=1
    )


# ─────────────────────────────────────────────────────────────────────────────
# Обратная совместимость: имена тел запросов до 3.0.
# ─────────────────────────────────────────────────────────────────────────────
BulkDeleteUsersByStatusRequestDto = BulkDeleteUsersByStatusBodyDto
BulkDeleteUsersRequestDto = BulkDeleteUsersBodyDto
BulkRevokeUsersSubscriptionRequestDto = BulkRevokeUsersSubscriptionBodyDto
BulkResetTrafficUsersRequestDto = BulkResetTrafficUsersBodyDto
BulkUpdateUsersRequestDto = BulkUpdateUsersBodyDto
BulkUpdateUsersSquadsRequestDto = BulkUpdateUsersSquadsBodyDto
BulkUpdateUsersInternalSquadsRequestDto = BulkUpdateUsersSquadsBodyDto
BulkExtendExpirationDateRequestDto = BulkExtendExpirationDateBodyDto
BulkAllUpdateUsersRequestDto = BulkAllUpdateUsersBodyDto
BulkAllExtendExpirationDateRequestDto = BulkAllExtendExpirationDateBodyDto
