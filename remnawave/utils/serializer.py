from pydantic import BaseModel


def orjson_default(obj):
    if isinstance(obj, BaseModel):
        # Mirrors the PydanticBody serialization in remnawave.rapid.client: send exactly the
        # fields the caller set, so an explicit `null` reaches the API instead of being dropped.
        return obj.model_dump(mode="json", exclude_unset=True, by_alias=True)
    return obj
