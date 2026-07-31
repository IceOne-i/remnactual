from datetime import datetime
from typing import Annotated, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_serializer

from remnawave.enums import (
    ResponseRuleConditionOperator,
    ResponseRuleOperator,
    ResponseRuleVersion,
    ResponseType,
    SubscriptionType,
)


class ResponseRuleCondition(BaseModel):
    """Condition to check against request headers"""
    model_config = ConfigDict(populate_by_name=True)

    header_name: Annotated[str, StringConstraints(pattern=r"^[!#$%&'*+\-.0-9A-Z^_`a-z|~]+$")] = Field(
        alias="headerName"
    )
    operator: ResponseRuleConditionOperator
    value: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    case_sensitive: bool = Field(alias="caseSensitive")


class ResponseModificationHeader(BaseModel):
    """Response header modification"""
    model_config = ConfigDict(populate_by_name=True)

    key: Annotated[str, StringConstraints(pattern=r"^[!#$%&'*+\-.0-9A-Z^_`a-z|~]+$")]
    value: Annotated[str, StringConstraints(min_length=1)]


class ResponseRuleEncryption(BaseModel):
    """Шифрование тела ответа (2.8, age-encryption)"""
    model_config = ConfigDict(populate_by_name=True)

    method: Literal["age1", "age1pq1"]
    key: str


class ResponseModifications(BaseModel):
    """Response modifications to apply when rule matches"""
    model_config = ConfigDict(populate_by_name=True)

    headers: Optional[List[ResponseModificationHeader]] = None
    apply_headers_to_end: Optional[bool] = Field(
        None,
        alias="applyHeadersToEnd",
        description=(
            "If True, SRR headers are appended at the very end of the response "
            "and may override headers from other sections."
        ),
    )
    subscription_template: Optional[Annotated[str, StringConstraints(min_length=1)]] = Field(
        None, alias="subscriptionTemplate"
    )
    ignore_host_xray_json_template: Optional[bool] = Field(
        None,
        alias="ignoreHostXrayJsonTemplate",
        description=(
            "If True, the Host's own Xray Json Template is ignored and the "
            "template defined by the SRR rule is used instead."
        ),
    )
    ignore_serve_json_at_base_subscription: Optional[bool] = Field(
        None,
        alias="ignoreServeJsonAtBaseSubscription",
        description=(
            "If True, the Serve JSON at Base Subscription setting is ignored "
            "(treated as False)."
        ),
    )
    additional_extended_clients_regex: Optional[
        List[Annotated[str, StringConstraints(min_length=1)]]
    ] = Field(
        None,
        alias="additionalExtendedClientsRegex",
        description=(
            "Дополнительные regex-паттерны расширенных клиентов; таким клиентам "
            "в ответе подписки отдаётся serverDescription."
        ),
    )
    disable_hwid_check: Optional[bool] = Field(
        None,
        alias="disableHwidCheck",
        description=(
            "If True, HWID check is disabled. Приоритетнее настроек Subscription Settings."
        ),
    )
    encryption: Optional[ResponseRuleEncryption] = Field(
        None,
        description="Шифрование тела ответа (age1 | age1pq1).",
    )
    exclude_hosts_by_tags: Optional[
        List[Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]]
    ] = Field(
        None,
        alias="excludeHostsByTags",
        min_length=1,
        description="Исключает хосты из выдачи подписки, если хотя бы один их тег совпал.",
    )


class ResponseRule(BaseModel):
    """Individual response rule configuration"""
    model_config = ConfigDict(populate_by_name=True)

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    description: Optional[Annotated[str, StringConstraints(min_length=1, max_length=250)]] = None
    enabled: bool
    operator: ResponseRuleOperator
    conditions: List[ResponseRuleCondition]
    response_type: ResponseType = Field(alias="responseType")
    response_modifications: Optional[ResponseModifications] = Field(
        None, alias="responseModifications"
    )


class ResponseRulesSettings(BaseModel):
    """Settings for response rules"""
    model_config = {"populate_by_name": True}

    disable_subscription_access_by_path: Optional[bool] = Field(
        None, alias="disableSubscriptionAccessByPath"
    )


class ResponseRules(BaseModel):
    """Response rules configuration"""
    model_config = ConfigDict(populate_by_name=True)

    version: ResponseRuleVersion
    rules: List[ResponseRule]
    settings: Optional[ResponseRulesSettings] = None


