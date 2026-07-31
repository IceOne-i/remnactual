from enum import StrEnum


class TemplateType(StrEnum):
    """SUBSCRIPTION_TEMPLATE_TYPE — тип шаблона подписки."""
    XRAY_JSON = "XRAY_JSON"
    XRAY_BASE64 = "XRAY_BASE64"
    MIHOMO = "MIHOMO"
    STASH = "STASH"
    CLASH = "CLASH"
    SINGBOX = "SINGBOX"
