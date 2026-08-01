from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    ConnectionsByNodeResponseDto,
    ConnectionsByNodeResultResponseDto,
    ConnectionsByUserResponseDto,
    ConnectionsByUserResultResponseDto,
    DropConnectionsBodyDto,
)
from remnawave.rapid import BaseController, get, post


class ConnectionsController(BaseController):
    @post("/connections/by-user/{userId}", response_class=ConnectionsByUserResponseDto)
    async def connections_by_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
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
        job_id: Annotated[str, Path(description="Job ID returned by connections_by_user", alias="jobId")],
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
        node_uuid: Annotated[str, Path(description="UUID of the node", alias="nodeUuid")],
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
        job_id: Annotated[str, Path(description="Job ID returned by connections_by_node", alias="jobId")],
    ) -> ConnectionsByNodeResultResponseDto:
        """Get Connections for Node by Job ID.

        Poll this endpoint after calling :meth:`connections_by_node`. When
        ``is_completed`` is ``True`` the ``result`` field contains per-user
        IP lists.
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
