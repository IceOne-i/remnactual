from typing import Annotated
from uuid import UUID

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models.node_ssh import (
    CreateSshTicketResponseDto,
    EvaluateVaultBodyDto,
    EvaluateVaultResponseDto,
)
from remnawave.rapid import BaseController, post


class NodeSshController(BaseController):
    """SSH-доступ к ноде через панель (3.4.0+).

    **Закрыт ролью АДМИНИСТРАТОРА, а не скоупом.** Контроллер панели объявлен
    ``@Roles(ROLE.ADMIN)`` и не несёт ``@ApiScopeResource``, поэтому ресурса
    ``node-ssh`` нет в каталоге ``GET /tokens/scopes``: API-токен сюда не
    пустят ни с каким набором скоупов. Нужен админский JWT.

    Сам терминал работает по WebSocket и в SDK не поддержан: он построен на
    ``httpx``, а веб-сокетов тот не умеет. Здесь только два HTTP-шага,
    предшествующих терминалу.
    """

    @post("/node-ssh/{uuid}/ticket", response_class=CreateSshTicketResponseDto)
    async def create_ssh_ticket(
        self,
        uuid: Annotated[UUID, Path(description="Node UUID")],
    ) -> CreateSshTicketResponseDto:
        """Create a single-use ticket for opening an SSH terminal session"""
        ...

    @post("/node-ssh/vault/evaluate", response_class=EvaluateVaultResponseDto)
    async def evaluate_vault(
        self,
        body: Annotated[EvaluateVaultBodyDto, PydanticBody()],
    ) -> EvaluateVaultResponseDto:
        """Oblivious evaluation step for unlocking the SSH key vault

        Панель отвечает ``429`` (``A255``) при слишком частых попытках — шаг
        намеренно ограничен по скорости.
        """
        ...
