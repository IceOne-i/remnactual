from datetime import datetime
from typing import Annotated, List, Literal
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.enums import Scope


class CreateApiTokenBodyDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30)] = Field(
        serialization_alias="name"
    )
    expires_in_days: float = Field(serialization_alias="expiresInDays", ge=1)
    scopes: List[str] = Field(
        default_factory=lambda: [Scope.WILDCARD],
        description='API token scopes. Pass :class:`remnawave.enums.Scope` members (or raw strings). Defaults to ["*"] (full access). See GET /api/tokens/scopes for the catalog.',
    )

    def __init__(self, **data):
        # Backward compatibility: `token_name` was renamed to `name` in v2.8.0
        if "token_name" in data and "name" not in data:
            data["name"] = data.pop("token_name")
        super().__init__(**data)


class CreateApiTokenResponseData(BaseModel):
    uuid: UUID
    name: str
    expire_at: datetime = Field(alias="expireAt")
    scopes: List[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    token: str


class CreateApiTokenResponseDto(CreateApiTokenResponseData):
    """``POST /api/tokens`` — 201 Created, отдаёт токен вместе с его plaintext-значением."""
    pass


# 3.0: DELETE /api/tokens/{uuid} отвечает 204 без тела — DeleteApiTokenResponseDto удалён.


class ApiTokenDto(BaseModel):
    uuid: UUID
    name: str
    expire_at: datetime = Field(..., alias="expireAt")
    scopes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    @property
    def token_name(self) -> str:
        """Backward compatibility property (renamed to `name` in v2.8.0)"""
        return self.name


# 3.0: объект `docs` убран из ответа GET /api/tokens — DocsInfoDto удалён,
# документация переехала на /api/backend-tools/{swagger,scalar,queues}.


class GetApiTokensResponseDto(BaseModel):
    """``GET /api/tokens`` — 3.0 отдаёт только список токенов."""
    tokens: List[ApiTokenDto] = Field(..., alias="tokens")

    @property
    def api_keys(self) -> List[ApiTokenDto]:
        """Backward compatibility property (renamed to `tokens` in v2.8.0)"""
        return self.tokens


class GetOttResponseDto(BaseModel):
    """``POST /api/tokens/ott`` — короткоживущий токен для Swagger/Scalar/Bull Board."""
    ott: str


class ApiTokenScopeEndpointDto(BaseModel):
    key: str
    kind: Literal["read", "write"]
    method: str
    path: str
    description: str


class ApiTokenScopeResourceDto(BaseModel):
    resource: str
    resource_scopes: List[str] = Field(..., alias="resourceScopes")
    endpoints: List[ApiTokenScopeEndpointDto]


class GetApiTokenScopesResponseData(BaseModel):
    wildcard: str
    resources: List[ApiTokenScopeResourceDto]


class GetApiTokenScopesResponseDto(GetApiTokenScopesResponseData):
    pass


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# 3.0 переименовал тело запроса *RequestDto -> *BodyDto, а ответ GET /api/tokens —
# в GetApiTokensResponseDto (контрактное имя).
CreateApiTokenRequestDto = CreateApiTokenBodyDto
FindAllApiTokensResponseDto = GetApiTokensResponseDto
FindAllApiTokensResponseData = GetApiTokensResponseDto
