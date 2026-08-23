from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from remnawave.enums import TrafficLimitStrategy, UserStatus
from remnawave.models.host_mapper import HostMapperDto
from remnawave.utils.happ_crypt import create_happ_crypto_link
from remnawave.models.users import (
    ActiveInternalSquadDto,
    HappCrypto,
    UserLastConnectedNodeDto,
    UserResponseDto,
    UserTrafficDto,
)


class HwidCheckupDto(BaseModel):
    """Результат проверки HWID-лимита (2.8, заменил булев `isHwidLimited`)"""
    subscription_allowed: bool = Field(alias="subscriptionAllowed")
    max_device_reached: bool = Field(alias="maxDeviceReached")
    hwid_not_supported: bool = Field(alias="hwidNotSupported")
    limit_bypassed: bool = Field(alias="limitBypassed")


class ConvertedUserInfo(BaseModel):
    days_left: int = Field(alias="daysLeft")
    traffic_limit: str = Field(alias="trafficLimit")
    traffic_used: str = Field(alias="trafficUsed")
    lifetime_traffic_used: str = Field(alias="lifetimeTrafficUsed")
    hwid_checkup: Optional[HwidCheckupDto] = Field(None, alias="hwidCheckup")

    @property
    def is_hwid_limited(self) -> bool:
        """Обратная совместимость с полем, удалённым в 2.8."""
        return bool(self.hwid_checkup and not self.hwid_checkup.subscription_allowed)


class Passwords(BaseModel):
    ss_password: str = Field(alias="ssPassword")
    trojan_password: str = Field(alias="trojanPassword")
    vless_password: str = Field(alias="vlessPassword")


class RawHostAdditionalParams(BaseModel):
    mode: Optional[str] = None
    heartbeat_period: Optional[float] = Field(None, alias="heartbeatPeriod")


class RawHostProtocolOptions(BaseModel):
    class SSOptions(BaseModel):
        method: Optional[str] = None
    
    ss: Optional[SSOptions] = None


class RawHostDbData(BaseModel):
    raw_inbound: Optional[Dict[str, Any]] = Field(None, alias="rawInbound")
    inbound_tag: str = Field(alias="inboundTag")
    uuid: str
    config_profile_uuid: Optional[str] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[str] = Field(None, alias="configProfileInboundUuid")
    is_disabled: bool = Field(alias="isDisabled")
    view_position: int = Field(alias="viewPosition") 
    remark: str
    is_hidden: bool = Field(alias="isHidden")
    tag: Optional[str] = None
    vless_route_id: Optional[int] = Field(None, alias="vlessRouteId")

class RawSettings(BaseModel):
    """Raw settings for network configuration"""
    header_type: Optional[str] = Field(None, alias="headerType")
    request: Optional[Dict[str, Any]] = None

class RawHost(BaseModel):
    password: Passwords 
    address: Optional[str] = None
    alpn: Optional[str] = None
    fingerprint: Optional[str] = None
    host: Optional[str] = None
    network: Optional[str] = None
    path: Optional[str] = None
    public_key: Optional[str] = Field(None, alias="publicKey")
    port: Optional[float] = None
    protocol: Optional[str] = None
    remark: Optional[str] = None
    short_id: Optional[str] = Field(None, alias="shortId")
    sni: Optional[str] = None
    spider_x: Optional[str] = Field(None, alias="spiderX")
    tls: Optional[str] = None
    raw_settings: Optional[RawSettings] = Field(None, alias="rawSettings")
    additional_params: Optional[RawHostAdditionalParams] = Field(None, alias="additionalParams")
    x_http_extra_params: Optional[Dict[str, Any]] = Field(None, alias="xHttpExtraParams")
    mux_params: Optional[Dict[str, Any]] = Field(None, alias="muxParams")
    sockopt_params: Optional[Dict[str, Any]] = Field(None, alias="sockoptParams")
    server_description: Optional[str] = Field(None, alias="serverDescription")
    flow: Optional[str] = None
    allow_insecure: Optional[bool] = Field(None, alias="allowInsecure")
    shuffle_host: Optional[bool] = Field(None, alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, alias="mihomoX25519")
    mldsa65_verify: Optional[str] = Field(None, alias="mldsa65Verify")
    encryption: Optional[str] = None
    protocol_options: Optional[RawHostProtocolOptions] = Field(None, alias="protocolOptions")
    db_data: Optional[RawHostDbData] = Field(None, alias="dbData")
    xray_json_template: Optional[Dict[str, Any]] = Field(None, alias="xrayJsonTemplate")


# ─────────────────────────────────────────────────────────────────────────────
# Resolved proxy configs (2.8) — заменили `rawHosts` в raw-подписке
# ─────────────────────────────────────────────────────────────────────────────

