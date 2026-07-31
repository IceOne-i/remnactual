import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, RootModel
from pydantic.alias_generators import to_camel


class UserUsageByRange(BaseModel):
    user_uuid: UUID = Field(alias="userUuid")
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    total: int
    date: datetime.date
    
    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class UserUsageByRangeResponseDto(RootModel[List[UserUsageByRange]]):
    """Список потребления пользователя за период."""

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        return bool(self.root)

    def __len__(self):
        return len(self.root)
