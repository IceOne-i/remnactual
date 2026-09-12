from __future__ import annotations

from dataclasses import replace
from http import HTTPStatus
from inspect import BoundArguments, Signature
from typing import Any, Dict, Mapping, Optional, Self, Tuple, Type, TypeVar

import httpx
import orjson
from httpx import Request, Response
from pydantic import BaseModel, RootModel, TypeAdapter
from pydantic.fields import FieldInfo
from rapid_api_client import (
    Body,
    FileBody,
    FormBody,
    PydanticBody,
    PydanticXmlBody,
    RapidApi,
)
from rapid_api_client.annotations import Header, JsonBody, Path, Query
from rapid_api_client.parameters import RapidParameter, ParameterManager
from rapid_api_client.xml import pydantic_xml
from rapid_api_client.utils import T
from rapid_api_client.utils import filter_none_values, find_annotation

from remnawave.exceptions import handle_api_error
from remnawave.rapid import AttributeBody
from remnawave.utils.serializer import orjson_default


BM = TypeVar("BM", bound=BaseModel)


class BaseController(RapidApi):
    def __init__(self, client: httpx.AsyncClient):
        super().__init__(async_client=client)
        self.client = client

    def _build_request(
        self,
        sig: Signature,
        rapid_parameters: CustomRapidParameters,
        method: str,
        path: str,
        args: Tuple[Any],
        kwargs: Mapping[str, Any],
        timeout: float | None,
    ) -> Request:
        ba = sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()

        path = rapid_parameters.get_resolved_path(path, ba)

        build_kwargs: Dict[str, Any] = {
            "headers": rapid_parameters.get_headers(ba),
            "params": rapid_parameters.get_query(ba),
        }
        post_kw, post_data = rapid_parameters.get_body(ba)
        if post_kw is not None:
            build_kwargs[post_kw] = post_data

        if timeout is not None:
            build_kwargs["timeout"] = timeout

        return self.client.build_request(method, path, **build_kwargs)

    def _handle_response(
        self,
        response: Response,
        response_class: Optional[Type[Response | str | bytes | BM] | TypeAdapter[T]] = Response,
    ) -> Optional[Response | str | bytes | BM | T]:
        # Ошибки разбираем ДО короткого замыкания на сырой Response, иначе
        # эндпоинт без явного response_class молча вернул бы 4xx/5xx как объект.
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            handle_api_error(e.response)

        # 3.0: 204 No Content и 202 Accepted приходят с пустым телом.
        # `response_class=None` — явное объявление такого эндпоинта в контроллере.
        if response_class is None or response.status_code in (
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ):
            return None

        if response_class is Response:
            return response

        if response_class is str:
            return response.text
        if response_class is bytes:
            return response.content
        if isinstance(response_class, TypeAdapter):
            return response_class.validate_json(response.content)
        if pydantic_xml is not None and issubclass(
            response_class, pydantic_xml.BaseXmlModel
        ):
            return response_class.from_xml(response.content)
        if issubclass(response_class, BaseModel):
            data = response.json()
            
            # Check if this is a RootModel (list response)
            if issubclass(response_class, RootModel):
                # This is a RootModel - needs the list data, not the wrapper
                if isinstance(data, dict) and "response" in data:
                    return response_class.model_validate(data["response"])
                else:
                    # API returns list directly
                    return response_class.model_validate(data)
            else:
                # This is a regular BaseModel
                # Auto-unwrap single response field for convenience
                if (isinstance(data, dict) and 
                    len(data) == 1 and 
                    "response" in data and
                    hasattr(response_class, 'model_fields') and 
                    len(response_class.model_fields) == 1 and
                    'response' in response_class.model_fields):
                    # This is a wrapper model with single "response" field
                    # Return the inner data directly for convenience
                    inner_field = response_class.model_fields['response']
                    inner_type = inner_field.annotation
                    
                    # If it's a simple type annotation, use it directly
                    if hasattr(inner_type, 'model_validate'):
                        return inner_type.model_validate(data["response"])
                    else:
                        # Fallback to original behavior
                        return response_class.model_validate(data)
                elif hasattr(response_class, 'model_fields') and 'response' in response_class.model_fields:
                    # Model expects full data with response wrapper
                    return response_class.model_validate(data)
                elif isinstance(data, dict) and "response" in data:
                    # Extract response data for models that don't expect wrapper
                    return response_class.model_validate(data["response"])
                else:
                    # API returns data directly (no wrapper)
                    return response_class.model_validate(data)
        raise ValueError(f"Response class not supported: {response_class}")