class CustomRemarksDto(BaseModel):
    """Custom remarks for different user states"""
    model_config = ConfigDict(populate_by_name=True)

    expired_users: List[str] = Field(alias="expiredUsers", min_length=1)
    limited_users: List[str] = Field(alias="limitedUsers", min_length=1)
    disabled_users: List[str] = Field(alias="disabledUsers", min_length=1)
    empty_hosts: List[str] = Field(alias="emptyHosts", min_length=1)
    hwid_max_devices_exceeded: List[str] = Field(alias="HWIDMaxDevicesExceeded", min_length=1)
    hwid_not_supported: List[str] = Field(alias="HWIDNotSupported", min_length=1)


class HwidSettingsDto(BaseModel):
    """HWID (Hardware ID) settings.

    `maxDevicesAnnounce` обязателен в теле запроса, но может быть `null`,
    поэтому ключ отправляется всегда."""
    model_config = ConfigDict(populate_by_name=True)

    enabled: bool
    fallback_device_limit: int = Field(alias="fallbackDeviceLimit")
    max_devices_announce: Optional[Annotated[str, StringConstraints(max_length=200)]] = Field(
        None, alias="maxDevicesAnnounce"
    )

    @model_serializer(mode="wrap")
    def _always_emit_announce(self, handler, info):
        data = handler(self)
        data.setdefault(
            "maxDevicesAnnounce" if info.by_alias else "max_devices_announce",
            self.max_devices_announce,
        )
        return data

class SubscriptionSettingsResponseDto(BaseModel):
    """Subscription settings response data"""
    uuid: UUID
    profile_title: str = Field(alias="profileTitle")
    support_link: str = Field(alias="supportLink")
    profile_update_interval: int = Field(alias="profileUpdateInterval", ge=1)
    is_profile_webpage_url_enabled: bool = Field(alias="isProfileWebpageUrlEnabled")
    serve_json_at_base_subscription: bool = Field(alias="serveJsonAtBaseSubscription")
    show_custom_remarks: bool = Field(alias="isShowCustomRemarks")
    
    custom_remarks: CustomRemarksDto = Field(alias="customRemarks")
    
    happ_announce: Optional[str] = Field(None, alias="happAnnounce")
    happ_routing: Optional[str] = Field(None, alias="happRouting")
    custom_response_headers: Optional[Dict[str, str]] = Field(None, alias="customResponseHeaders")
    randomize_hosts: bool = Field(alias="randomizeHosts")
    response_rules: Optional[ResponseRules] = Field(None, alias="responseRules")
    
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetSubscriptionSettingsResponseDto(SubscriptionSettingsResponseDto):
    pass


class UpdateSubscriptionSettingsResponseDto(SubscriptionSettingsResponseDto):
    pass


class UpdateSubscriptionSettingsRequestDto(BaseModel):
    """Update subscription settings request"""
    uuid: UUID
    profile_title: Optional[str] = Field(None, serialization_alias="profileTitle")
    support_link: Optional[str] = Field(None, serialization_alias="supportLink")
    profile_update_interval: Optional[int] = Field(None, serialization_alias="profileUpdateInterval")
    is_profile_webpage_url_enabled: Optional[bool] = Field(
        None, serialization_alias="isProfileWebpageUrlEnabled"
    )
    serve_json_at_base_subscription: Optional[bool] = Field(
        None, serialization_alias="serveJsonAtBaseSubscription"
    )
    is_show_custom_remarks: Optional[bool] = Field(None, serialization_alias="isShowCustomRemarks")
    
    custom_remarks: Optional[CustomRemarksDto] = Field(None, serialization_alias="customRemarks")
    
    happ_announce: Optional[Annotated[str, StringConstraints(max_length=200)]] = Field(
        None, serialization_alias="happAnnounce"
    )
    happ_routing: Optional[str] = Field(None, serialization_alias="happRouting")
    custom_response_headers: Optional[Dict[str, str]] = Field(
        None, serialization_alias="customResponseHeaders"
    )
    randomize_hosts: Optional[bool] = Field(None, serialization_alias="randomizeHosts")
    response_rules: Optional[ResponseRules] = Field(None, serialization_alias="responseRules")
    
    hwid_settings: Optional[HwidSettingsDto] = Field(None, serialization_alias="hwidSettings")


# Backward compatibility aliases
CustomRemarks = CustomRemarksDto
HwidSettings = HwidSettingsDto