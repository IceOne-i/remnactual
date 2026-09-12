from typing import Annotated

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateApiTokenBodyDto,
    CreateApiTokenResponseDto,
    GetApiTokenScopesResponseDto,
    GetApiTokensResponseDto,
    GetOttResponseDto,
)
from remnawave.rapid import BaseController, delete, get, post


class APITokensManagementController(BaseController):
    @post("/tokens", response_class=CreateApiTokenResponseDto)
    async def create(
        self,
        body: Annotated[CreateApiTokenBodyDto, PydanticBody()],
    ) -> CreateApiTokenResponseDto:
        """Create a new API token"""
        ...

    @delete("/tokens/{uuid}", response_class=None)
    async def delete(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the API token")],
    ) -> None:
        """Delete API token

        Отвечает ``204 No Content`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @get("/tokens", response_class=GetApiTokensResponseDto)
    async def find_all(
        self,
    ) -> GetApiTokensResponseDto:
        """Get all API tokens"""
        ...

    @get("/tokens/scopes", response_class=GetApiTokenScopesResponseDto)
    async def get_scopes(
        self,
    ) -> GetApiTokenScopesResponseDto:
        """Get available API token scopes"""
        ...

    @post("/tokens/ott", response_class=GetOttResponseDto)
    async def get_ott(
        self,
    ) -> GetOttResponseDto:
        """Get short-lived token for accessing backend tools (Swagger, Scalar, Bull Board)"""
        ...
