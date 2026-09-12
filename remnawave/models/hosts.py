from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, RootModel, model_validator

from remnawave.enums import (
    ALPN,
    InternalSquadsMode,
    MihomoIpVersion,
    SecurityLayer,
    SubscriptionType,
)
from remnawave.models.host_mapper import HostMapperDto

# Tag for a single host tag entry: uppercase alphanumeric, underscores and colons, max 36 chars
HostTag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]

# `remark` в 3.0 расширен с 40 до 100 символов (CreateHostCommand/UpdateHostCommand)
HostRemark = Annotated[str, StringConstraints(min_length=1, max_length=100)]


class HostInternalSquadsDto(BaseModel):
    """Отношение хоста к внутренним сквадам (панель 3.4.0+).

    Пришло на смену полю ``excludedInternalSquads``, которое умело выражать
    только один случай — «спрятать от перечисленных». Режим ``ALLOW_ONLY``
    выражает обратный, и панель требует у него непустой список: хост,
    видимый ТОЛЬКО пустому множеству сквадов, не виден никому.
    """

    mode: InternalSquadsMode
    squads: List[UUID] = Field(default_factory=list)

    @model_validator(mode="after")
    def _allow_only_needs_squads(self) -> "HostInternalSquadsDto":
        if self.mode is InternalSquadsMode.ALLOW_ONLY and not self.squads:
            raise ValueError("At least one internal squad is required in ALLOW_ONLY mode")
        return self


def _reject_both_squad_fields(model: BaseModel) -> None:
    """Запрещает задать и старое поле, и новое одновременно.

    Схемы панели НЕ строгие: неизвестный ключ она отбрасывает молча. Значит
    ``excluded_internal_squads``, отправленное панели 3.4+, не вызовет ошибки
    и просто ничего не сделает — а вызывающий будет уверен, что настроил
    хост. Разрешать оба поля сразу значит оставить этот промах невидимым;
    здесь он становится ошибкой ещё до сетевого вызова.
    """
    fields = model.model_fields_set
    if "internal_squads" in fields and "excluded_internal_squads" in fields:
        raise ValueError(
            "excluded_internal_squads (panel < 3.4) and internal_squads (panel >= 3.4) "
            "are two forms of the same setting — set exactly one, matching your panel"
        )


class ReorderHostItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderHostsBodyDto(BaseModel):
    hosts: List[ReorderHostItem]


class CloneHostBodyDto(BaseModel):
    """POST /hosts/actions/clone (panel >= 3.4.4)."""
    model_config = ConfigDict(populate_by_name=True)

    clone_from_uuid: UUID = Field(alias="cloneFromUuid")


class HostInboundData(BaseModel):
    config_profile_uuid: Optional[UUID] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[UUID] = Field(None, alias="configProfileInboundUuid")


class CreateHostInboundData(BaseModel):
    config_profile_uuid: UUID = Field(serialization_alias="configProfileUuid")
    config_profile_inbound_uuid: UUID = Field(serialization_alias="configProfileInboundUuid")


