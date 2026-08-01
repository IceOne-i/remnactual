from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateInfraBillingHistoryRecordBodyDto,
    CreateInfraBillingHistoryRecordResponseDto,
    CreateInfraBillingNodeBodyDto,
    CreateInfraBillingNodeResponseDto,
    CreateInfraProviderBodyDto,
    CreateInfraProviderResponseDto,
    GetInfraBillingHistoryRecordsResponseDto,
    GetInfraBillingNodesResponseDto,
    GetInfraProvidersResponseDto,
    GetInfraProviderResponseDto,
    UpdateInfraBillingNodeBodyDto,
    UpdateInfraBillingNodeResponseDto,
    UpdateInfraProviderBodyDto,
    UpdateInfraProviderResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class InfraBillingController(BaseController):
    @get("/infra-billing/providers", response_class=GetInfraProvidersResponseDto)
    async def get_infra_providers(self) -> GetInfraProvidersResponseDto:
        """Get all infra providers"""
        ...

    @post("/infra-billing/providers", response_class=CreateInfraProviderResponseDto)
    async def create_infra_provider(
        self,
        body: Annotated[CreateInfraProviderBodyDto, PydanticBody()],
    ) -> CreateInfraProviderResponseDto:
        """Create infra provider"""
        ...

    @patch("/infra-billing/providers", response_class=UpdateInfraProviderResponseDto)
    async def update_infra_provider(
        self,
        body: Annotated[UpdateInfraProviderBodyDto, PydanticBody()],
    ) -> UpdateInfraProviderResponseDto:
        """Update infra provider"""
        ...

    @get("/infra-billing/providers/{uuid}", response_class=GetInfraProviderResponseDto)
    async def get_infra_provider_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra provider")],
    ) -> GetInfraProviderResponseDto:
        """Get infra provider by uuid"""
        ...

    @delete("/infra-billing/providers/{uuid}", response_class=None)
    async def delete_infra_provider_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra provider")],
    ) -> None:
        """Delete infra provider by uuid (204, без тела)"""
        ...

    @post("/infra-billing/history", response_class=CreateInfraBillingHistoryRecordResponseDto)
    async def create_infra_billing_history_record(
        self,
        body: Annotated[CreateInfraBillingHistoryRecordBodyDto, PydanticBody()],
    ) -> CreateInfraBillingHistoryRecordResponseDto:
        """Create infra billing history"""
        ...

    @get("/infra-billing/history", response_class=GetInfraBillingHistoryRecordsResponseDto)
    async def get_infra_billing_history_records(
        self,
        start: Annotated[
            Optional[int],
            Query(default=None, description="Offset for pagination (default 0)"),
        ] = None,
        size: Annotated[
            Optional[int],
            Query(default=None, ge=1, le=500, description="Page size, 1..500 (default 50)"),
        ] = None,
    ) -> GetInfraBillingHistoryRecordsResponseDto:
        """Get infra billing history"""
        ...

    @delete("/infra-billing/history/{uuid}", response_class=None)
    async def delete_infra_billing_history_record_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the billing history record")],
    ) -> None:
        """Delete infra billing history (204, без тела)"""
        ...

    @get("/infra-billing/nodes", response_class=GetInfraBillingNodesResponseDto)
    async def get_billing_nodes(self) -> GetInfraBillingNodesResponseDto:
        """Get infra billing nodes"""
        ...

    @patch("/infra-billing/nodes", response_class=UpdateInfraBillingNodeResponseDto)
    async def update_infra_billing_node(
        self,
        body: Annotated[UpdateInfraBillingNodeBodyDto, PydanticBody()],
    ) -> UpdateInfraBillingNodeResponseDto:
        """Update infra billing nodes"""
        ...

    @post("/infra-billing/nodes", response_class=CreateInfraBillingNodeResponseDto)
    async def create_infra_billing_node(
        self,
        body: Annotated[CreateInfraBillingNodeBodyDto, PydanticBody()],
    ) -> CreateInfraBillingNodeResponseDto:
        """Create infra billing node"""
        ...

    @delete("/infra-billing/nodes/{uuid}", response_class=None)
    async def delete_infra_billing_node_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra billing node")],
    ) -> None:
        """Delete infra billing node (204, без тела)"""
        ...
