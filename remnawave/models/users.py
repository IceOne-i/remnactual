from datetime import datetime
from typing import Annotated, List, Literal, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    model_validator,
)

from remnawave.enums import TrafficLimitStrategy, UserStatus
from remnawave.utils.happ_crypt import create_happ_crypto_link


class UserActiveInboundsDto(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: str | None = None
    security: str | None = None


class UserLastConnectedNodeDto(BaseModel):
    connected_at: datetime = Field(alias="connectedAt")
    node_name: str = Field(alias="nodeName")


class ActiveInternalSquadDto(BaseModel):
    """`BaseInternalSquadSchema` контракта 3.0."""
    uuid: UUID
    name: str


class HappCrypto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    crypto_link: str = Field(alias="cryptoLink")


class CreateUserBodyDto(BaseModel):
    """Тело `POST /api/users` (`CreateUserCommand.RequestBodySchema`).

    3.0: поле `uuid` удалено — идентификатор пользователя выдаёт панель (числовой `id`).
    """
    # Required fields
    username: Annotated[
        str,
        StringConstraints(pattern=r"^[a-zA-Z0-9_-]+$", min_length=3, max_length=36)
    ] = Field(..., description="Unique username for the user")
    expire_at: datetime = Field(..., serialization_alias="expireAt", description="Account expiration date")

    # Optional fields with defaults
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="User account status")
    traffic_limit_strategy: TrafficLimitStrategy = Field(
        default=TrafficLimitStrategy.NO_RESET,
        serialization_alias="trafficLimitStrategy",
        description="Traffic reset strategy"
    )

    # Optional fields
    short_uuid: Optional[str] = Field(None, serialization_alias="shortUuid")
    trojan_password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=32)]] = Field(
        None, serialization_alias="trojanPassword"
    )
    vless_uuid: Optional[UUID] = Field(None, serialization_alias="vlessUuid")
    ss_password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=32)]] = Field(
        None, serialization_alias="ssPassword"
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    created_at: Optional[datetime] = Field(None, serialization_alias="createdAt")
    last_traffic_reset_at: Optional[datetime] = Field(None, serialization_alias="lastTrafficResetAt")
    description: Optional[str] = None
    tag: Optional[Annotated[str, StringConstraints(max_length=16, pattern=r"^[A-Z0-9_]+$")]] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[EmailStr] = None
    hwid_device_limit: Optional[int] = Field(None, serialization_alias="hwidDeviceLimit", ge=0)
    active_internal_squads: Optional[List[UUID]] = Field(None, serialization_alias="activeInternalSquads")
    external_squad_uuid: Optional[UUID] = Field(None, serialization_alias="externalSquadUuid")


class UpdateUserBodyDto(BaseModel):
    """Тело `PATCH /api/users` (`UpdateUserCommand.RequestBodySchema`).

    3.0: пользователь идентифицируется числовым `id` (поле `uuid` удалено).
    Нужно передать хотя бы одно из `id` / `username`.
    """
    id: Optional[int] = Field(
        None,
        description="ID of the user. ID has higher priority than username",
    )
    username: Optional[str] = Field(None, description="Username of the user")

    # Optional update fields
    # Контракт: только ACTIVE или DISABLED — LIMITED/EXPIRED выставляет сама панель
    status: Optional[Literal[UserStatus.ACTIVE, UserStatus.DISABLED]] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    expire_at: Optional[datetime] = Field(None, serialization_alias="expireAt")
    hwid_device_limit: Optional[int] = Field(None, serialization_alias="hwidDeviceLimit", ge=0)
    tag: Optional[Annotated[str, StringConstraints(max_length=16, pattern=r"^[A-Z0-9_]+$")]] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    traffic_limit_bytes: Optional[float] = Field(None, serialization_alias="trafficLimitBytes", ge=0)
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, serialization_alias="trafficLimitStrategy"
    )
    active_internal_squads: Optional[List[UUID]] = Field(
        None, serialization_alias="activeInternalSquads"
    )
    external_squad_uuid: Optional[UUID] = Field(None, serialization_alias="externalSquadUuid")

    @model_validator(mode="after")
    def _require_identifier(self):
        if self.id is None and self.username is None:
            raise ValueError("Either id or username must be provided")
        return self


