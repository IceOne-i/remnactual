"""Regression tests for the Remnawave 3.4.x contract delta.

Each test pins something `libs/contract` changed between backend tags `3.3.2`
and `3.4.3`. They run offline — no panel required.

3.4 — первый НЕ аддитивный шаг после 3.0:

* у хоста ``excludedInternalSquads`` заменён на ``internalSquads`` («режим +
  список»), и та же замена транзитивно пришла в массовое обновление;
* ``isDisabled`` в теле ``PATCH /hosts`` перестал иметь значение по умолчанию;
* у shared lists имя ушло из пути в query (``by-name``) и в тело — потому что
  3.4 разрешила слэш внутри имени;
* метки на шести видах сущностей: поле ``tags`` плюс ``GET``/``PATCH`` ``/tags``;
* контроллер ``node-ssh`` — админский, БЕЗ скоупа;
* коды ошибок ``A254``–``A257``.

Пол панели остаётся 3.0.0: снятое поле хоста здесь СОХРАНЕНО рядом с новым,
поэтому SDK продолжает читать и писать панель 3.3.
"""
import ast
import json
import pathlib
from uuid import UUID

import pytest
from pydantic import ValidationError

REPO = pathlib.Path(__file__).resolve().parent.parent

SQUAD_A = UUID("11111111-1111-4111-8111-111111111111")
SQUAD_B = UUID("22222222-2222-4222-8222-222222222222")
ENTITY = UUID("33333333-3333-4333-8333-333333333333")

#: (модуль контроллера, префикс пути) — шесть сущностей, получивших метки.
TAGGED = [
    ("config_profiles", "/config-profiles"),
    ("external_squads", "/external-squads"),
    ("internal_squads", "/internal-squads"),
    ("node_plugins", "/node-plugins"),
    ("subscription_page", "/subscription-page-configs"),
    ("subscriptions_template", "/subscription-templates"),
]

#: (модуль моделей, класс сущности) — те же шесть.
TAGGED_DTO = [
    ("config_profiles", "ConfigProfileDto"),
    ("external_squads", "ExternalSquadDto"),
    ("internal_squads", "InternalSquadDto"),
    ("node_plugins", "NodePluginDto"),
    ("subscription_page", "SubscriptionPageConfigDto"),
    ("subscriptions_template", "TemplateResponseDto"),
]


def _endpoint_decorators(controller_module: str, method_name: str):
    tree = ast.parse(
        (REPO / "remnawave" / "controllers" / f"{controller_module}.py").read_text(
            encoding="utf-8"
        )
    )
    return [
        dec
        for fn in ast.walk(tree)
        if isinstance(fn, ast.AsyncFunctionDef) and fn.name == method_name
        for dec in fn.decorator_list
        if isinstance(dec, ast.Call)
    ]


def _route(controller_module: str, method_name: str):
    decorators = _endpoint_decorators(controller_module, method_name)
    assert len(decorators) == 1, f"{method_name}: ожидался ровно один декоратор"
    dec = decorators[0]
    return getattr(dec.func, "id", None), (dec.args[0].value if dec.args else None)


# ---------------------------------------------------------------------------
# Хосты: excludedInternalSquads -> internalSquads
# ---------------------------------------------------------------------------


