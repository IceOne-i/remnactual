"""Метки сущностей (панель 3.4.0+).

Одна и та же пара эндпоинтов заведена панелью на ШЕСТИ сущностях — профилях
конфигурации, внутренних и внешних сквадах, плагинах нод, конфигах страницы
подписки и шаблонах подписки, — с побайтово одинаковыми телами и ответами.
Поэтому модели здесь общие: шесть копий расходились бы при первой же правке
контракта, и разошлись бы молча.

Не путать с метками ХОСТА (``HostTag`` в ``models/hosts.py``) и метками
ПОЛЬЗОВАТЕЛЯ: те живут прямо в теле своей сущности и появились задолго до 3.4.
"""
from typing import Annotated, List
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

#: Одна метка: заглавные латинские буквы, цифры, подчёркивание и двоеточие,
#: не длиннее 36 символов. Ограничения — контрактные (`TagSchema`).
EntityTag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]


class GetEntityTagsResponseDto(BaseModel):
    """``GET /<сущность>/tags`` — все метки, встречающиеся у сущностей этого вида."""

    tags: List[str] = Field(default_factory=list)


class SetEntityTagsBodyDto(BaseModel):
    """``PATCH /<сущность>/tags`` — ЗАМЕНА набора меток у одной сущности.

    Именно замена, а не добавление: панель сохраняет присланный список целиком,
    поэтому пустой список снимает все метки.
    """

    uuid: UUID
    #: Не более десяти меток — ограничение контракта (`TagsSchema`).
    tags: List[EntityTag] = Field(default_factory=list, max_length=10)


class SetEntityTagsResponseDto(BaseModel):
    uuid: UUID
    tags: List[str] = Field(default_factory=list)


__all__ = [
    "EntityTag",
    "GetEntityTagsResponseDto",
    "SetEntityTagsBodyDto",
    "SetEntityTagsResponseDto",
]
