from typing import Annotated

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateNodeIntegrationBodyDto,
    CreateNodeIntegrationResponseDto,
    GetNodeIntegrationResponseDto,
    GetNodeIntegrationsResponseDto,
    UpdateNodeIntegrationBodyDto,
    UpdateNodeIntegrationResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodeIntegrationsController(BaseController):
    """Node Integrations (3.3.0).

    Интеграция — именованный кусок конфигурации, который панель подмешивает
    в конфиг каждой ноды, где он включён (`integrationUuids` у ноды).
    """

    @get("/node-integrations", response_class=GetNodeIntegrationsResponseDto)
    async def get_all_node_integrations(self) -> GetNodeIntegrationsResponseDto:
        """Get all Node Integrations"""
        ...

    @get("/node-integrations/{uuid}", response_class=GetNodeIntegrationResponseDto)
    async def get_node_integration(
        self,
        uuid: Annotated[str, Path(), Field(description="Node integration UUID")],
    ) -> GetNodeIntegrationResponseDto:
        """Get Node Integration by uuid"""
        ...

    @post("/node-integrations", response_class=CreateNodeIntegrationResponseDto)
    async def create_node_integration(
        self,
        body: Annotated[CreateNodeIntegrationBodyDto, PydanticBody()],
    ) -> CreateNodeIntegrationResponseDto:
        """Create Node Integration (201 Created)"""
        ...

    @patch("/node-integrations", response_class=UpdateNodeIntegrationResponseDto)
    async def update_node_integration(
        self,
        body: Annotated[UpdateNodeIntegrationBodyDto, PydanticBody()],
    ) -> UpdateNodeIntegrationResponseDto:
        """Update Node Integration

        `restart_nodes=True` перезапускает ноды, на которых интеграция включена.
        """
        ...

    @delete("/node-integrations/{uuid}", response_class=None)
    async def delete_node_integration(
        self,
        uuid: Annotated[str, Path(), Field(description="Node integration UUID")],
    ) -> None:
        """Delete Node Integration (204 No Content)"""
        ...
