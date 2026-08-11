from enum import StrEnum


class NodeIpStatus(StrEnum):
    """Назначение IP-адреса ноды (``NODE_IP_STATUSES``, контракт 3.2.3)."""

    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    MANAGEMENT = "MANAGEMENT"
    TRANSIT = "TRANSIT"
    MONITORING = "MONITORING"
    RESERVE = "RESERVE"
    BLOCKED = "BLOCKED"
    FLAGGED = "FLAGGED"
    DEPRECATED = "DEPRECATED"
    UNKNOWN = "UNKNOWN"
