from remnawave.models.keygen import GetNodeSecretKeyResponseDto
from remnawave.rapid import BaseController, get


class KeygenController(BaseController):
    @get("/keygen", response_class=GetNodeSecretKeyResponseDto)
    async def generate_key(
        self,
    ) -> GetNodeSecretKeyResponseDto:
        """Get SECRET_KEY for Remnawave Node"""
        ...
