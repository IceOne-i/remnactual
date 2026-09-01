"""SSH-доступ к ноде через панель (3.4.0+).

Оба эндпоинта закрыты РОЛЬЮ АДМИНИСТРАТОРА, а не скоупом API-токена: их
контроллер в панели объявлен `@Roles(ROLE.ADMIN)` и `@ApiScopeResource` не
несёт, поэтому в каталоге ``GET /tokens/scopes`` ресурса ``node-ssh`` нет
вовсе. Токеном, выпущенным через API, сюда не попасть ни с каким набором
скоупов — нужен админский JWT.

Сам терминал работает по WebSocket, и это НЕ поддерживается SDK: он построен
на httpx, а ``httpx`` веб-сокетов не умеет. Здесь только два HTTP-шага,
которые терминалу предшествуют, — билет и снятие блокировки хранилища ключей.
"""
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated


class CreateSshTicketResponseDto(BaseModel):
    """Одноразовый билет на открытие SSH-сессии."""

    #: Одноразовый; панель гасит его при первом использовании.
    ticket: str
    #: Путь WebSocket-эндпоинта, к которому билет предъявляется.
    path: str
    expires_in_seconds: int = Field(alias="expiresInSeconds")


class EvaluateVaultBodyDto(BaseModel):
    """Шаг ослеплённого вычисления при разблокировке хранилища SSH-ключей.

    Клиент присылает ослеплённое значение и получает вычисленное; сам пароль
    панели не показывается — в этом смысл шага. Значение base64, не длиннее
    128 символов (ограничение контракта).
    """

    blinded: Annotated[str, StringConstraints(max_length=128)]


class EvaluateVaultResponseDto(BaseModel):
    evaluated: str


__all__ = [
    "CreateSshTicketResponseDto",
    "EvaluateVaultBodyDto",
    "EvaluateVaultResponseDto",
]