class CustomRapidParameters(ParameterManager):
    @classmethod
    def from_sig(cls, sig: Signature) -> Self:
        out = cls()
        for parameter in sig.parameters.values():
            field = find_annotation(parameter, FieldInfo)
            if (annot := find_annotation(parameter, Path)) is not None:
                out.path_parameters.append(RapidParameter(parameter, annot, field))
            if (annot := find_annotation(parameter, Query)) is not None:
                # Let HTTPX encode booleans and repeated query values.
                annot = replace(annot, transformer=lambda value: value)
                out.query_parameters.append(RapidParameter(parameter, annot, field))
            if (annot := find_annotation(parameter, Header)) is not None:
                out.header_parameters.append(RapidParameter(parameter, annot, field))
            if (annot := find_annotation(parameter, Body)) is not None:
                if isinstance(annot, (PydanticBody, PydanticXmlBody)):
                    # Serialize below, preserving explicit null and unset fields.
                    annot = replace(annot, transformer=lambda value: value)
                out.body_parameters.append(RapidParameter(parameter, annot, field))

        if len(out.body_parameters) > 0:
            first_body_param = out.body_parameters[0]
            if isinstance(first_body_param.rapid_annotation, FileBody):
                assert all(
                    map(lambda p: isinstance(p.rapid_annotation, FileBody), out.body_parameters)
                ), "All body parameters must be of type FileBody"
            elif isinstance(first_body_param.rapid_annotation, FormBody):
                assert all(
                    map(lambda p: isinstance(p.rapid_annotation, FormBody), out.body_parameters)
                ), "All body parameters must be of type FormBody"
            elif isinstance(first_body_param.rapid_annotation, JsonBody):
                assert len(out.body_parameters) == 1, "Only one JsonBody allowed"
            elif isinstance(first_body_param.rapid_annotation, Body) and not isinstance(
                first_body_param.rapid_annotation,
                AttributeBody,  # don't check the AttributeBody because there can be more than one
            ):
                assert (
                    len(out.body_parameters) == 1
                ), "Only one Body (JsonBody, FormBody, PydanticBody, FileBody, PydanticXmlBody) allowed"

        return out

    def get_body(self, ba: BoundArguments) -> Tuple[str | None, Any]:
        """
        Prepares the body of an HTTP request based on annotated parameters.

        For parameters annotated with `AttributeBody`, collects them into a dictionary,
        serializes them into JSON with custom type processing via `orjson`, and returns
        the result as `("json", dict)`. Supports other body types like `FileBody`,
        `FormBody`, `PydanticBody`, etc., with appropriate serialization.

        Args:
            ba (BoundArguments): Bound arguments of the function containing parameter values.

        Returns:
            Tuple[str | None, Any]: A tuple of (body_type, body_data), where body_type
                indicates the content type (e.g., "json", "files") and body_data is the
                serialized content, or (None, None) if no body is constructed.
        """

        if len(self.body_parameters) > 0:
            first_body_param = self.body_parameters[0]
            if isinstance(first_body_param.rapid_annotation, FileBody):
                values = filter_none_values(
                    {p.get_name(): p.get_value(ba) for p in self.body_parameters}
                )
                if len(values) > 0:
                    return "files", values
            elif isinstance(first_body_param.rapid_annotation, FormBody):
                values = {}

                def update_values(p: RapidParameter[Body]) -> None:
                    if (value := p.get_value(ba)) is not None:
                        if isinstance(value, dict):
                            values.update(value)
                        else:
                            values[p.get_name()] = value

                for param in self.body_parameters:
                    update_values(param)

                if len(values) > 0:
                    return "data", values
            elif isinstance(first_body_param.rapid_annotation, PydanticXmlBody):
                assert (
                    pydantic_xml is not None
                ), "pydantic-xml must be installed to use PydanticXmlBody"
                if (value := first_body_param.get_value(ba)) is not None:
                    assert isinstance(value, pydantic_xml.BaseXmlModel)
                    return "content", value.to_xml()
            elif isinstance(first_body_param.rapid_annotation, PydanticBody):
                if (value := first_body_param.get_value(ba)) is not None:
                    assert isinstance(value, BaseModel)
                    # `exclude_unset` (not `exclude_none`): the API distinguishes an absent key
                    # from an explicit `null`, and since 2.8 several nullable fields can only be
                    # cleared by sending `null`. Sending exactly what the caller set preserves
                    # that distinction; server-side defaults cover the fields left untouched.
                    return "json", value.model_dump(
                        exclude_unset=True, by_alias=True, mode="json"
                    )
            elif isinstance(first_body_param.rapid_annotation, JsonBody):
                if (value := first_body_param.get_value(ba)) is not None:
                    assert isinstance(value, dict)
                    return "json", value
            elif isinstance(first_body_param.rapid_annotation, AttributeBody):
                body: dict[str, Any] = {}
                for param in self.body_parameters:
                    if (value := param.get_value(ba)) is not None:
                        param_name: str = param.get_name()
                        body[param_name] = value
                if body:
                    return "json", orjson.loads(
                        orjson.dumps(body, default=orjson_default)
                    )
            else:
                if (value := first_body_param.get_value(ba)) is not None:
                    return "content", value

        return None, None