class TestHostInternalSquads:
    def test_mode_is_a_closed_pair(self):
        from remnawave.enums import InternalSquadsMode

        assert {m.value for m in InternalSquadsMode} == {"EXCLUDE", "ALLOW_ONLY"}

    def test_allow_only_requires_at_least_one_squad(self):
        """Контракт: ALLOW_ONLY с пустым списком — хост, видимый никому."""
        from remnawave.models import HostInternalSquadsDto

        with pytest.raises(ValidationError):
            HostInternalSquadsDto(mode="ALLOW_ONLY", squads=[])

        assert HostInternalSquadsDto(mode="ALLOW_ONLY", squads=[SQUAD_A]).squads == [SQUAD_A]

    def test_exclude_may_be_empty(self):
        from remnawave.models import HostInternalSquadsDto

        assert HostInternalSquadsDto(mode="EXCLUDE").squads == []

    def test_response_keeps_both_keys_and_neither_is_required(self):
        """Пол панели 3.0.0: на 3.3 не приходит новый ключ, на 3.4 — старый.

        Контракт объявляет ``internalSquads`` ОБЯЗАТЕЛЬНЫМ в ответе; здесь он
        необязателен намеренно, иначе разбор ответа панели 3.3 падал бы.
        """
        from remnawave.models import HostResponseDto

        fields = HostResponseDto.model_fields
        assert fields["internal_squads"].alias == "internalSquads"
        assert fields["excluded_internal_squads"].alias == "excludedInternalSquads"
        assert fields["internal_squads"].is_required() is False
        assert fields["excluded_internal_squads"].is_required() is False

    def test_effective_view_folds_both_panel_shapes(self):
        """Свойство отдаёт ОДНУ форму независимо от версии панели.

        До 3.4 поле выражало ровно режим EXCLUDE, поэтому перевод точный.
        """
        from remnawave.enums import InternalSquadsMode
        from remnawave.models import HostInternalSquadsDto, HostResponseDto

        old = HostResponseDto.model_construct(
            excluded_internal_squads=[SQUAD_A], internal_squads=None
        )
        assert old.effective_internal_squads == HostInternalSquadsDto(
            mode=InternalSquadsMode.EXCLUDE, squads=[SQUAD_A]
        )

        new = HostResponseDto.model_construct(
            excluded_internal_squads=[],
            internal_squads=HostInternalSquadsDto(
                mode=InternalSquadsMode.ALLOW_ONLY, squads=[SQUAD_B]
            ),
        )
        assert new.effective_internal_squads.mode is InternalSquadsMode.ALLOW_ONLY
        assert new.effective_internal_squads.squads == [SQUAD_B]

    @pytest.mark.parametrize(
        "model_name",
        ["CreateHostBodyDto", "UpdateHostBodyDto", "UpdateManyHostsBodyDto"],
    )
    def test_setting_both_forms_is_refused_before_the_call(self, model_name):
        """Схемы панели НЕ строгие: лишний ключ она отбрасывает МОЛЧА.

        Значит ``excludedInternalSquads``, отправленное панели 3.4, ничего не
        сделает и об этом никто не узнает. Здесь это ошибка до сетевого вызова.
        """
        import remnawave.models as models

        model = getattr(models, model_name)
        common = {
            "internal_squads": {"mode": "EXCLUDE", "squads": []},
            "excluded_internal_squads": [SQUAD_A],
        }
        if model_name == "CreateHostBodyDto":
            common |= {
                "inbound": {
                    "config_profile_uuid": str(SQUAD_A),
                    "config_profile_inbound_uuid": str(SQUAD_B),
                },
                "remark": "host",
                "address": "example.org",
                "port": 443,
            }
        elif model_name == "UpdateHostBodyDto":
            common |= {"uuid": ENTITY}
        else:
            common |= {"uuids": [ENTITY]}

        with pytest.raises(ValidationError):
            model(**common)

    @pytest.mark.parametrize(
        "model_name", ["CreateHostBodyDto", "UpdateHostBodyDto", "UpdateManyHostsBodyDto"]
    )
    def test_new_form_serializes_under_the_contract_key(self, model_name):
        import remnawave.models as models

        model = getattr(models, model_name)
        kwargs = {"internal_squads": {"mode": "ALLOW_ONLY", "squads": [str(SQUAD_A)]}}
        if model_name == "CreateHostBodyDto":
            kwargs |= {
                "inbound": {
                    "config_profile_uuid": str(SQUAD_A),
                    "config_profile_inbound_uuid": str(SQUAD_B),
                },
                "remark": "host",
                "address": "example.org",
                "port": 443,
            }
        elif model_name == "UpdateHostBodyDto":
            kwargs |= {"uuid": ENTITY}
        else:
            kwargs |= {"uuids": [ENTITY]}

        dumped = model(**kwargs).model_dump(
            mode="json", exclude_unset=True, by_alias=True
        )
        assert dumped["internalSquads"] == {
            "mode": "ALLOW_ONLY",
            "squads": [str(SQUAD_A)],
        }
        assert "excludedInternalSquads" not in dumped

    def test_old_form_still_reaches_a_3_3_panel(self):
        """Пол панели 3.0.0: снятое поле СОХРАНЕНО и по-прежнему уезжает."""
        from remnawave.models import UpdateHostBodyDto

        dumped = UpdateHostBodyDto(
            uuid=ENTITY, excluded_internal_squads=[SQUAD_A]
        ).model_dump(mode="json", exclude_unset=True, by_alias=True)
        assert dumped["excludedInternalSquads"] == [str(SQUAD_A)]
        assert "internalSquads" not in dumped


class TestHostIsDisabledNoLongerDefaults:
    def test_update_body_omits_is_disabled_when_untouched(self):
        """3.4.0: ``isDisabled`` стал optional вместо ``.default(false)``.

        Раньше обновление, не упомянувшее поле, МОЛЧА включало отключённый
        хост. Тело SDK и до этого не подставляло значение — тест закрепляет,
        что так и останется.
        """
        from remnawave.models import UpdateHostBodyDto

        dumped = UpdateHostBodyDto(uuid=ENTITY, remark="renamed").model_dump(
            mode="json", exclude_unset=True, by_alias=True
        )
        assert "isDisabled" not in dumped


