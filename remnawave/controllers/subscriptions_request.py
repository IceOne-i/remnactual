from typing import Annotated, Optional

from pydantic import Field
from rapid_api_client import Query

from remnawave.models.subscription_request_history import (
    GetAllSubscriptionRequestHistoryResponseDto,
    GetSubscriptionRequestHistoryStatsResponseDto,
)
from remnawave.rapid import BaseController, get


class SubscriptionRequestHistoryController(BaseController):
    @get("/subscription-request-history", response_class=GetAllSubscriptionRequestHistoryResponseDto)
    async def get_all_subscription_request_history(
        self,
        size: Annotated[
            int, Query(), Field(default=25, ge=1, le=1000, description="Page size, 1..1000 (default 25)")
        ] = 25,
        start: Annotated[
            int, Query(), Field(default=0, ge=0, description="Offset for pagination")
        ] = 0,
        filters: Annotated[
            Optional[str],
            Query(), Field(default=None, description='JSON array of filters, e.g. \'[{"id":"userId","value":7}]\''),
        ] = None,
        filter_modes: Annotated[
            Optional[str],
            Query(alias="filterModes"), Field(default=None, description="JSON object of filter modes"),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(alias="globalFilterMode"), Field(default=None, description="Global filter mode"),
        ] = None,
        sorting: Annotated[
            Optional[str],
            Query(), Field(default=None, description='JSON array of sorting rules, e.g. \'[{"id":"requestAt","desc":true}]\''),
        ] = None,
    ) -> GetAllSubscriptionRequestHistoryResponseDto:
        """Get all subscription request history"""
        ...

    @get(
        "/subscription-request-history/stats",
        response_class=GetSubscriptionRequestHistoryStatsResponseDto,
    )
    async def get_subscription_request_history_stats(
        self,
    ) -> GetSubscriptionRequestHistoryStatsResponseDto:
        """Get subscription request history stats"""
        ...