class VlessProtocolOptions(BaseModel):
    encryption: str
    id: str
    flow: str


class ShadowsocksProtocolOptions(BaseModel):
    method: str
    password: str
    uot: bool
    uot_version: int = Field(alias="uotVersion")


class TrojanProtocolOptions(BaseModel):
    password: str


class HysteriaProtocolOptions(BaseModel):
    version: int


class TcpTransportOptions(BaseModel):
    header: Optional[Dict[str, Any]] = Field(...)


class XhttpTransportOptions(BaseModel):
    path: Optional[str] = Field(...)
    host: Optional[str] = Field(...)
    mode: str
    extra: Optional[Dict[str, Any]] = Field(...)


class WsTransportOptions(BaseModel):
    path: Optional[str] = Field(...)
    host: Optional[str] = Field(...)
    headers: Optional[Dict[str, str]] = Field(...)
    heartbeat_period: Optional[float] = Field(..., alias="heartbeatPeriod")


class HttpUpgradeTransportOptions(BaseModel):
    path: Optional[str] = Field(...)
    host: Optional[str] = Field(...)
    headers: Optional[Dict[str, str]] = Field(...)


class GrpcTransportOptions(BaseModel):
    authority: Optional[str] = Field(...)
    service_name: Optional[str] = Field(..., alias="serviceName")
    multi_mode: bool = Field(alias="multiMode")


class KcpTransportOptions(BaseModel):
    client_mtu: int = Field(alias="clientMtu")
    client_tti: int = Field(alias="clientTti")
    congestion: bool


class HysteriaTransportOptions(BaseModel):
    version: int
    auth: str


