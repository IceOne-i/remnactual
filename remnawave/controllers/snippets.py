from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateSnippetBodyDto,
    CreateSnippetResponseDto,
    DeleteSnippetBodyDto,
    GetSnippetsResponseDto,
    UpdateSnippetBodyDto,
    UpdateSnippetResponseDto,
)
from remnawave.rapid import BaseController, delete, get, post, patch


class SnippetsController(BaseController):
    @get("/snippets", response_class=GetSnippetsResponseDto)
    async def get_snippets(self) -> GetSnippetsResponseDto:
        """Get snippets"""
        ...

    @post("/snippets", response_class=CreateSnippetResponseDto)
    async def create_snippet(
        self,
        body: Annotated[CreateSnippetBodyDto, PydanticBody()],
    ) -> CreateSnippetResponseDto:
        """Create snippet"""
        ...

    @patch("/snippets", response_class=UpdateSnippetResponseDto)
    async def update_snippet(
        self,
        body: Annotated[UpdateSnippetBodyDto, PydanticBody()],
    ) -> UpdateSnippetResponseDto:
        """Update snippet"""
        ...

    @delete("/snippets", response_class=None)
    async def delete_snippet_by_name(
        self,
        body: Annotated[DeleteSnippetBodyDto, PydanticBody()],
    ) -> None:
        """Delete snippet

        Отвечает ``204 No Content`` с пустым телом — метод возвращает ``None``.
        """
        ...
