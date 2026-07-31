from datetime import datetime
from functools import partial, wraps
from inspect import signature
from typing import Any, Callable, Coroutine, Type

import httpx
from httpx import AsyncClient, Response
from pydantic import TypeAdapter
from rapid_api_client.typing import BM, T

from remnawave.exceptions import ApiErrorResponse, NetworkError

from .client import BaseController, CustomRapidParameters


def http(
    method: str,
    path: str,
    response_class: Type[BM | str | bytes | Response] | TypeAdapter[T] = Response,
    timeout: float | None = None,
) -> Callable[
    [Callable], Callable[..., Coroutine[Any, Any, BM | str | bytes | Response | T]]
]:
    def decorator(
        func: Callable,
    ) -> Callable[..., Coroutine[Any, Any, BM | str | bytes | Response | T]]:
        sig = signature(func)
        rapid_parameters = CustomRapidParameters.from_sig(sig)

        @wraps(func)
        async def wrapper(
            api: BaseController, *args, **kwargs
        ) -> BM | str | bytes | Response | T:
            assert isinstance(
                api, BaseController
            ), f"{api} should be an instance of BaseController"
            assert isinstance(
                api.client, AsyncClient
            ), f"{api.client} should be an instance of httpx.AsyncClient"

            # noinspection PyProtectedMember
            request = api._build_request(
                sig, rapid_parameters, method, path, (api,) + args, kwargs, timeout
            )
            try:
                response = await api.client.send(request)
            except httpx.RequestError as exc:
                # Соединение/таймаут/DNS — оборачиваем в исключение SDK, чтобы
                # вызывающему не приходилось ловить httpx напрямую.
                raise NetworkError(
                    0,
                    ApiErrorResponse(
                        timestamp=datetime.now(),
                        path=str(request.url.path),
                        message=f"Request error: {exc}",
                        code="NETWORK_ERROR",
                    ),
                ) from exc
            # noinspection PyProtectedMember
            return api._handle_response(response, response_class=response_class)

        return wrapper

    return decorator


get = partial(http, "GET")
post = partial(http, "POST")
delete = partial(http, "DELETE")
put = partial(http, "PUT")
patch = partial(http, "PATCH")
