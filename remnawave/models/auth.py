from typing import Annotated, Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from remnawave.enums.auth import OAuth2Provider


class AuthTokenResponseData(BaseModel):
    access_token: str = Field(alias="accessToken")


class RegisterResponseDto(BaseModel):
    access_token: str = Field(alias="accessToken")


class LoginResponseDto(BaseModel):
    access_token: str = Field(alias="accessToken")


class PasskeyAuthenticationSettings(BaseModel):
    enabled: bool


class OAuth2ProvidersSettings(BaseModel):
    providers: Dict[str, bool]


class PasswordAuthenticationSettings(BaseModel):
    enabled: bool


class AuthenticationSettings(BaseModel):
    passkey: PasskeyAuthenticationSettings
    oauth2: OAuth2ProvidersSettings
    password: PasswordAuthenticationSettings


class BrandingSettings(BaseModel):
    title: Optional[str] = None
    logo_url: Optional[str] = Field(None, alias="logoUrl")


class GetStatusResponseDto(BaseModel):
    """Status response with authentication and branding settings"""
    is_login_allowed: bool = Field(alias="isLoginAllowed")
    is_register_allowed: bool = Field(alias="isRegisterAllowed")
    authentication: Optional[AuthenticationSettings] = None
    branding: BrandingSettings


class LoginBodyDto(BaseModel):
    username: str
    password: str


class RegisterBodyDto(BaseModel):
    username: str
    password: Annotated[str, StringConstraints(min_length=24)]

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class TelegramCallbackRequestDto(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class TelegramCallbackResponseDto(AuthTokenResponseData):
    pass


# OAuth2 Authorization models
class OAuth2AuthorizeBodyDto(BaseModel):
    """Request to initiate OAuth2 authorization"""
    provider: OAuth2Provider


class OAuth2AuthorizeResponseDto(BaseModel):
    """Response with OAuth2 authorization URL"""
    authorization_url: Optional[str] = Field(alias="authorizationUrl")


# OAuth2 Callback models
class OAuth2CallbackBodyDto(BaseModel):
    """Request for OAuth2 callback"""
    provider: OAuth2Provider
    code: str
    state: str


class OAuth2CallbackResponseDto(BaseModel):
    """Response with access token from OAuth2 callback"""
    access_token: str = Field(alias="accessToken")


# Passkey Authentication models
class GetPasskeyAuthenticationOptionsResponseDto(BaseModel):
    """Response with passkey authentication options.

    Контракт объявляет тело как `z.unknown()` — произвольный WebAuthn-объект,
    поэтому все ключи сохраняются как есть (`extra="allow"`).
    """
    model_config = ConfigDict(extra="allow")


class VerifyPasskeyAuthenticationBodyDto(BaseModel):
    """Request to verify passkey authentication"""
    # Passkey authentication response is complex WebAuthn object
    response: Dict[str, Any]


class VerifyPasskeyAuthenticationResponseDto(BaseModel):
    """Response with access token after successful passkey authentication"""
    access_token: str = Field(alias="accessToken")


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# 3.0 переименовал тела запросов *RequestDto -> *BodyDto.
LoginRequestDto = LoginBodyDto
RegisterRequestDto = RegisterBodyDto
OAuth2AuthorizeRequestDto = OAuth2AuthorizeBodyDto
OAuth2CallbackRequestDto = OAuth2CallbackBodyDto
VerifyPasskeyAuthenticationRequestDto = VerifyPasskeyAuthenticationBodyDto

# Legacy aliases (v2.8 и раньше)
StatusResponseDto = GetStatusResponseDto
LoginTelegramRequestDto = TelegramCallbackRequestDto
