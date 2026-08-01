from datetime import datetime
from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class PasskeyDto(BaseModel):
    """Passkey data model"""
    id: str
    name: str
    created_at: datetime = Field(alias="createdAt")
    last_used_at: datetime = Field(alias="lastUsedAt")


# Registration models
class GetPasskeyRegistrationOptionsResponseDto(BaseModel):
    """Response with passkey registration options.

    Контракт объявляет тело как `z.unknown()` — произвольный WebAuthn-объект,
    поэтому все ключи сохраняются как есть (`extra="allow"`).
    """
    model_config = ConfigDict(extra="allow")


class VerifyPasskeyRegistrationBodyDto(BaseModel):
    """Request to verify passkey registration"""
    # WebAuthn registration response is complex object
    response: Dict[str, Any]


class VerifyPasskeyRegistrationResponseData(BaseModel):
    """Passkey registration verification result data"""
    verified: bool


class VerifyPasskeyRegistrationResponseDto(BaseModel):
    """Response with passkey registration verification result"""
    verified: bool


class GetPasskeysResponseDto(BaseModel):
    """``GET /api/passkeys`` — список passkey текущего администратора"""
    passkeys: List[PasskeyDto]


class DeletePasskeyBodyDto(BaseModel):
    """Request to delete a passkey"""
    id: str


# 3.0: DELETE /api/passkeys отвечает 204 без тела — DeletePasskeyResponseDto удалён.


class UpdatePasskeyBodyDto(BaseModel):
    """Request to update a passkey"""
    id: str
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]


class UpdatePasskeyResponseData(BaseModel):
    """Response data with updated passkeys list"""
    passkeys: List[PasskeyDto]


class UpdatePasskeyResponseDto(BaseModel):
    """Response with updated passkey information"""
    passkeys: List[PasskeyDto]


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# 3.0 переименовал тела запросов *RequestDto -> *BodyDto, а ответ GET /api/passkeys —
# в GetPasskeysResponseDto (контрактное имя).
VerifyPasskeyRegistrationRequestDto = VerifyPasskeyRegistrationBodyDto
DeletePasskeyRequestDto = DeletePasskeyBodyDto
UpdatePasskeyRequestDto = UpdatePasskeyBodyDto
GetAllPasskeysResponseDto = GetPasskeysResponseDto
GetAllPasskeysResponseData = GetPasskeysResponseDto