class UpdateHostBodyDto(BaseModel):
    uuid: UUID
    inbound: Optional[CreateHostInboundData] = None
    remark: Optional[HostRemark] = None
    address: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    is_disabled: Optional[bool] = Field(None, serialization_alias="isDisabled")
    security_layer: Optional[SecurityLayer] = Field(None, serialization_alias="securityLayer")
    server_description: Optional[str] = Field(None, serialization_alias="serverDescription", max_length=30)
    tags: Optional[List[HostTag]] = Field(None, serialization_alias="tags", max_length=10)
    is_hidden: Optional[bool] = Field(None, serialization_alias="isHidden")
    override_sni_from_address: Optional[bool] = Field(None, serialization_alias="overrideSniFromAddress")
    keep_blank_sni: Optional[bool] = Field(None, serialization_alias="keepSniBlank")
    vless_route_id: Optional[int] = Field(None, serialization_alias="vlessRouteId", ge=0, le=65535)
    pinned_peer_cert_sha256: Optional[str] = Field(None, serialization_alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(None, serialization_alias="verifyPeerCertByName")
    shuffle_host: Optional[bool] = Field(None, serialization_alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(None, serialization_alias="mihomoIpVersion")
    xhttp_extra_params: Optional[Any] = Field(None, serialization_alias="xhttpExtraParams")
    mux_params: Optional[Any] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[Any] = Field(None, serialization_alias="sockoptParams")
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    nodes: Optional[List[UUID]] = None
    xray_json_template_uuid: Optional[UUID] = Field(None, serialization_alias="xrayJsonTemplateUuid")
    #: Панель < 3.4. Снято в 3.4.0 в пользу :attr:`internal_squads`.
    excluded_internal_squads: Optional[List[UUID]] = Field(
        None,
        serialization_alias="excludedInternalSquads",
        deprecated="Panel < 3.4 only. Panel 3.4 replaced it with internal_squads "
        "and IGNORES this key silently.",
    )
    #: Панель 3.4.0+. Пара «режим + список» вместо одного списка исключений.
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None, serialization_alias="internalSquads"
    )
    exclude_from_subscription_types: Optional[List[SubscriptionType]] = Field(
        None,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )
    #: 3.3.0: правки сгенерированного конфига по типам клиентов.
    mapper: Optional[HostMapperDto] = Field(None, serialization_alias="mapper")

    @model_validator(mode="after")
    def _one_squad_form(self) -> "UpdateHostBodyDto":
        _reject_both_squad_fields(self)
        return self

    def __init__(self, **data):
        # Backward compatibility: `tag` (single value) was replaced by `tags` (list) in v2.8.0
        if "tag" in data and "tags" not in data:
            tag = data.pop("tag")
            # `tags: null` контрактом не принимается — при tag=None поле просто не задаём
            if tag is not None:
                data["tags"] = [tag]
        # Backward compatibility: `allow_insecure` was removed in v2.8.0 (use security_layer instead)
        data.pop("allow_insecure", None)
        # Backward compatibility: `xHttpExtraParams` alias was renamed to `xhttpExtraParams`
        if "x_http_extra_params" in data and "xhttp_extra_params" not in data:
            data["xhttp_extra_params"] = data.pop("x_http_extra_params")
        super().__init__(**data)

    @property
    def x_http_extra_params(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> Optional[str]:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid if self.inbound else None


class HostResponseDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    remark: str
    address: str
    port: int
    path: str | None = Field(alias="path")
    sni: str | None = Field(alias="sni")
    host: str | None = Field(alias="host")
    alpn: str | None = Field(alias="alpn")
    fingerprint: str | None = Field(alias="fingerprint")
    xhttp_extra_params: Any | None = Field(None, alias="xhttpExtraParams")
    mux_params: Any | None = Field(alias="muxParams")
    sockopt_params: Any | None = Field(alias="sockoptParams")
    final_mask: Any | None = Field(None, alias="finalMask")
    inbound: HostInboundData
    server_description: str | None = Field(alias="serverDescription")
    tags: List[str] = Field(default_factory=list, alias="tags")
    vless_route_id: int | None = Field(alias="vlessRouteId")
    pinned_peer_cert_sha256: str | None = Field(None, alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: str | None = Field(None, alias="verifyPeerCertByName")
    shuffle_host: bool = Field(alias="shuffleHost")
    mihomo_x25519: bool = Field(alias="mihomoX25519")
    mihomo_ip_version: str | None = Field(None, alias="mihomoIpVersion")
    nodes: List[UUID]
    is_disabled: bool = Field(False, alias="isDisabled")
    security_layer: SecurityLayer = Field(SecurityLayer.DEFAULT, alias="securityLayer")
    is_hidden: bool = Field(False, alias="isHidden")
    override_sni_from_address: bool = Field(False, alias="overrideSniFromAddress")
    keep_blank_sni: bool = Field(False, alias="keepSniBlank")
    xray_json_template_uuid: UUID | None = Field(alias="xrayJsonTemplateUuid")
    #: Панель < 3.4. На 3.4+ поле не приходит и остаётся пустым — читайте
    #: :attr:`effective_internal_squads`, он сводит обе формы к одной.
    excluded_internal_squads: List[UUID] = Field(default_factory=list, alias="excludedInternalSquads")
    #: Панель 3.4.0+. Объявлено обязательным в контракте, но здесь
    #: необязательно НАМЕРЕННО: пол панели у форка — 3.0.0, а панель до 3.4
    #: этого ключа не присылает вовсе.
    internal_squads: Optional[HostInternalSquadsDto] = Field(None, alias="internalSquads")
    exclude_from_subscription_types: List[SubscriptionType] = Field(
        default_factory=list,
        alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host is excluded.",
    )
    # 3.3.0: правки сгенерированного конфига. Панели до 3.3.0 поля не присылают.
    mapper: HostMapperDto = Field(default_factory=HostMapperDto, alias="mapper")

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid

    @property
    def x_http_extra_params(self) -> Dict[str, Any] | None:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> str | None:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    @property
    def allow_insecure(self) -> bool:
        """Backward compatibility property (removed in v2.8.0, derived from security_layer)"""
        return self.security_layer == SecurityLayer.NONE

    @property
    def effective_internal_squads(self) -> HostInternalSquadsDto:
        """Отношение хоста к сквадам ОДНОЙ формой, независимо от версии панели.

        На 3.4+ отдаёт то, что прислала панель. На панели до 3.4 собирает
        эквивалент из ``excludedInternalSquads``: старое поле выражало ровно
        режим ``EXCLUDE``, поэтому перевод точный, а не приблизительный.
        """
        if self.internal_squads is not None:
            return self.internal_squads
        return HostInternalSquadsDto(
            mode=InternalSquadsMode.EXCLUDE, squads=list(self.excluded_internal_squads)
        )


class CreateHostBodyDto(BaseModel):
    inbound: CreateHostInboundData
    remark: HostRemark
    address: str
    port: int
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    xhttp_extra_params: Optional[Any] = Field(None, serialization_alias="xhttpExtraParams")
    mux_params: Optional[Any] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[Any] = Field(None, serialization_alias="sockoptParams")
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    server_description: Optional[str] = Field(None, serialization_alias="serverDescription", max_length=30)
    tags: Optional[List[HostTag]] = Field(None, serialization_alias="tags", max_length=10)
    vless_route_id: Optional[int] = Field(None, serialization_alias="vlessRouteId", ge=0, le=65535)
    pinned_peer_cert_sha256: Optional[str] = Field(None, serialization_alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(None, serialization_alias="verifyPeerCertByName")
    shuffle_host: bool = Field(False, serialization_alias="shuffleHost")
    mihomo_x25519: bool = Field(False, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(None, serialization_alias="mihomoIpVersion")
    nodes: List[UUID] = Field(default_factory=list)
    is_disabled: bool = Field(False, serialization_alias="isDisabled")
    security_layer: SecurityLayer = Field(SecurityLayer.DEFAULT, serialization_alias="securityLayer")
    is_hidden: bool = Field(False, serialization_alias="isHidden")
    override_sni_from_address: bool = Field(False, serialization_alias="overrideSniFromAddress")
    keep_blank_sni: bool = Field(False, serialization_alias="keepSniBlank")
    xray_json_template_uuid: Optional[UUID] = Field(None, serialization_alias="xrayJsonTemplateUuid")
    #: Панель < 3.4. Снято в 3.4.0 в пользу :attr:`internal_squads`.
    excluded_internal_squads: List[UUID] = Field(
        default_factory=list,
        serialization_alias="excludedInternalSquads",
        deprecated="Panel < 3.4 only. Panel 3.4 replaced it with internal_squads "
        "and IGNORES this key silently.",
    )
    #: Панель 3.4.0+. Пара «режим + список» вместо одного списка исключений.
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None, serialization_alias="internalSquads"
    )
    exclude_from_subscription_types: List[SubscriptionType] = Field(
        default_factory=list,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )
    #: 3.3.0: правки сгенерированного конфига по типам клиентов.
    mapper: Optional[HostMapperDto] = Field(None, serialization_alias="mapper")

    @model_validator(mode="after")
    def _one_squad_form(self) -> "CreateHostBodyDto":
        _reject_both_squad_fields(self)
        return self

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid

    @property
    def x_http_extra_params(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> Optional[str]:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    def __init__(
        self,
        inbound_uuid: Optional[UUID] = None,
        config_profile_uuid: Optional[UUID] = None,
        **data,
    ):
        # Совместимость: `inbound_uuid` + `config_profile_uuid` собираются в `inbound`.
        # Исторически UUID профиля передавали под именем `config_profile_inbound_uuid`.
        if config_profile_uuid is None and "config_profile_inbound_uuid" in data:
            config_profile_uuid = data.pop("config_profile_inbound_uuid")

        if inbound_uuid is not None and "inbound" not in data:
            if config_profile_uuid is None:
                raise ValueError(
                    "config_profile_uuid is required when passing inbound_uuid; "
                    "pass inbound=CreateHostInboundData(...) instead"
                )
            data["inbound"] = CreateHostInboundData(
                config_profile_uuid=config_profile_uuid,
                config_profile_inbound_uuid=inbound_uuid,
            )

        # Backward compatibility: `tag` (single value) was replaced by `tags` (list) in v2.8.0
        if "tag" in data and "tags" not in data:
            tag = data.pop("tag")
            # `tags: null` контрактом не принимается — при tag=None поле просто не задаём
            if tag is not None:
                data["tags"] = [tag]
        # Backward compatibility: `allow_insecure` was removed in v2.8.0 (use security_layer instead)
        data.pop("allow_insecure", None)
        # Backward compatibility: `xHttpExtraParams` alias was renamed to `xhttpExtraParams`
        if "x_http_extra_params" in data and "xhttp_extra_params" not in data:
            data["xhttp_extra_params"] = data.pop("x_http_extra_params")

        super().__init__(**data)


class GetHostsTagsResponseDto(BaseModel):
    """GET /hosts/tags → 200 `{ "response": { "tags": [...] } }`"""
    tags: List[str]


class GetHostsResponseDto(RootModel[List[HostResponseDto]]):
    """GET /hosts → 200, список хостов."""
    root: List[HostResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


class ReorderHostsResponseDto(BaseModel):
    """POST /hosts/actions/reorder → 200 `{ "response": { "isUpdated": bool } }`"""
    is_updated: bool = Field(alias="isUpdated", default=True)


# ─────────────────────────────────────────────────────────────────────────────
# Legacy aliases (имена до 3.0) — импорты продолжают работать
# ─────────────────────────────────────────────────────────────────────────────
CreateHostRequestDto = CreateHostBodyDto
UpdateHostRequestDto = UpdateHostBodyDto
ReorderHostRequestDto = ReorderHostsBodyDto
ReorderHostResponseDto = ReorderHostsResponseDto
GetAllHostsResponseDto = GetHostsResponseDto
GetAllHostTagsResponseDto = GetHostsTagsResponseDto

# POST /hosts (201), PATCH /hosts (200) и GET /hosts/{uuid} (200) отдают один и тот же
# `HostResponseSchema`, поэтому отдельных моделей у них больше нет.
CreateHostResponseDto = HostResponseDto
UpdateHostResponseDto = HostResponseDto
GetOneHostResponseDto = HostResponseDto
HostsResponseDto = HostResponseDto
