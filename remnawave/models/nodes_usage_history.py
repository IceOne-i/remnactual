from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NodeActiveSquadDto(BaseModel):
    squad_name: str = Field(alias="squadName")
    active_inbounds: list[str] = Field(alias="activeInbounds")


class NodeInfoDto(BaseModel):
    uuid: UUID
    name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    config_profile_name: str = Field(alias="configProfileName")
    config_profile_uuid: UUID = Field(alias="configProfileUuid")
    active_squads: List[NodeActiveSquadDto] = Field(alias="activeSquads")


class GetUserAccessibleNodesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    active_nodes: List[NodeInfoDto] = Field(default_factory=list, alias="activeNodes")

    @property
    def nodes(self) -> List[NodeInfoDto]:
        """Устаревшее имя поля до 2.8 — API отдаёт `activeNodes`."""
        return self.active_nodes


class GetUserAccessibleNodesResponseDto(GetUserAccessibleNodesResponse):
    pass
