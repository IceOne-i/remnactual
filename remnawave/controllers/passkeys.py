from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    DeletePasskeyBodyDto,
    GetPasskeyRegistrationOptionsResponseDto,
    GetPasskeysResponseDto,
    UpdatePasskeyBodyDto,
    UpdatePasskeyResponseDto,
    VerifyPasskeyRegistrationBodyDto,
    VerifyPasskeyRegistrationResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class PasskeysController(BaseController):
    @get("/passkeys/registration/options", response_class=GetPasskeyRegistrationOptionsResponseDto)
    async def passkey_registration_options(
        self,
    ) -> GetPasskeyRegistrationOptionsResponseDto:
        """Get registration options for passkey"""
        ...

    @post("/passkeys/registration/verify", response_class=VerifyPasskeyRegistrationResponseDto)
    async def passkey_registration_verify(
        self,
        body: Annotated[VerifyPasskeyRegistrationBodyDto, PydanticBody()],
    ) -> VerifyPasskeyRegistrationResponseDto:
        """Verify registration for passkey"""
        ...

    @get("/passkeys", response_class=GetPasskeysResponseDto)
    async def get_active_passkeys(
        self,
    ) -> GetPasskeysResponseDto:
        """Get passkeys"""
        ...

    @delete("/passkeys", response_class=None)
    async def delete_passkey(
        self,
        body: Annotated[DeletePasskeyBodyDto, PydanticBody()],
    ) -> None:
        """Delete a passkey by ID

        Отвечает ``204 No Content`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @patch("/passkeys", response_class=UpdatePasskeyResponseDto)
    async def update_passkey(
        self,
        body: Annotated[UpdatePasskeyBodyDto, PydanticBody()],
    ) -> UpdatePasskeyResponseDto:
        """Update passkey"""
        ...
