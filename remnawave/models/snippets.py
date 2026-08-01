from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, StringConstraints


class SnippetItem(BaseModel):
    """Individual snippet item"""
    name: str
    snippet: Any  # Can be any JSON object or array


class SnippetsData(BaseModel):
    """Snippets response data"""
    total: int
    snippets: List[SnippetItem]


# Изменяем структуру - API возвращает данные напрямую
class GetSnippetsResponseDto(SnippetsData):
    """Get all snippets response - extends SnippetsData directly"""
    pass


class CreateSnippetResponseDto(SnippetsData):
    """Create snippet response - extends SnippetsData directly"""
    pass


class UpdateSnippetResponseDto(SnippetsData):
    """Update snippet response - extends SnippetsData directly"""
    pass


# 3.0: DELETE /api/snippets отвечает 204 без тела — DeleteSnippetResponseDto удалён.


class CreateSnippetBodyDto(BaseModel):
    """Create snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]
    snippet: List[Dict[str, Any]]  # Array of objects


class UpdateSnippetBodyDto(BaseModel):
    """Update snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]
    snippet: List[Dict[str, Any]]  # Array of objects


class DeleteSnippetBodyDto(BaseModel):
    """Delete snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]


# ---------------- BACKWARDS-COMPATIBLE ALIASES ---------------- #
# 3.0 переименовал тела запросов *RequestDto -> *BodyDto.
CreateSnippetRequestDto = CreateSnippetBodyDto
UpdateSnippetRequestDto = UpdateSnippetBodyDto
DeleteSnippetRequestDto = DeleteSnippetBodyDto
