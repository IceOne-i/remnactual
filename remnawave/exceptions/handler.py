from datetime import datetime
from typing import Dict, Type

import httpx

from remnawave.enums import ErrorCode
from remnawave.enums.error_code import ERROR_HTTP_CODES
from .general import (
    ApiError,
    ApiErrorResponse,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    UnauthorizedError,
    ValidationError,
)

#: Код ошибки -> класс исключения. Сгенерировано из httpCode в контракте
#: (@remnawave/backend-contract, constants/errors/errors.ts), поэтому класс
#: исключения всегда соответствует реальному HTTP-статусу ответа.
ERRORS: Dict[str, Type[ApiError]] = {
    # ---------------- HTTP 400 ----------------
    ErrorCode.USER_USERNAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.USER_SHORT_UUID_ALREADY_EXISTS: BadRequestError,
    ErrorCode.USER_SUBSCRIPTION_UUID_ALREADY_EXISTS: BadRequestError,
    ErrorCode.USER_ALREADY_DISABLED: BadRequestError,
    ErrorCode.USER_ALREADY_ENABLED: BadRequestError,
    ErrorCode.NODE_NAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.NODE_ADDRESS_ALREADY_EXISTS: BadRequestError,
    ErrorCode.HOST_REMARK_ALREADY_EXISTS: BadRequestError,
    ErrorCode.USER_HWID_DEVICE_ALREADY_EXISTS: BadRequestError,
    ErrorCode.USER_HWID_DEVICE_LIMIT_REACHED: BadRequestError,
    ErrorCode.RESERVED_INTERNAL_SQUAD_NAME: BadRequestError,
    ErrorCode.RESERVED_CONFIG_PROFILE_NAME: BadRequestError,
    ErrorCode.NODE_IS_DISABLED: BadRequestError,
    ErrorCode.NAME_OR_CONFIG_REQUIRED: BadRequestError,
    ErrorCode.NAME_OR_INBOUNDS_REQUIRED: BadRequestError,
    ErrorCode.SNIPPET_NAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.SNIPPET_CANNOT_BE_EMPTY: BadRequestError,
    ErrorCode.SNIPPET_CANNOT_CONTAIN_EMPTY_OBJECTS: BadRequestError,
    ErrorCode.RESERVED_TEMPLATE_NAME: BadRequestError,
    ErrorCode.TEMPLATE_JSON_NOT_ALLOWED_FOR_YAML_TEMPLATE: BadRequestError,
    ErrorCode.TEMPLATE_YAML_NOT_ALLOWED_FOR_JSON_TEMPLATE: BadRequestError,
    ErrorCode.TEMPLATE_JSON_AND_YAML_CANNOT_BE_UPDATED_SIMULTANEOUSLY: BadRequestError,
    ErrorCode.TEMPLATE_NAME_ALREADY_EXISTS_FOR_THIS_TYPE: BadRequestError,
    ErrorCode.RESERVED_TEMPLATE_CANNOT_BE_DELETED: BadRequestError,
    ErrorCode.TEMPLATE_TYPE_NOT_ALLOWED: BadRequestError,
    ErrorCode.EXTERNAL_SQUAD_NAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.NAME_OR_TEMPLATES_REQUIRED: BadRequestError,
    ErrorCode.PASSKEYS_NOT_CONFIGURED: BadRequestError,
    ErrorCode.PASSKEYS_NOT_ENABLED: BadRequestError,
    ErrorCode.RESERVED_CONFIG_NAME: BadRequestError,
    ErrorCode.CONFIG_NAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.RESERVED_SUBPAGE_CONFIG_CANT_BE_DELETED: BadRequestError,
    ErrorCode.INVALID_SUBSCRIPTION_PAGE_CONFIG: BadRequestError,
    ErrorCode.INVALID_REMNAWAVE_INJECTOR: BadRequestError,
    ErrorCode.INVALID_NODE_PLUGIN_CONFIG: BadRequestError,
    ErrorCode.NODE_PLUGIN_NAME_ALREADY_EXISTS: BadRequestError,
    ErrorCode.INVALID_API_TOKEN_SCOPE: BadRequestError,
    ErrorCode.CREATE_INFRA_BILLING_NODE_MISSING_TARGET: BadRequestError,
    # ---------------- HTTP 401 ----------------
    ErrorCode.UNAUTHORIZED: UnauthorizedError,
    # ---------------- HTTP 403 ----------------
    ErrorCode.FORBIDDEN_ROLE_ERROR: ForbiddenError,
    ErrorCode.FORBIDDEN: ForbiddenError,
    # ---------------- HTTP 404 ----------------
    ErrorCode.REQUESTED_TOKEN_NOT_FOUND: NotFoundError,
    ErrorCode.NODE_NOT_FOUND: NotFoundError,
    ErrorCode.CONFIG_NOT_FOUND: NotFoundError,
    ErrorCode.USER_NOT_FOUND: NotFoundError,
    ErrorCode.HOST_NOT_FOUND: NotFoundError,
    ErrorCode.USERS_NOT_FOUND: NotFoundError,
    ErrorCode.GET_USER_BY_UNIQUE_FIELDS_NOT_FOUND: NotFoundError,
    ErrorCode.ADMIN_NOT_FOUND: NotFoundError,
    ErrorCode.SUBSCRIPTION_SETTINGS_NOT_FOUND: NotFoundError,
    ErrorCode.INBOUND_NOT_FOUND: NotFoundError,
    ErrorCode.CONFIG_PROFILE_NOT_FOUND: NotFoundError,
    ErrorCode.INTERNAL_SQUAD_NOT_FOUND: NotFoundError,
    ErrorCode.CONFIG_PROFILE_INBOUND_NOT_FOUND_IN_SPECIFIED_PROFILE: NotFoundError,
    ErrorCode.INFRA_PROVIDER_NOT_FOUND: NotFoundError,
    ErrorCode.OAUTH2_PROVIDER_NOT_FOUND: NotFoundError,
    ErrorCode.SNIPPET_NOT_FOUND: NotFoundError,
    ErrorCode.SUBSCRIPTION_TEMPLATE_NOT_FOUND: NotFoundError,
    ErrorCode.EXTERNAL_SQUAD_NOT_FOUND: NotFoundError,
    ErrorCode.PASSKEY_NOT_FOUND: NotFoundError,
    ErrorCode.HWID_DEVICE_NOT_FOUND: NotFoundError,
    ErrorCode.SUBSCRIPTION_PAGE_CONFIG_NOT_FOUND: NotFoundError,
    ErrorCode.JOB_RESULT_FETCH_FAILED: NotFoundError,
    ErrorCode.CONNECTED_NODES_NOT_FOUND: NotFoundError,
    ErrorCode.NODE_PLUGIN_NOT_FOUND: NotFoundError,
    ErrorCode.METADATA_NOT_FOUND: NotFoundError,
    # ---------------- HTTP 409 ----------------
    ErrorCode.ENABLED_NODES_NOT_FOUND: ConflictError,
    ErrorCode.INBOUNDS_WITH_SAME_TAG_ALREADY_EXISTS: ConflictError,
    ErrorCode.CONFIG_PROFILE_NAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.INTERNAL_SQUAD_NAME_ALREADY_EXISTS: ConflictError,
    # ---------------- HTTP 500 ----------------
    ErrorCode.INTERNAL_SERVER_ERROR: ServerError,
    ErrorCode.LOGIN_ERROR: ServerError,
    ErrorCode.CREATE_API_TOKEN_ERROR: ServerError,
    ErrorCode.DELETE_API_TOKEN_ERROR: ServerError,
    ErrorCode.FIND_ALL_API_TOKENS_ERROR: ServerError,
    ErrorCode.GET_PUBLIC_KEY_ERROR: ServerError,
    ErrorCode.ENABLE_NODE_ERROR: ServerError,
    ErrorCode.UPDATE_CONFIG_ERROR: ServerError,
    ErrorCode.GET_CONFIG_ERROR: ServerError,
    ErrorCode.DELETE_MANY_INBOUNDS_ERROR: ServerError,
    ErrorCode.CREATE_MANY_INBOUNDS_ERROR: ServerError,
    ErrorCode.FIND_ALL_INBOUNDS_ERROR: ServerError,
    ErrorCode.CREATE_USER_ERROR: ServerError,
    ErrorCode.CREATE_USER_WITH_INBOUNDS_ERROR: ServerError,
    ErrorCode.CANT_GET_CREATED_USER_WITH_INBOUNDS: ServerError,
    ErrorCode.GET_ALL_USERS_ERROR: ServerError,
    ErrorCode.GET_USER_BY_ERROR: ServerError,
    ErrorCode.REVOKE_USER_SUBSCRIPTION_ERROR: ServerError,
    ErrorCode.DISABLE_USER_ERROR: ServerError,
    ErrorCode.ENABLE_USER_ERROR: ServerError,
    ErrorCode.CREATE_NODE_ERROR: ServerError,
    ErrorCode.RESTART_NODE_ERROR: ServerError,
    ErrorCode.GET_CONFIG_WITH_USERS_ERROR: ServerError,
    ErrorCode.DELETE_USER_ERROR: ServerError,
    ErrorCode.UPDATE_NODE_ERROR: ServerError,
    ErrorCode.UPDATE_USER_ERROR: ServerError,
    ErrorCode.INCREMENT_USED_TRAFFIC_ERROR: ServerError,
    ErrorCode.GET_ALL_NODES_ERROR: ServerError,
    ErrorCode.GET_ONE_NODE_ERROR: ServerError,
    ErrorCode.DELETE_NODE_ERROR: ServerError,
    ErrorCode.CREATE_HOST_ERROR: ServerError,
    ErrorCode.DELETE_HOST_ERROR: ServerError,
    ErrorCode.GET_USER_STATS_ERROR: ServerError,
    ErrorCode.UPDATE_USER_WITH_INBOUNDS_ERROR: ServerError,
    ErrorCode.GET_ALL_HOSTS_ERROR: ServerError,
    ErrorCode.REORDER_HOSTS_ERROR: ServerError,
    ErrorCode.UPDATE_HOST_ERROR: ServerError,
    ErrorCode.CREATE_CONFIG_ERROR: ServerError,
    ErrorCode.GET_NODES_USAGE_BY_RANGE_ERROR: ServerError,
    ErrorCode.RESET_USER_TRAFFIC_ERROR: ServerError,
    ErrorCode.REORDER_NODES_ERROR: ServerError,
    ErrorCode.GET_ALL_INBOUNDS_ERROR: ServerError,
    ErrorCode.BULK_DELETE_USERS_BY_STATUS_ERROR: ServerError,
    ErrorCode.UPDATE_INBOUND_ERROR: ServerError,
    ErrorCode.CONFIG_VALIDATION_ERROR: ServerError,
    ErrorCode.UPDATE_EXCEEDED_TRAFFIC_USERS_ERROR: ServerError,
    ErrorCode.CREATE_ADMIN_ERROR: ServerError,
    ErrorCode.GET_AUTH_STATUS_ERROR: ServerError,
    ErrorCode.DISABLE_NODE_ERROR: ServerError,
    ErrorCode.GET_ONE_HOST_ERROR: ServerError,
    ErrorCode.GET_SUBSCRIPTION_SETTINGS_ERROR: ServerError,
    ErrorCode.UPDATE_SUBSCRIPTION_SETTINGS_ERROR: ServerError,
    ErrorCode.ADD_INBOUND_TO_USERS_ERROR: ServerError,
    ErrorCode.REMOVE_INBOUND_FROM_USERS_ERROR: ServerError,
    ErrorCode.ADD_INBOUND_TO_NODES_ERROR: ServerError,
    ErrorCode.REMOVE_INBOUND_FROM_NODES_ERROR: ServerError,
    ErrorCode.DELETE_HOSTS_ERROR: ServerError,
    ErrorCode.BULK_ENABLE_HOSTS_ERROR: ServerError,
    ErrorCode.BULK_DISABLE_HOSTS_ERROR: ServerError,
    ErrorCode.BULK_DELETE_USERS_BY_UUID_ERROR: ServerError,
    ErrorCode.BULK_REVOKE_USERS_SUBSCRIPTION_ERROR: ServerError,
    ErrorCode.BULK_RESET_USER_TRAFFIC_ERROR: ServerError,
    ErrorCode.BULK_UPDATE_USERS_ERROR: ServerError,
    ErrorCode.BULK_ADD_INBOUNDS_TO_USERS_ERROR: ServerError,
    ErrorCode.BULK_UPDATE_ALL_USERS_ERROR: ServerError,
    ErrorCode.KEYPAIR_CREATION_ERROR: ServerError,
    ErrorCode.GET_USER_USAGE_BY_RANGE_ERROR: ServerError,
    ErrorCode.KEYPAIR_NOT_FOUND: ServerError,
    ErrorCode.ACTIVATE_ALL_INBOUNDS_ERROR: ServerError,
    ErrorCode.GET_NODES_USER_USAGE_BY_RANGE_ERROR: ServerError,
    ErrorCode.CREATE_HWID_USER_DEVICE_ERROR: ServerError,
    ErrorCode.CHECK_HWID_EXISTS_ERROR: ServerError,
    ErrorCode.GET_USER_HWID_DEVICES_ERROR: ServerError,
    ErrorCode.DELETE_HWID_USER_DEVICE_ERROR: ServerError,
    ErrorCode.UPSERT_HWID_USER_DEVICE_ERROR: ServerError,
    ErrorCode.GET_ALL_TAGS_ERROR: ServerError,
    ErrorCode.GETTING_ALL_SUBSCRIPTIONS_ERROR: ServerError,
    ErrorCode.TRIGGER_THRESHOLD_NOTIFICATION_ERROR: ServerError,
    ErrorCode.BULK_DELETE_BY_STATUS_ERROR: ServerError,
    ErrorCode.CLEAN_OLD_USAGE_RECORDS_ERROR: ServerError,
    ErrorCode.VACUUM_TABLE_ERROR: ServerError,
    ErrorCode.GET_CONFIG_PROFILES_ERROR: ServerError,
    ErrorCode.GET_CONFIG_PROFILE_BY_UUID_ERROR: ServerError,
    ErrorCode.CREATE_CONFIG_PROFILE_ERROR: ServerError,
    ErrorCode.GET_INBOUNDS_BY_PROFILE_UUID_ERROR: ServerError,
    ErrorCode.GET_INTERNAL_SQUADS_ERROR: ServerError,
    ErrorCode.GET_INTERNAL_SQUAD_BY_UUID_ERROR: ServerError,
    ErrorCode.CREATE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.UPDATE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.DELETE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.CREATE_USER_WITH_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.GET_USER_ACCESSIBLE_NODES_ERROR: ServerError,
    ErrorCode.GET_INFRA_PROVIDERS_ERROR: ServerError,
    ErrorCode.GET_INFRA_PROVIDER_BY_UUID_ERROR: ServerError,
    ErrorCode.DELETE_INFRA_PROVIDER_BY_UUID_ERROR: ServerError,
    ErrorCode.CREATE_INFRA_PROVIDER_ERROR: ServerError,
    ErrorCode.UPDATE_INFRA_PROVIDER_ERROR: ServerError,
    ErrorCode.CREATE_INFRA_BILLING_HISTORY_RECORD_ERROR: ServerError,
    ErrorCode.GET_INFRA_BILLING_HISTORY_RECORDS_ERROR: ServerError,
    ErrorCode.DELETE_INFRA_BILLING_HISTORY_RECORD_BY_UUID_ERROR: ServerError,
    ErrorCode.GET_BILLING_NODES_ERROR: ServerError,
    ErrorCode.UPDATE_INFRA_BILLING_NODE_ERROR: ServerError,
    ErrorCode.CREATE_INFRA_BILLING_NODE_ERROR: ServerError,
    ErrorCode.DELETE_INFRA_BILLING_NODE_BY_UUID_ERROR: ServerError,
    ErrorCode.GET_BILLING_NODES_FOR_NOTIFICATIONS_ERROR: ServerError,
    ErrorCode.ADD_USERS_TO_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.INTERNAL_SQUAD_BULK_ACTIONS_ERROR: ServerError,
    ErrorCode.REMOVE_USERS_FROM_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.DELETE_CONFIG_PROFILE_BY_UUID_ERROR: ServerError,
    ErrorCode.UPDATE_CONFIG_PROFILE_ERROR: ServerError,
    ErrorCode.OAUTH2_AUTHORIZE_ERROR: ServerError,
    ErrorCode.SYNC_ACTIVE_PROFILE_ERROR: ServerError,
    ErrorCode.GET_ALL_HOST_TAGS_ERROR: ServerError,
    ErrorCode.GET_INTERNAL_SQUAD_ACCESSIBLE_NODES_ERROR: ServerError,
    ErrorCode.DELETE_HWID_USER_DEVICES_ERROR: ServerError,
    ErrorCode.CREATE_USER_SUBSCRIPTION_REQUEST_HISTORY_ERROR: ServerError,
    ErrorCode.GET_USER_SUBSCRIPTION_REQUEST_HISTORY_ERROR: ServerError,
    ErrorCode.GET_ALL_HWID_DEVICES_ERROR: ServerError,
    ErrorCode.GET_HWID_DEVICES_STATS_ERROR: ServerError,
    ErrorCode.GET_USER_SUBSCRIPTION_REQUEST_HISTORY_STATS_ERROR: ServerError,
    ErrorCode.GET_SNIPPETS_ERROR: ServerError,
    ErrorCode.DELETE_SNIPPET_BY_NAME_ERROR: ServerError,
    ErrorCode.UPDATE_SNIPPET_ERROR: ServerError,
    ErrorCode.GET_ALL_SUBSCRIPTION_TEMPLATES_ERROR: ServerError,
    ErrorCode.GET_SUBSCRIPTION_TEMPLATE_BY_UUID_ERROR: ServerError,
    ErrorCode.UPDATE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.DELETE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.CREATE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.GET_EXTERNAL_SQUADS_ERROR: ServerError,
    ErrorCode.CREATE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.UPDATE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.DELETE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.ADD_USERS_TO_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.REMOVE_USERS_FROM_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.GET_EXTERNAL_SQUAD_BY_UUID_ERROR: ServerError,
    ErrorCode.GET_REMNAAWAVE_SETTINGS_ERROR: ServerError,
    ErrorCode.UPDATE_REMNAAWAVE_SETTINGS_ERROR: ServerError,
    ErrorCode.GENERATE_PASSKEY_REGISTRATION_OPTIONS: ServerError,
    ErrorCode.VERIFY_PASSKEY_REGISTRATION_ERROR: ServerError,
    ErrorCode.GET_ACTIVE_PASSKEYS_ERROR: ServerError,
    ErrorCode.DELETE_PASSKEY_ERROR: ServerError,
    ErrorCode.GET_COMPUTED_CONFIG_PROFILE_BY_UUID_ERROR: ServerError,
    ErrorCode.RESET_NODE_TRAFFIC_ERROR: ServerError,
    ErrorCode.UPDATE_PASSKEY_ERROR: ServerError,
    ErrorCode.GENERIC_REORDER_ERROR: ServerError,
    ErrorCode.BULK_EXTEND_EXPIRATION_DATE_ERROR: ServerError,
    ErrorCode.GET_SUBSCRIPTION_PAGE_CONFIG_BY_UUID_ERROR: ServerError,
    ErrorCode.GET_ALL_SUBSCRIPTION_PAGE_CONFIGS_ERROR: ServerError,
    ErrorCode.UPDATE_SUBSCRIPTION_PAGE_CONFIG_ERROR: ServerError,
    ErrorCode.DELETE_SUBSCRIPTION_PAGE_CONFIG_ERROR: ServerError,
    ErrorCode.CREATE_SUBSCRIPTION_PAGE_CONFIG_ERROR: ServerError,
    ErrorCode.JOB_CREATION_FAILED: ServerError,
    ErrorCode.GET_NODE_PLUGIN_BY_UUID_ERROR: ServerError,
    ErrorCode.UPDATE_NODE_PLUGIN_ERROR: ServerError,
    ErrorCode.CREATE_NODE_PLUGIN_ERROR: ServerError,
    ErrorCode.GET_TORRENT_BLOCKER_REPORTS_ERROR: ServerError,
    ErrorCode.UPDATE_HOSTS_ERROR: ServerError,
    ErrorCode.NODE_ERROR_WITH_MSG: ServerError,
    ErrorCode.NODE_ERROR_500_WITH_MSG: ServerError,
}