class TlsSecurityOptions(BaseModel):
    pinned_peer_cert_sha256: Optional[str] = Field(..., alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(..., alias="verifyPeerCertByName")
    alpn: Optional[str] = Field(...)
    enable_session_resumption: bool = Field(alias="enableSessionResumption")
    fingerprint: Optional[str] = Field(...)
    server_name: Optional[str] = Field(..., alias="serverName")
    ech_config_list: Optional[str] = Field(..., alias="echConfigList")
    ech_force_query: Optional[str] = Field(..., alias="echForceQuery")
    #: 3.0: новое поле `echSockopt`
    ech_sockopt: Optional[Any] = Field(None, alias="echSockopt")
    #: 3.2.3: `cipherSuites` из `tlsSettings` инбаунда доезжает до Xray-Json и Base64.
    cipher_suites: Optional[str] = Field(None, alias="cipherSuites")


class RealitySecurityOptions(BaseModel):
    fingerprint: str
    public_key: str = Field(alias="publicKey")
    short_id: Optional[str] = Field(..., alias="shortId")
    server_name: str = Field(alias="serverName")
    spider_x: Optional[str] = Field(..., alias="spiderX")
    mldsa65_verify: Optional[str] = Field(..., alias="mldsa65Verify")


class ProxyEntryMetadata(BaseModel):
    uuid: UUID
    tags: List[str]
    exclude_from_subscription_types: List[str] = Field(alias="excludeFromSubscriptionTypes")
    inbound_tag: str = Field(alias="inboundTag")
    config_profile_uuid: Optional[UUID] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[UUID] = Field(None, alias="configProfileInboundUuid")
    is_disabled: bool = Field(alias="isDisabled")
    is_hidden: bool = Field(alias="isHidden")
    view_position: int = Field(alias="viewPosition")
    remark: str
    vless_route_id: Optional[int] = Field(None, alias="vlessRouteId")
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")


class ResolvedProxyStreamOverrides(BaseModel):
    final_mask: Optional[Any] = Field(None, alias="finalMask")
    sockopt: Optional[Any] = None


class ResolvedProxyClientOverrides(BaseModel):
    shuffle_host: bool = Field(alias="shuffleHost")
    mihomo_x25519: bool = Field(alias="mihomoX25519")
    mihomo_ip_version: Optional[str] = Field(None, alias="mihomoIpVersion")
    server_description: Optional[str] = Field(None, alias="serverDescription")
    xray_json_template: Optional[Any] = Field(None, alias="xrayJsonTemplate")
    #: 3.3.0: mapper хоста доезжает до raw-подписки. Панели до 3.3.0 его не присылают.
    mapper: HostMapperDto = Field(default_factory=HostMapperDto, alias="mapper")


class ResolvedProxyConfig(BaseModel):
    """Элемент `resolvedProxyConfigs` raw-подписки (2.8)"""
    final_remark: str = Field(alias="finalRemark")
    address: str
    port: int
    protocol: str
    protocol_options: Union[
        VlessProtocolOptions,
        ShadowsocksProtocolOptions,
        TrojanProtocolOptions,
        HysteriaProtocolOptions,
    ] = Field(alias="protocolOptions")
    transport: str
    transport_options: Union[
        WsTransportOptions,
        HttpUpgradeTransportOptions,
        XhttpTransportOptions,
        GrpcTransportOptions,
        KcpTransportOptions,
        HysteriaTransportOptions,
        TcpTransportOptions,
    ] = Field(alias="transportOptions")
    security: str
    security_options: Optional[Union[TlsSecurityOptions, RealitySecurityOptions]] = Field(
        None, alias="securityOptions"
    )
    stream_overrides: ResolvedProxyStreamOverrides = Field(alias="streamOverrides")
    mux: Optional[Any] = None
    client_overrides: ResolvedProxyClientOverrides = Field(alias="clientOverrides")
    metadata: ProxyEntryMetadata


class RawSubscriptionResponse(BaseModel):
    """Raw subscription response data"""
    user: UserResponseDto
    converted_user_info: ConvertedUserInfo = Field(alias="convertedUserInfo")
    headers: Dict[str, Optional[str]]
    resolved_proxy_configs: List[ResolvedProxyConfig] = Field(
        default_factory=list, alias="resolvedProxyConfigs"
    )


class GetRawSubscriptionByShortUuidResponseDto(RawSubscriptionResponse):
    pass

# ─────────────────────────────────────────────────────────────────────────────
# Subscription info (`SubscriptionInfoSchema`)
# ─────────────────────────────────────────────────────────────────────────────

class UserSubscription(BaseModel):
    short_uuid: str = Field(alias="shortUuid")
    username: str
    days_left: float = Field(alias="daysLeft")
    traffic_used: str = Field(alias="trafficUsed")
    traffic_limit: str = Field(alias="trafficLimit")
    lifetime_traffic_used: str = Field(alias="lifetimeTrafficUsed")
    traffic_used_bytes: str = Field(alias="trafficUsedBytes")
    traffic_limit_bytes: str = Field(alias="trafficLimitBytes")
    lifetime_traffic_used_bytes: str = Field(alias="lifetimeTrafficUsedBytes")
    traffic_limit_strategy: TrafficLimitStrategy = Field(alias="trafficLimitStrategy")
    expires_at: datetime = Field(alias="expiresAt")
    user_status: UserStatus = Field(alias="userStatus")
    is_active: bool = Field(alias="isActive")


class SubscriptionInfoDto(BaseModel):
    """`SubscriptionInfoSchema` контракта 3.0 — общее тело всех ответов о подписке."""
    is_found: bool = Field(alias="isFound")
    user: UserSubscription
    links: List[str]
    ss_conf_links: Dict[str, str] = Field(alias="ssConfLinks")
    subscription_url: str = Field(alias="subscriptionUrl")


class SubscriptionInfoData(SubscriptionInfoDto):
    """3.0 не отдаёт `happ` в теле — ссылка вычисляется на клиенте."""
    happ: Optional[HappCrypto] = None


class GetSubscriptionInfoResponseDto(SubscriptionInfoDto):
    @property
    def happ(self) -> HappCrypto:
        """Generate HAPP link on the fly"""
        crypto_link = create_happ_crypto_link(self.subscription_url)
        return HappCrypto(crypto_link=crypto_link)


class SubscriptionWithoutHapp(SubscriptionInfoDto):
    """Элемент списка `GET /api/subscriptions`."""
    pass


class GetAllSubscriptionsResponseDto(BaseModel):
    subscriptions: List[SubscriptionWithoutHapp]
    total: float


class GetSubscriptionByUsernameResponseDto(SubscriptionInfoDto):
    pass


class GetSubscriptionByShortUuidProtectedResponseDto(SubscriptionInfoDto):
    pass


class GetSubscriptionByIdResponseDto(SubscriptionInfoDto):
    """Ответ `GET /api/subscriptions/by-id/{userId}` (3.0, заменил `by-uuid/{uuid}`)."""
    pass


class GetConnectionKeysByUserIdResponseDto(BaseModel):
    enabled_keys: List[str] = Field(alias="enabledKeys")
    hidden_keys: List[str] = Field(alias="hiddenKeys")
    disabled_keys: List[str] = Field(alias="disabledKeys")

    @property
    def connection_keys(self) -> List[str]:
        """Backward compatibility: historically SDK exposed a flat list of keys."""
        return self.enabled_keys


# Legacy aliases for backward compatibility
SubscriptionInfoResponseDto = GetSubscriptionInfoResponseDto
GetSubscriptionsResponseDto = GetAllSubscriptionsResponseDto
GetSubscriptionByShortUUIDResponseDto = GetSubscriptionByShortUuidProtectedResponseDto
GetSubscriptionByUUIDResponseDto = GetSubscriptionByIdResponseDto
GetConnectionKeysByUuidResponseDto = GetConnectionKeysByUserIdResponseDto