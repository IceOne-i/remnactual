from typing import Annotated

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models.metadata import (
    GetNodeMetadataResponseDto,
    GetUserMetadataResponseDto,
    UpsertNodeMetadataBodyDto,
    UpsertNodeMetadataResponseDto,
    UpsertUserMetadataBodyDto,
    UpsertUserMetadataResponseDto,
)
from remnawave.rapid import BaseController, get, put


class MetadataController(BaseController):
    @get("/metadata/user/{userId}", response_class=GetUserMetadataResponseDto)
    async def get_user_metadata(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="User ID")],
    ) -> GetUserMetadataResponseDto:
        """Get user metadata"""
        ...

    @put("/metadata/user/{userId}", response_class=UpsertUserMetadataResponseDto)
    async def upsert_user_metadata(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="User ID")],
        body: Annotated[UpsertUserMetadataBodyDto, PydanticBody()],
    ) -> UpsertUserMetadataResponseDto:
        """Update or create User Metadata"""
        ...

    @get("/metadata/node/{uuid}", response_class=GetNodeMetadataResponseDto)
    async def get_node_metadata(
        self,
        uuid: Annotated[str, Path(), Field(description="Node UUID")],
    ) -> GetNodeMetadataResponseDto:
        """Get node metadata"""
        ...

    @put("/metadata/node/{uuid}", response_class=UpsertNodeMetadataResponseDto)
    async def upsert_node_metadata(
        self,
        uuid: Annotated[str, Path(), Field(description="Node UUID")],
        body: Annotated[UpsertNodeMetadataBodyDto, PydanticBody()],
    ) -> UpsertNodeMetadataResponseDto:
        """Update or create Node Metadata"""
        ...
