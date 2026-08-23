"""Host Mapper — правка сгенерированного конфига хоста, 3.3.0.

Операции выполняются **после** генератора, поэтому могут изменить или удалить всё,
что он произвёл. Источник для ``copy`` — сырой инбаунд конфиг-профиля, которому
принадлежит хост, либо сам хост, если путь начинается с ``$host.``.

Секции соответствуют типам клиентов: ``xrayJson``, ``mihomo``, ``base64``, ``singbox``.
"""
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models._serialization import AlwaysEmitModel

#: Путь внутри сырого инбаунда/хоста или внутри генерируемого конфига.
HostMapperPath = Annotated[str, StringConstraints(min_length=1, max_length=512)]

#: Значение операции ``set``: строки, числа, булевы, массивы и объекты.
HostMapperValue = Union[bool, int, float, str, List[Any], Dict[str, Any]]


class HostMapperCopyOperation(AlwaysEmitModel):
    """Копирует значение из сырого инбаунда (или из хоста через ``$host.``)."""

    model_config = ConfigDict(populate_by_name=True)

    __always_emit__ = ("op",)

    op: Literal["copy"] = "copy"
    #: `from` — зарезервированное слово Python, поэтому поле называется `from_`.
    from_: HostMapperPath = Field(alias="from", serialization_alias="from")
    to: HostMapperPath


class HostMapperSetOperation(AlwaysEmitModel):
    """Записывает фиксированное значение, создавая недостающие ключи."""

    model_config = ConfigDict(populate_by_name=True)

    __always_emit__ = ("op",)

    op: Literal["set"] = "set"
    to: HostMapperPath
    value: HostMapperValue


class HostMapperUnsetOperation(AlwaysEmitModel):
    """Удаляет поле, которое сгенерировал сам генератор."""

    model_config = ConfigDict(populate_by_name=True)

    __always_emit__ = ("op",)

    op: Literal["unset"] = "unset"
    to: HostMapperPath


#: Дискриминированное объединение операций — дискриминатор `op`.
HostMapperOperation = Annotated[
    Union[HostMapperCopyOperation, HostMapperSetOperation, HostMapperUnsetOperation],
    Field(discriminator="op"),
]


class HostMapperDto(BaseModel):
    """Набор операций по типам клиентов.

    Панели до 3.3.0 поля `mapper` не присылают — все секции остаются ``None``.
    """

    model_config = ConfigDict(populate_by_name=True)

    xray_json: Optional[List[HostMapperOperation]] = Field(None, alias="xrayJson")
    mihomo: Optional[List[HostMapperOperation]] = None
    base64: Optional[List[HostMapperOperation]] = None
    singbox: Optional[List[HostMapperOperation]] = None
