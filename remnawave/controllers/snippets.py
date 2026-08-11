from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateSnippetBodyDto,
    CreateSnippetResponseDto,
    DeleteSnippetBodyDto,
    GetSnippetsResponseDto,
    SyncSnippetBodyDto,
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

    @post("/snippets/actions/sync", response_class=None)
    async def sync_snippet(
        self,
        body: Annotated[SyncSnippetBodyDto, PydanticBody()],
    ) -> None:
        """Sync snippet to affected config profiles

        3.2.3: раскатывает сниппет по всем конфиг-профилям, которые на него ссылаются;
        ноды этих профилей перезапускаются.

        Отвечает ``202 Accepted`` с пустым телом — метод возвращает ``None``.
        """
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
