from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models._serialization import AlwaysEmitModel


class InfraProviderSimpleDto(BaseModel):
    """Упрощенная модель провайдера (PartialInfraProviderSchema.pick)"""
    uuid: UUID
    name: str
    login_url: Optional[str] = Field(alias="loginUrl")
    favicon_link: Optional[str] = Field(alias="faviconLink")


class InfraProviderRecordDto(BaseModel):
    """Провайдер внутри записи истории биллинга (без createdAt/updatedAt/loginUrl)"""
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(alias="faviconLink")


class InfraBillingHistoryStatsDto(BaseModel):
    """Статистика истории биллинга для провайдера"""
    total_amount: float = Field(alias="totalAmount")
    total_bills: float = Field(alias="totalBills")


class InfraProviderBillingNodeDetailsDto(BaseModel):
    """Привязка billing node к реальной ноде. `null` для кастомной billing node."""
    node_uuid: UUID = Field(alias="nodeUuid")
    country_code: str = Field(alias="countryCode")


class InfraBillingNodeSimpleDto(BaseModel):
    """Элемент `billingNodes` в модели провайдера"""
    name: str
    details: Optional[InfraProviderBillingNodeDetailsDto] = None


class InfraProviderDto(BaseModel):
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    billing_history: InfraBillingHistoryStatsDto = Field(alias="billingHistory")
    billing_nodes: List[InfraBillingNodeSimpleDto] = Field(alias="billingNodes")


class InfraBillingNodeRefDto(BaseModel):
    """Ссылка на ноду внутри billing node (NodesSchema.pick)"""
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class InfraBillingHistoryDto(BaseModel):
    uuid: UUID
    provider_uuid: UUID = Field(alias="providerUuid")
    amount: float
    billed_at: datetime = Field(alias="billedAt")
    provider: InfraProviderRecordDto


class InfraBillingNodeDto(BaseModel):
    uuid: UUID
    node_uuid: Optional[UUID] = Field(None, alias="nodeUuid")
    name: Optional[str] = None
    provider_uuid: UUID = Field(alias="providerUuid")
    provider: InfraProviderSimpleDto
    node: Optional[InfraBillingNodeRefDto] = None
    next_billing_at: datetime = Field(alias="nextBillingAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class AvailableBillingNodeDto(BaseModel):
    """Модель для доступных узлов биллинга"""
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class BillingStatsDto(BaseModel):
    """Статистика биллинга"""
    upcoming_nodes_count: float = Field(alias="upcomingNodesCount")
    current_month_payments: float = Field(alias="currentMonthPayments")
    total_spent: float = Field(alias="totalSpent")


# Provider models
class CreateInfraProviderBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class CreateInfraProviderResponseDto(InfraProviderDto):
    pass


class UpdateInfraProviderBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class UpdateInfraProviderResponseDto(InfraProviderDto):
    pass


class AllInfraProvidersData(BaseModel):
    total: float = Field(alias="total")
    providers: List[InfraProviderDto]


# Исправленные имена моделей согласно OpenAPI
class GetInfraProvidersResponseDto(AllInfraProvidersData):
    pass


class GetInfraProviderResponseDto(InfraProviderDto):
    pass


# 3.0: DELETE /infra-billing/providers/{uuid} отвечает 204 без тела,
# поэтому модели ответа больше нет.


# Billing History models
class CreateInfraBillingHistoryRecordBodyDto(BaseModel):
    """Модель для создания записи истории биллинга"""
    model_config = ConfigDict(populate_by_name=True)

    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    amount: float = Field(ge=0)
    billed_at: datetime = Field(serialization_alias="billedAt")


class InfraBillingHistoryData(BaseModel):
    records: List[InfraBillingHistoryDto]
    total: float


# POST /infra-billing/history (201) возвращает обновлённый список записей,
# а не одну созданную запись.
class CreateInfraBillingHistoryRecordResponseDto(InfraBillingHistoryData):
    pass


class GetInfraBillingHistoryRecordsResponseDto(InfraBillingHistoryData):
    pass


# 3.0: DELETE /infra-billing/history/{uuid} отвечает 204 без тела.


# Billing Nodes models
class CreateInfraBillingNodeBodyDto(AlwaysEmitModel):
    """`nodeUuid` и `name` обязательны в теле запроса, но могут быть `null`
    (кастомная billing node не привязана к реальной ноде), поэтому оба ключа
    отправляются всегда — даже если вызывающий их не задал."""
    __always_emit__ = ("node_uuid", "name")

    model_config = ConfigDict(populate_by_name=True)

    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    node_uuid: Optional[UUID] = Field(None, serialization_alias="nodeUuid")
    name: Optional[Annotated[str, StringConstraints(min_length=1, max_length=255)]] = None
    next_billing_at: datetime = Field(serialization_alias="nextBillingAt")


class InfraBillingNodesData(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: List[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: List[AvailableBillingNodeDto] = Field(alias="availableBillingNodes")
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


# API возвращает список всех billing nodes после создания (201), а не один созданный
class CreateInfraBillingNodeResponseDto(InfraBillingNodesData):
    pass


class UpdateInfraBillingNodeBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuids: List[UUID]
    next_billing_at: datetime = Field(serialization_alias="nextBillingAt")


class UpdateInfraBillingNodeResponseDto(InfraBillingNodesData):
    pass


class GetInfraBillingNodesResponseDto(InfraBillingNodesData):
    pass


# 3.0: DELETE /infra-billing/nodes/{uuid} отвечает 204 без тела.


# Legacy aliases для обратной совместимости
NodeDto = InfraBillingNodeRefDto
CreateInfraProviderRequestDto = CreateInfraProviderBodyDto
UpdateInfraProviderRequestDto = UpdateInfraProviderBodyDto
CreateInfraBillingHistoryRecordRequestDto = CreateInfraBillingHistoryRecordBodyDto
CreateInfraBillingNodeRequestDto = CreateInfraBillingNodeBodyDto
UpdateInfraBillingNodeRequestDto = UpdateInfraBillingNodeBodyDto
GetInfraProviderByUuidResponseDto = GetInfraProviderResponseDto
GetAllInfraProvidersResponseDto = GetInfraProvidersResponseDto
GetAllInfraBillingHistoryResponseDto = GetInfraBillingHistoryRecordsResponseDto
GetInfraBillingHistoryByUuidResponseDto = InfraBillingHistoryDto
GetAllInfraBillingNodesResponseDto = GetInfraBillingNodesResponseDto
GetInfraBillingNodeByUuidResponseDto = InfraBillingNodeDto
