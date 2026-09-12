from typing import Annotated, Optional

from pydantic import Field
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    ConnectionsByNodeResponseDto,
    ConnectionsByNodeResultResponseDto,
    ConnectionsByUserResponseDto,
    ConnectionsByUserResultResponseDto,
    DropConnectionsBodyDto,
    GeocheckByNodeBodyDto,
    GeocheckByNodeResponseDto,
    GeocheckByNodeResultResponseDto,
)
from remnawave.rapid import BaseController, get, post


class ConnectionsController(BaseController):
    @post("/connections/by-user/{userId}", response_class=ConnectionsByUserResponseDto)
    async def connections_by_user(
        self,
        user_id: Annotated[int, Path(alias="userId"), Field(description="ID of the user")],
    ) -> ConnectionsByUserResponseDto:
        """Request Connections for User.

        Starts a background job that queries all connected nodes for the IPs
        used by the given user.  The returned ``job_id`` must be passed to
        :meth:`connections_by_user_result` to retrieve the actual list once the
        job is complete.
        """
        ...

    @get("/connections/by-user/{jobId}", response_class=ConnectionsByUserResultResponseDto)
    async def connections_by_user_result(
        self,
        job_id: Annotated[str, Path(alias="jobId"), Field(description="Job ID returned by connections_by_user")],
    ) -> ConnectionsByUserResultResponseDto:
        """Get Connections for User by Job ID.

        Poll this endpoint after calling :meth:`connections_by_user`.  When
        ``is_completed`` is ``True`` the ``result`` field contains per-node
        IP lists.  When ``is_failed`` is ``True`` the job encountered an
        error.
        """
        ...

    @post("/connections/by-node/{nodeUuid}", response_class=ConnectionsByNodeResponseDto)
    async def connections_by_node(
        self,
        node_uuid: Annotated[str, Path(alias="nodeUuid"), Field(description="UUID of the node")],
    ) -> ConnectionsByNodeResponseDto:
        """Request Connections for Node.

        Starts a background job that queries the specified node for the IPs
        of all connected users. The returned ``job_id`` must be passed to
        :meth:`connections_by_node_result` to retrieve the actual list once
        the job is complete.
        """
        ...

    @get("/connections/by-node/{jobId}", response_class=ConnectionsByNodeResultResponseDto)
    async def connections_by_node_result(
        self,
        job_id: Annotated[str, Path(alias="jobId"), Field(description="Job ID returned by connections_by_node")],
    ) -> ConnectionsByNodeResultResponseDto:
        """Get Connections for Node by Job ID.

        Poll this endpoint after calling :meth:`connections_by_node`. When
        ``is_completed`` is ``True`` the ``result`` field contains per-user
        IP lists.
        """
        ...

    @post("/connections/geocheck/{nodeUuid}", response_class=GeocheckByNodeResponseDto)
    async def geocheck_by_node(
        self,
        node_uuid: Annotated[str, Path(alias="nodeUuid"), Field(description="UUID of the node")],
        body: Annotated[Optional[GeocheckByNodeBodyDto], PydanticBody()] = None,
    ) -> GeocheckByNodeResponseDto:
        """Request Geocheck for Node.

        3.3.0: ставит задачу геопроверки на ноде и возвращает ``job_id``.
        Результат забирается через :meth:`geocheck_by_node_result` — нода может
        отвечать до минуты.

        Источник проверки задаётся либо ``ip``, либо ``interface``, но не оба сразу.
        """
        ...

    @get("/connections/geocheck/{jobId}", response_class=GeocheckByNodeResultResponseDto)
    async def geocheck_by_node_result(
        self,
        job_id: Annotated[str, Path(alias="jobId"), Field(description="Job ID returned by geocheck_by_node")],
    ) -> GeocheckByNodeResultResponseDto:
        """Get Geocheck for Node by Job ID.

        Когда ``is_completed`` — ``True``, в ``result`` лежит отчёт ноды:
        SVG-картинка в base64 (``image``) и сырой отчёт (``raw_report``).
        """
        ...

    @post("/connections/drop", response_class=None)
    async def drop_connections(
        self,
        body: Annotated[DropConnectionsBodyDto, PydanticBody()],
    ) -> None:
        """Drop active connections.

        Sends a drop-connections event to the target nodes.  You can specify
        the connections to drop either by user IDs or by IP addresses, and
        you can target all connected nodes or a specific subset.

        Отвечает ``202 Accepted`` с пустым телом — метод возвращает ``None``.
        """
        ...


# Обратная совместимость: контроллер до 3.0 назывался IpControlController.
IpControlController = ConnectionsController
