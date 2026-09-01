from typing import Annotated, Optional

from rapid_api_client import Path, PydanticBody, Query


from remnawave.models.node_plugins import (
    CloneNodePluginBodyDto,
    CloneNodePluginResponseDto,
    CreateNodePluginBodyDto,
    CreateNodePluginResponseDto,
    CreateSharedListBodyDto,
    CreateSharedListResponseDto,
    DeleteSharedListBodyDto,
    GetNodePluginResponseDto,
    GetNodePluginsResponseDto,
    GetSharedListResponseDto,
    GetSharedListsResponseDto,
    GetTorrentBlockerReportsResponseDto,
    GetTorrentBlockerReportsStatsResponseDto,
    PluginExecutorBodyDto,
    ReorderNodePluginsBodyDto,
    ReorderNodePluginsResponseDto,
    SyncNodePluginBodyDto,
    SyncSharedListBodyDto,
    UpdateNodePluginBodyDto,
    UpdateNodePluginResponseDto,
    UpdateSharedListBodyDto,
    UpdateSharedListResponseDto,
)
from remnawave.models.tags import (
    GetEntityTagsResponseDto,
    SetEntityTagsBodyDto,
    SetEntityTagsResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodePluginsController(BaseController):
    @get("/node-plugins/torrent-blocker", response_class=GetTorrentBlockerReportsResponseDto)
    async def get_torrent_blocker_reports(
        self,
        size: Annotated[
            Optional[int], Query(default=None, ge=1, le=1000, description="Page size, 1..1000")
        ] = None,
        start: Annotated[Optional[int], Query(default=None, ge=0, description="Offset")] = None,
        filters: Annotated[
            Optional[str], Query(default=None, description="JSON array of filters")
        ] = None,
        filter_modes: Annotated[
            Optional[str],
            Query(default=None, alias="filterModes", description="JSON object of filter modes"),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(default=None, alias="globalFilterMode", description="Global filter mode"),
        ] = None,
        sorting: Annotated[
            Optional[str], Query(default=None, description="JSON array of sorting rules")
        ] = None,
    ) -> GetTorrentBlockerReportsResponseDto:
        """Get Torrent Blocker Reports"""
        ...

    @get("/node-plugins/torrent-blocker/stats", response_class=GetTorrentBlockerReportsStatsResponseDto)
    async def get_torrent_blocker_reports_stats(
        self,
    ) -> GetTorrentBlockerReportsStatsResponseDto:
        """Get Torrent Blocker Reports Stats"""
        ...

    @delete("/node-plugins/torrent-blocker/truncate", response_class=None)
    async def truncate_torrent_blocker_reports(
        self,
    ) -> None:
        """Truncate Torrent Blocker Reports (204 No Content)"""
        ...

    @get("/node-plugins", response_class=GetNodePluginsResponseDto)
    async def get_all_node_plugins(self) -> GetNodePluginsResponseDto:
        """Get all Node Plugins"""
        ...

    @patch("/node-plugins", response_class=UpdateNodePluginResponseDto)
    async def update_node_plugin(
        self,
        body: Annotated[UpdateNodePluginBodyDto, PydanticBody()],
    ) -> UpdateNodePluginResponseDto:
        """Update Node Plugin"""
        ...

    @post("/node-plugins", response_class=CreateNodePluginResponseDto)
    async def create_node_plugin(
        self,
        body: Annotated[CreateNodePluginBodyDto, PydanticBody()],
    ) -> CreateNodePluginResponseDto:
        """Create Node Plugin (201 Created)"""
        ...

    @get("/node-plugins/{uuid}", response_class=GetNodePluginResponseDto)
    async def get_node_plugin_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> GetNodePluginResponseDto:
        """Get Node Plugin by uuid"""
        ...

    @delete("/node-plugins/{uuid}", response_class=None)
    async def delete_node_plugin(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> None:
        """Delete Node Plugin (204 No Content)"""
        ...

    @post("/node-plugins/actions/reorder", response_class=ReorderNodePluginsResponseDto)
    async def reorder_node_plugins(
        self,
        body: Annotated[ReorderNodePluginsBodyDto, PydanticBody()],
    ) -> ReorderNodePluginsResponseDto:
        """Reorder Node Plugins"""
        ...

    @post("/node-plugins/actions/clone", response_class=CloneNodePluginResponseDto)
    async def clone_node_plugin(
        self,
        body: Annotated[CloneNodePluginBodyDto, PydanticBody()],
    ) -> CloneNodePluginResponseDto:
        """Clone Node Plugin"""
        ...

    @post("/node-plugins/executor", response_class=None)
    async def plugin_executor(
        self,
        body: Annotated[PluginExecutorBodyDto, PydanticBody()],
    ) -> None:
        """Execute command on node plugins (202 Accepted)"""
        ...

    @post("/node-plugins/actions/sync", response_class=None)
    async def sync_node_plugin(
        self,
        body: Annotated[SyncNodePluginBodyDto, PydanticBody()],
    ) -> None:
        """Sync Node Plugin to nodes

        3.3.0: отправляет текущий конфиг плагина, включая общие списки, на каждую
        подключённую ноду, где плагин активен.

        Отвечает ``202 Accepted`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @get("/node-plugins/shared-lists", response_class=GetSharedListsResponseDto)
    async def get_shared_lists(self) -> GetSharedListsResponseDto:
        """Get Shared Lists (Preview)

        3.3.0: возвращает только имя, тип и количество элементов каждого списка.
        За самими элементами — :meth:`get_shared_list`.
        """
        ...

    @get("/node-plugins/shared-lists/by-name", response_class=GetSharedListResponseDto)
    async def get_shared_list(
        self,
        name: Annotated[str, Query(description="Shared list name")],
    ) -> GetSharedListResponseDto:
        """Get Shared List by name

        **Требует панель 3.4.0+.** До неё имя стояло СЕГМЕНТОМ ПУТИ
        (``/shared-lists/{name}``). Адрес сменился не ради красоты: 3.4.0
        разрешила слэш внутри имени, а такое имя сегментом пути быть не может.
        """
        ...

    @post("/node-plugins/shared-lists", response_class=CreateSharedListResponseDto)
    async def create_shared_list(
        self,
        body: Annotated[CreateSharedListBodyDto, PydanticBody()],
    ) -> CreateSharedListResponseDto:
        """Create Shared List (201 Created)

        Префикс ``ext:`` панель добавляет к имени сама.
        """
        ...

    @patch("/node-plugins/shared-lists", response_class=UpdateSharedListResponseDto)
    async def update_shared_list(
        self,
        body: Annotated[UpdateSharedListBodyDto, PydanticBody()],
    ) -> UpdateSharedListResponseDto:
        """Update Shared List"""
        ...

    @delete("/node-plugins/shared-lists", response_class=None)
    async def delete_shared_list(
        self,
        body: Annotated[DeleteSharedListBodyDto, PydanticBody()],
    ) -> None:
        """Delete Shared List by name (204 No Content)

        **Требует панель 3.4.0+.** Имя переехало из пути в ТЕЛО по той же
        причине, что и у :meth:`get_shared_list`: со слэшем внутри оно
        перестало быть выразимым сегментом пути.
        """
        ...

    @post("/node-plugins/shared-lists/actions/sync", response_class=None)
    async def sync_shared_list(
        self,
        body: Annotated[SyncSharedListBodyDto, PydanticBody()],
    ) -> None:
        """Sync Shared List to nodes

        3.3.0: раскатывает каждый плагин, ссылающийся на список, по нодам,
        где этот плагин активен.

        Отвечает ``202 Accepted`` с пустым телом — метод возвращает ``None``.
        """
        ...

    @get("/node-plugins/tags", response_class=GetEntityTagsResponseDto)
    async def get_tags(self) -> GetEntityTagsResponseDto:
        """Get tags of Node Plugins (панель 3.4.0+)

        Отдаёт ВСЕ метки, встречающиеся у сущностей этого вида, а не метки
        одной из них: у конкретной они лежат в её собственном поле ``tags``.
        """
        ...

    @patch("/node-plugins/tags", response_class=SetEntityTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetEntityTagsBodyDto, PydanticBody()],
    ) -> SetEntityTagsResponseDto:
        """Set tags of Node Plugin (панель 3.4.0+)

        ЗАМЕНЯЕТ набор меток целиком: пустой список снимает все.
        """
        ...
