from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    GetPasskeyAuthenticationOptionsResponseDto,
    GetStatusResponseDto,
    LoginBodyDto,
    LoginResponseDto,
    OAuth2AuthorizeBodyDto,
    OAuth2AuthorizeResponseDto,
    OAuth2CallbackBodyDto,
    OAuth2CallbackResponseDto,
    RegisterBodyDto,
    RegisterResponseDto,
    VerifyPasskeyAuthenticationBodyDto,
    VerifyPasskeyAuthenticationResponseDto,
)
from remnawave.rapid import BaseController, get, post


class AuthController(BaseController):
    @post("/auth/login", response_class=LoginResponseDto)
    async def login(
        self,
        body: Annotated[LoginBodyDto, PydanticBody()],
    ) -> LoginResponseDto:
        """Login as superadmin"""
        ...

    @post("/auth/register", response_class=RegisterResponseDto)
    async def register(
        self,
        body: Annotated[RegisterBodyDto, PydanticBody()],
    ) -> RegisterResponseDto:
        """Register as superadmin"""
        ...

    @get("/auth/status", response_class=GetStatusResponseDto)
    async def get_status(
        self,
    ) -> GetStatusResponseDto:
        """Get the status of the authentication"""
        ...

    @post("/auth/oauth2/authorize", response_class=OAuth2AuthorizeResponseDto)
    async def oauth2_authorize(
        self,
        body: Annotated[OAuth2AuthorizeBodyDto, PydanticBody()],
    ) -> OAuth2AuthorizeResponseDto:
        """Initiate OAuth2 authorization"""
        ...

    @post("/auth/oauth2/callback", response_class=OAuth2CallbackResponseDto)
    async def oauth2_callback(
        self,
        body: Annotated[OAuth2CallbackBodyDto, PydanticBody()],
    ) -> OAuth2CallbackResponseDto:
        """Callback from OAuth2"""
        ...

    @get("/auth/passkey/authentication/options", response_class=GetPasskeyAuthenticationOptionsResponseDto)
    async def passkey_authentication_options(
        self,
    ) -> GetPasskeyAuthenticationOptionsResponseDto:
        """Get the authentication options for passkey"""
        ...

    @post("/auth/passkey/authentication/verify", response_class=VerifyPasskeyAuthenticationResponseDto)
    async def passkey_authentication_verify(
        self,
        body: Annotated[VerifyPasskeyAuthenticationBodyDto, PydanticBody()],
    ) -> VerifyPasskeyAuthenticationResponseDto:
        """Verify the authentication for passkey"""
        ...