# ---------------------------------------------------------------------------
# Shared lists: имя ушло из пути
# ---------------------------------------------------------------------------


class TestSharedListsMovedOffThePath:
    @pytest.mark.parametrize(
        ("method_name", "http_method", "path"),
        [
            ("get_shared_list", "get", "/node-plugins/shared-lists/by-name"),
            ("delete_shared_list", "delete", "/node-plugins/shared-lists"),
        ],
    )
    def test_endpoints_moved(self, method_name, http_method, path):
        assert _route("node_plugins", method_name) == (http_method, path)

    def test_name_may_contain_slashes(self):
        """Причина переезда: со слэшем имя перестало быть сегментом пути."""
        from remnawave.models import CreateSharedListBodyDto

        body = CreateSharedListBodyDto(
            name="geo/ru/mobile", config={"type": "ipList", "items": []}
        )
        assert body.name == "geo/ru/mobile"

    @pytest.mark.parametrize("name", ["geo//ru", "/geo", "geo/"])
    def test_slash_is_a_separator_not_a_free_character(self, name):
        from remnawave.models import CreateSharedListBodyDto

        with pytest.raises(ValidationError):
            CreateSharedListBodyDto(name=name, config={"type": "ipList", "items": []})

    def test_delete_body_carries_the_name(self):
        from remnawave.models import DeleteSharedListBodyDto

        body = DeleteSharedListBodyDto(name="geo_ru")
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "name": "geo_ru"
        }


# ---------------------------------------------------------------------------
# Метки
# ---------------------------------------------------------------------------


class TestEntityTags:
    @pytest.mark.parametrize(("module", "prefix"), TAGGED)
    def test_get_is_registered_on_the_contract_path(self, module, prefix):
        assert _route(module, "get_tags") == ("get", f"{prefix}/tags")

    @pytest.mark.parametrize(("module", "prefix"), TAGGED)
    def test_set_is_a_patch_on_the_collection(self, module, prefix):
        """Панель принимает PATCH на /tags с uuid В ТЕЛЕ, а не в пути."""
        assert _route(module, "set_tags") == ("patch", f"{prefix}/tags")

    @pytest.mark.parametrize(("module", "dto_name"), TAGGED_DTO)
    def test_entity_carries_tags(self, module, dto_name):
        import importlib

        dto = getattr(importlib.import_module(f"remnawave.models.{module}"), dto_name)
        assert "tags" in dto.model_fields

    @pytest.mark.parametrize(("module", "dto_name"), TAGGED_DTO)
    def test_tags_default_to_empty_on_a_pre_3_4_panel(self, module, dto_name):
        """Пол панели 3.0.0: до 3.4 ключа нет вовсе, разбор обязан пережить это."""
        import importlib

        dto = getattr(importlib.import_module(f"remnawave.models.{module}"), dto_name)
        assert dto.model_fields["tags"].is_required() is False

    def test_body_replaces_the_whole_set(self):
        from remnawave.models import SetEntityTagsBodyDto

        body = SetEntityTagsBodyDto(uuid=ENTITY, tags=[])
        assert body.model_dump(mode="json", exclude_unset=True, by_alias=True) == {
            "uuid": str(ENTITY),
            "tags": [],
        }

    @pytest.mark.parametrize("tag", ["lower", "with space", "ПРИВЕТ", "A" * 37])
    def test_tag_outside_the_contract_pattern_is_rejected(self, tag):
        """Контракт: ^[A-Z0-9_:]+$, не длиннее 36 символов."""
        from remnawave.models import SetEntityTagsBodyDto

        with pytest.raises(ValidationError):
            SetEntityTagsBodyDto(uuid=ENTITY, tags=[tag])

    @pytest.mark.parametrize("tag", ["GEO", "GEO_RU", "GEO:RU", "A1"])
    def test_contract_shaped_tags_pass(self, tag):
        from remnawave.models import SetEntityTagsBodyDto

        assert SetEntityTagsBodyDto(uuid=ENTITY, tags=[tag]).tags == [tag]

    def test_at_most_ten_tags(self):
        from remnawave.models import SetEntityTagsBodyDto

        with pytest.raises(ValidationError):
            SetEntityTagsBodyDto(uuid=ENTITY, tags=[f"T{i}" for i in range(11)])

    def test_get_response_parses_the_contract_payload(self):
        from remnawave.models import GetEntityTagsResponseDto

        assert GetEntityTagsResponseDto.model_validate({"tags": ["GEO"]}).tags == ["GEO"]

    def test_set_response_parses_the_contract_payload(self):
        from remnawave.models import SetEntityTagsResponseDto

        parsed = SetEntityTagsResponseDto.model_validate(
            {"uuid": str(ENTITY), "tags": ["GEO"]}
        )
        assert parsed.uuid == ENTITY and parsed.tags == ["GEO"]


