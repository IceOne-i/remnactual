"""Offline checks for backend tag 3.4.4 (contract 3.4.15)."""
import json
from uuid import UUID

import httpx
import pytest
from pydantic import ValidationError

from remnawave import RemnawaveSDK
from remnawave.enums import ErrorCode, Scope
from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES
from tests.test_3_3_compliance import HOST_PAYLOAD


async def test_clone_host_request_and_response():
    from remnawave.models import CloneHostBodyDto, HostResponseDto

    source = UUID("b1f0e2b4-1f5c-4c9a-9b2e-2f2f6a7c8d90")

    def respond(request):
        assert request.method == "POST"
        assert request.url.path == "/api/hosts/actions/clone"
        assert json.loads(request.content) == {"cloneFromUuid": str(source)}
        return httpx.Response(201, json={"response": HOST_PAYLOAD})

    async with httpx.AsyncClient(
        base_url="https://panel.example/api", transport=httpx.MockTransport(respond)
    ) as client:
        sdk = RemnawaveSDK(client=client)
        result = await sdk.hosts.clone_host(CloneHostBodyDto(clone_from_uuid=source))
        assert isinstance(result, HostResponseDto)
        assert result.uuid == UUID(HOST_PAYLOAD["uuid"])

    assert CloneHostBodyDto(cloneFromUuid=str(source)).clone_from_uuid == source
    with pytest.raises(ValidationError):
        CloneHostBodyDto(clone_from_uuid="invalid")


def test_clone_host_scope_and_error():
    assert Scope.HOSTS_CLONE == "hosts:clone"
    assert ErrorCode.CLONE_HOST_ERROR == "A258"
    assert ERROR_HTTP_CODES["A258"] == 500
    assert ERROR_MESSAGES["A258"] == "Clone host error"