class UserTrafficDto(BaseModel):
    """`UserTrafficSchema` контракта 3.0."""
    used_traffic_bytes: float = Field(alias="usedTrafficBytes")
    lifetime_used_traffic_bytes: float = Field(alias="lifetimeUsedTrafficBytes")
    online_at: Optional[datetime] = Field(None, alias="onlineAt")
    first_connected_at: Optional[datetime] = Field(None, alias="firstConnectedAt")
    last_connected_node_uuid: Optional[UUID] = Field(None, alias="lastConnectedNodeUuid")


class UserResponseDto(BaseModel):
    """`ExtendedUsersSchema` контракта 3.0 — единое тело всех ответов о пользователе.

    3.0: поля `uuid`, `subLastUserAgent`, `subLastOpenedAt` удалены,
    идентификатор пользователя — числовой `id`.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: int
    short_uuid: str = Field(alias="shortUuid")
    username: str
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    traffic_limit_bytes: float = Field(0, alias="trafficLimitBytes")
    traffic_limit_strategy: TrafficLimitStrategy = Field(
        TrafficLimitStrategy.NO_RESET, alias="trafficLimitStrategy"
    )
    expire_at: datetime = Field(alias="expireAt")
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    email: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[str] = None
    hwid_device_limit: Optional[int] = Field(None, alias="hwidDeviceLimit")
    external_squad_uuid: Optional[UUID] = Field(None, alias="externalSquadUuid")
    trojan_password: str = Field(alias="trojanPassword")
    vless_uuid: UUID = Field(alias="vlessUuid")
    ss_password: str = Field(alias="ssPassword")
    last_trigger_threshold: int = Field(0, alias="lastTriggeredThreshold")
    sub_revoked_at: Optional[datetime] = Field(None, alias="subRevokedAt")
    last_traffic_reset_at: Optional[datetime] = Field(None, alias="lastTrafficResetAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    subscription_url: str = Field(alias="subscriptionUrl")
    active_internal_squads: list[ActiveInternalSquadDto] = Field(alias="activeInternalSquads")
    user_traffic: UserTrafficDto = Field(alias="userTraffic")

    @property
    def used_traffic_bytes(self) -> float:
        """Backward compatibility property"""
        return self.user_traffic.used_traffic_bytes

    @property
    def lifetime_used_traffic_bytes(self) -> float:
        """Backward compatibility property"""
        return self.user_traffic.lifetime_used_traffic_bytes

    @property
    def online_at(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.online_at

    @property
    def first_connected(self) -> Optional[datetime]:
        """Backward compatibility property"""
        return self.user_traffic.first_connected_at

    @property
    def last_connected_node_uuid(self) -> Optional[UUID]:
        """Backward compatibility property"""
        return self.user_traffic.last_connected_node_uuid

    @property
    def happ(self) -> HappCrypto:
        """Generate Happ Crypto Link"""
        crypto_link = create_happ_crypto_link(self.subscription_url)
        return HappCrypto(cryptoLink=crypto_link)

    def happ_with_version(self, version: Literal["v3", "v4"] = "v4") -> HappCrypto:
        return self._generate_happ(version=version)

    def _generate_happ(self, version):
        crypto_link = create_happ_crypto_link(content=self.subscription_url, method=version)
        return HappCrypto(cryptoLink=crypto_link)


class RevokeUserBodyDto(BaseModel):
    """Тело `POST /api/users/{userId}/actions/revoke`."""
    short_uuid: Optional[str] = Field(
        None,
        serialization_alias="shortUuid",
        description="Optional. If not provided, a new short UUID will be generated by Remnawave.",
        min_length=16,
        max_length=64,
    )
    revoke_only_passwords: Optional[bool] = Field(
        None,
        serialization_alias="revokeOnlyPasswords",
        description="Optional. If true, only passwords will be revoked without changing the short UUID.",
    )


class ExtendUserBodyDto(BaseModel):
    """Тело `POST /api/users/{userId}/actions/extend` (новое в 3.0)."""
    days: int = Field(
        ...,
        ge=1,
        description="The number of days to extend the expiration date.",
    )


class ResolveUserBodyDto(BaseModel):
    """Тело `POST /api/users/resolve`.

    3.0: идентификатор `uuid` удалён — ровно одно из `id` / `shortUuid` / `username`.
    """
    id: Optional[int] = None
    short_uuid: Optional[str] = Field(None, serialization_alias="shortUuid")
    username: Optional[str] = None

    @model_validator(mode="after")
    def _exactly_one_identifier(self):
        provided = [self.id, self.short_uuid, self.username]
        if sum(v is not None for v in provided) != 1:
            raise ValueError(
                "Exactly one of id, short_uuid or username must be provided"
            )
        return self


class ResolveUserResponseDto(BaseModel):
    """Ответ `POST /api/users/resolve` (3.0: без `uuid`)."""
    id: int
    username: str
    short_uuid: str = Field(alias="shortUuid")


class SubscriptionRequestRecord(BaseModel):
    """Subscription request history record"""
    id: int
    user_id: int = Field(alias="userId")
    request_at: datetime = Field(alias="requestAt")
    # 3.1: какое правило SRR обработало запрос. Панели 3.0.x эти поля не пишут.
    srr_response_type: Optional[str] = Field(None, alias="srrResponseType")
    srr_rule_name: Optional[str] = Field(None, alias="srrRuleName")
    request_ip: Optional[str] = Field(None, alias="requestIp")
    user_agent: Optional[str] = Field(None, alias="userAgent")


class SubscriptionRequestsResponseData(BaseModel):
    """Subscription requests response data"""
    total: int
    records: List[SubscriptionRequestRecord]


class UsersResponseDto(BaseModel):
    """Users collection response"""
    users: list[UserResponseDto]
    total: int


class GetAllUsersResponseDto(UsersResponseDto):
    """Response for get all users"""
    pass


class UsersStreamData(BaseModel):
    """Cursor-based (keyset) users stream page"""
    users: list[UserResponseDto]
    next_cursor: Optional[str] = Field(
        None,
        alias="nextCursor",
        description="Cursor to fetch the next page, or null if there are no more results",
    )
    has_more: bool = Field(alias="hasMore", description="Whether there are more results to fetch")


class GetUsersStreamResponseDto(UsersStreamData):
    """Response for get all users using cursor-based (keyset) pagination"""
    pass


class TagsResponseDto(BaseModel):
    """Tags collection response"""
    tags: list[str]


class GetAllTagsResponseDto(TagsResponseDto):
    """Response for get all tags"""
    pass


class GetSubscriptionRequestsResponseDto(SubscriptionRequestsResponseData):
    """Response for get subscription requests"""
    pass


class GetUserSubscriptionRequestHistoryResponseDto(SubscriptionRequestsResponseData):
    """Response for get user subscription request history"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Обратная совместимость: имена моделей до 3.0.
# Тела запросов переименованы `*RequestDto` → `*BodyDto`, а все ответы об одном
# пользователе схлопнуты в `UserResponseDto` (`UserResponseSchema` контракта).
# ─────────────────────────────────────────────────────────────────────────────
CreateUserRequestDto = CreateUserBodyDto
UpdateUserRequestDto = UpdateUserBodyDto
RevokeUserRequestDto = RevokeUserBodyDto
ResolveUserRequestBodyDto = ResolveUserBodyDto

CreateUserResponseDto = UserResponseDto
UpdateUserResponseDto = UserResponseDto
GetUserByUuidResponseDto = UserResponseDto
GetUserByIdResponseDto = UserResponseDto
GetUserByShortUuidResponseDto = UserResponseDto
GetUserByUsernameResponseDto = UserResponseDto
DisableUserResponseDto = UserResponseDto
EnableUserResponseDto = UserResponseDto
ResetUserTrafficResponseDto = UserResponseDto
RevokeUserSubscriptionResponseDto = UserResponseDto
ExtendUserResponseDto = UserResponseDto
ActivateAllInboundsResponseDto = UserResponseDto