# ---------------------------------------------------------------------------
# node-ssh
# ---------------------------------------------------------------------------


class TestNodeSsh:
    @pytest.mark.parametrize(
        ("method_name", "http_method", "path"),
        [
            ("create_ssh_ticket", "post", "/node-ssh/{uuid}/ticket"),
            ("evaluate_vault", "post", "/node-ssh/vault/evaluate"),
        ],
    )
    def test_endpoints_are_registered_on_the_contract_paths(
        self, method_name, http_method, path
    ):
        assert _route("node_ssh", method_name) == (http_method, path)

    def test_controller_is_reachable_from_the_sdk(self):
        source = (REPO / "remnawave" / "__init__.py").read_text(encoding="utf-8")
        assert "self.node_ssh = NodeSshController(self._client)" in source

    def test_no_scope_exists_for_it(self):
        """Контроллер панели БЕЗ ``@ApiScopeResource``: ресурса нет в каталоге.

        Значит API-токен сюда не пустят ни с каким набором скоупов — нужен
        админский JWT. Скоуп ``node-ssh:*`` в перечислении был бы обещанием
        доступа, которого не существует.
        """
        from remnawave.enums import Scope

        assert not [s for s in Scope if s.value.startswith("node-ssh")]

    def test_ticket_response_parses_the_contract_payload(self):
        from remnawave.models import CreateSshTicketResponseDto

        parsed = CreateSshTicketResponseDto.model_validate(
            {"ticket": "t", "path": "/ssh", "expiresInSeconds": 60}
        )
        assert parsed.expires_in_seconds == 60

    def test_vault_body_limits_the_blinded_value(self):
        from remnawave.models import EvaluateVaultBodyDto

        with pytest.raises(ValidationError):
            EvaluateVaultBodyDto(blinded="x" * 129)


# ---------------------------------------------------------------------------
# Коды ошибок и скоупы
# ---------------------------------------------------------------------------


class TestErrorsAndScopes:
    @pytest.mark.parametrize(
        ("member", "code", "message", "http"),
        [
            ("CREATE_SSH_TICKET_ERROR", "A254", "Create SSH ticket error", 500),
            ("EVALUATE_VAULT_ERROR", "A255", "Vault evaluation refused", 429),
            ("GET_ENTITY_TAGS_ERROR", "A256", "Get tags error", 500),
            ("SET_ENTITY_TAGS_ERROR", "A257", "Set tags error", 500),
        ],
    )
    def test_new_error_codes(self, member, code, message, http):
        from remnawave.enums import ErrorCode
        from remnawave.enums.error_code import ERROR_HTTP_CODES, ERROR_MESSAGES

        assert getattr(ErrorCode, member) == code
        assert ERROR_MESSAGES[code] == message
        assert ERROR_HTTP_CODES[code] == http

    def test_a253_is_absent_in_the_panel_too(self):
        """Панель пропустила номер; пропуск сохранён, иначе коды разъедутся."""
        from remnawave.enums.error_code import ERROR_MESSAGES

        assert "A253" not in ERROR_MESSAGES

    @pytest.mark.parametrize(
        "scope",
        [
            "config-profiles:list-tags",
            "config-profiles:set-tags",
            "external-squads:list-tags",
            "external-squads:set-tags",
            "internal-squads:list-tags",
            "internal-squads:set-tags",
            "node-plugins:list-tags",
            "node-plugins:set-tags",
            "subscription-page-configs:list-tags",
            "subscription-page-configs:set-tags",
            "subscription-template:list-tags",
            "subscription-template:set-tags",
        ],
    )
    def test_tag_scopes_are_grantable(self, scope):
        from remnawave.enums import Scope

        assert scope in {s.value for s in Scope}

    def test_catalog_matches_the_panel_exactly(self):
        """Перечисление против каталога, собранного правилом ScopeCatalogService.

        Каталог нельзя вывести из одного контракта: какие контроллеры вообще
        раздают скоупы, знает только исходник панели (декоратор
        ``@ApiScopeResource``) — auth, passkeys, tokens, настройки и публичная
        подписка не раздают их вовсе.
        """
        from remnawave.enums import Scope

        fixture = json.loads(
            (pathlib.Path(__file__).parent / "fixtures" / "scopes_3.4.json").read_text(
                encoding="utf-8"
            )
        )
        assert {s.value for s in Scope} == set(fixture["scopes"])
