from pydantic import BaseModel, ConfigDict, Field


class SecretKeyData(BaseModel):
    """SECRET_KEY выдаваемый панелью для Remnawave Node.

    3.0: `response.pubKey` переименован в `response.secretKey`."""
    model_config = ConfigDict(populate_by_name=True)

    secret_key: str = Field(alias="secretKey")


class GetNodeSecretKeyResponseDto(SecretKeyData):
    """Get SECRET_KEY for Remnawave Node"""
    pass


# Legacy aliases (имена 2.8; поле теперь `secret_key`/`secretKey`)
PubKeyData = SecretKeyData
PubKeyResponseDto = SecretKeyData
GetPubKeyResponseDto = GetNodeSecretKeyResponseDto