def handle_api_error(response: httpx.Response) -> None:
    """Handle API error responses and raise appropriate exceptions.

    Всегда возбуждает исключение для не-2xx ответов: молчаливый возврат приводил
    к тому, что на 3xx вызывающий код продолжал разбирать пустое тело ответа.
    """
    if 200 <= response.status_code < 300:
        return

    try:
        error_data = response.json()
    except ValueError:
        raise ApiError(
            response.status_code,
            ApiErrorResponse(
                timestamp=datetime.now(),
                path=str(response.request.url.path),
                message=f"Unknown error: {response.text}",
                code="UNKNOWN",
                status_code=response.status_code,
            ),
        )

    try:
        error_response = ApiErrorResponse(**error_data)
    except Exception:
        raise ApiError(
            response.status_code,
            ApiErrorResponse(
                timestamp=datetime.now(),
                path=str(response.request.url.path),
                message=f"Unexpected error payload: {response.text}",
                code="UNKNOWN",
                status_code=response.status_code,
            ),
        )

    # Дозаполняем поля, которых нет в ответе API v2
    if error_response.timestamp is None:
        error_response.timestamp = datetime.now()
    if error_response.path is None:
        error_response.path = str(response.request.url.path)
    if error_response.status_code is None:
        error_response.status_code = response.status_code
    if error_response.code is None:
        error_response.code = f"HTTP_{response.status_code}"

    exception_class = ERRORS.get(
        error_response.code, _get_exception_by_status_code(response.status_code)
    )
    raise exception_class(response.status_code, error_response)


def get_http_code(error_code: str) -> int | None:
    """HTTP-статус, объявленный контрактом для данного кода ошибки."""
    return ERROR_HTTP_CODES.get(str(error_code))


def _get_exception_by_status_code(status_code: int) -> Type[ApiError]:
    """Get exception class based on HTTP status code"""
    if status_code == 400:
        return BadRequestError
    elif status_code == 401:
        return UnauthorizedError
    elif status_code == 403:
        return ForbiddenError
    elif status_code == 404:
        return NotFoundError
    elif status_code == 409:
        return ConflictError
    elif status_code == 422:
        return ValidationError
    elif status_code == 429:
        return RateLimitError
    elif status_code >= 500:
        return ServerError
    else:
        return ApiError
