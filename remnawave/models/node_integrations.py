"""Node Integrations — интеграции, подмешиваемые в конфиг нод (3.3.0)."""
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

#: Имя интеграции: 2..30 символов (контракт CreateNodeIntegrationCommand).
NodeIntegrationName = Annotated[str, StringConstraints(min_length=2, max_length=30)]

#: Описание интеграции: до 255 символов, nullable.
NodeIntegrationDescription = Annotated[str, StringConstraints(max_length=255)]


class NodeIntegrationDto(BaseModel):
    """Интеграция ноды"""

    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: str
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class GetNodeIntegrationsResponseDto(BaseModel):
    """GET /node-integrations"""

    model_config = ConfigDict(populate_by_name=True)

    total: int
    node_integrations: List[NodeIntegrationDto] = Field(alias="nodeIntegrations")


class GetNodeIntegrationResponseDto(NodeIntegrationDto):
    """GET /node-integrations/{uuid}"""


class CreateNodeIntegrationBodyDto(BaseModel):
    """POST /node-integrations"""

    name: NodeIntegrationName
    description: Optional[NodeIntegrationDescription] = None
    config: Dict[str, Any]


class CreateNodeIntegrationResponseDto(NodeIntegrationDto):
    """Ответ POST /node-integrations"""


class UpdateNodeIntegrationBodyDto(BaseModel):
    """PATCH /node-integrations"""

    uuid: UUID
    name: Optional[NodeIntegrationName] = None
    description: Optional[NodeIntegrationDescription] = None
    config: Optional[Dict[str, Any]] = None
    #: Перезапустить ноды, на которых включена интеграция. По умолчанию панель не перезапускает.
    restart_nodes: Optional[bool] = Field(None, serialization_alias="restartNodes")


class UpdateNodeIntegrationResponseDto(NodeIntegrationDto):
    """Ответ PATCH /node-integrations"""


# DELETE /node-integrations/{uuid} отвечает 204 без тела — DTO ответа не нужен.
