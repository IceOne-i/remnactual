from typing import Annotated

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateConfigProfileBodyDto,
    CreateConfigProfileResponseDto,
    GetAllInboundsResponseDto,
    GetComputedConfigProfileByUuidResponseDto,
    GetConfigProfileByUuidResponseDto,
    GetConfigProfilesResponseDto,
    GetInboundsByProfileUuidResponseDto,
    ReorderConfigProfilesBodyDto,
    ReorderConfigProfilesResponseDto,
    UpdateConfigProfileBodyDto,
    UpdateConfigProfileResponseDto,
)
from remnawave.models.tags import (
    GetEntityTagsResponseDto,
    SetEntityTagsBodyDto,
    SetEntityTagsResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class ConfigProfilesController(BaseController):
    @get("/config-profiles", response_class=GetConfigProfilesResponseDto)
    async def get_config_profiles(self) -> GetConfigProfilesResponseDto:
        """Get config profiles"""
        ...

    @post("/config-profiles", response_class=CreateConfigProfileResponseDto)
    async def create_config_profile(
        self,
        body: Annotated[CreateConfigProfileBodyDto, PydanticBody()],
    ) -> CreateConfigProfileResponseDto:
        """Create config profile"""
        ...

    @patch("/config-profiles", response_class=UpdateConfigProfileResponseDto)
    async def update_config_profile(
        self,
        body: Annotated[UpdateConfigProfileBodyDto, PydanticBody()],
    ) -> UpdateConfigProfileResponseDto:
        """Update Core Config in specific config profile"""
        ...

    @get("/config-profiles/inbounds", response_class=GetAllInboundsResponseDto)
    async def get_all_inbounds(self) -> GetAllInboundsResponseDto:
        """Get all inbounds from all config profiles"""
        ...

    @get("/config-profiles/{uuid}/inbounds", response_class=GetInboundsByProfileUuidResponseDto)
    async def get_inbounds_by_profile_uuid(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the config profile")],
    ) -> GetInboundsByProfileUuidResponseDto:
        """Get inbounds by profile uuid"""
        ...

    @get("/config-profiles/{uuid}", response_class=GetConfigProfileByUuidResponseDto)
    async def get_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the config profile")],
    ) -> GetConfigProfileByUuidResponseDto:
        """Get config profile by uuid"""
        ...

    @delete("/config-profiles/{uuid}", response_class=None)
    async def delete_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the config profile")],
    ) -> None:
        """Delete config profile

        Отвечает ``204 No Content`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @post("/config-profiles/actions/reorder", response_class=ReorderConfigProfilesResponseDto)
    async def reorder_config_profiles(
        self,
        body: Annotated[ReorderConfigProfilesBodyDto, PydanticBody()],
    ) -> ReorderConfigProfilesResponseDto:
        """Reorder config profiles"""
        ...

    # Get computed config profile by uuid​
    @get(
        "/config-profiles/{uuid}/computed-config",
        response_class=GetComputedConfigProfileByUuidResponseDto,
    )
    async def get_computed_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(), Field(description="UUID of the config profile")],
    ) -> GetComputedConfigProfileByUuidResponseDto:
        """Get computed config profile by uuid"""
        ...

    @get("/config-profiles/tags", response_class=GetEntityTagsResponseDto)
    async def get_tags(self) -> GetEntityTagsResponseDto:
        """Get tags of Config Profiles (панель 3.4.0+)

        Отдаёт ВСЕ метки, встречающиеся у сущностей этого вида, а не метки
        одной из них: у конкретной они лежат в её собственном поле ``tags``.
        """
        ...

    @patch("/config-profiles/tags", response_class=SetEntityTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetEntityTagsBodyDto, PydanticBody()],
    ) -> SetEntityTagsResponseDto:
        """Set tags of Config Profile (панель 3.4.0+)

        ЗАМЕНЯЕТ набор меток целиком: пустой список снимает все.
        """
        ...
