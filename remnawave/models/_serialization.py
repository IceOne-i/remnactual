"""Помощники сериализации тел запросов.

Тела запросов сериализуются с ``exclude_unset=True`` (см. :mod:`remnawave.rapid.client`):
уходит ровно то, что задал вызывающий, поэтому явный ``None`` доезжает до API как JSON
``null``, а нетронутые поля не отправляются вовсе.

Некоторые эндпоинты объявляют ключ обязательным, хотя у SDK для него есть разумное
значение по умолчанию (дискриминаторы, ``forceRestart``, ``inbounds`` и т.п.).
Такие модели наследуются от :class:`AlwaysEmitModel` и перечисляют имена полей в
``__always_emit__`` — эти ключи попадают в тело всегда.
"""
from typing import Any, ClassVar, Tuple

from pydantic import BaseModel, TypeAdapter, model_serializer


class AlwaysEmitModel(BaseModel):
    """Базовая модель, гарантирующая наличие обязательных ключей в теле запроса."""

    #: Имена полей (python-имена), которые обязаны присутствовать в каждом дампе.
    __always_emit__: ClassVar[Tuple[str, ...]] = ()

    @model_serializer(mode="wrap")
    def _emit_required_keys(self, handler, info) -> Any:
        data = handler(self)
        if not isinstance(data, dict):
            return data
        for name in self.__always_emit__:
            field = type(self).model_fields[name]
            key = name
            if info.by_alias:
                key = field.serialization_alias or field.alias or name
            if key not in data:
                data[key] = TypeAdapter(field.annotation).dump_python(
                    getattr(self, name),
                    mode=info.mode or "python",
                    by_alias=True,
                )
        return data
