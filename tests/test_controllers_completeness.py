"""Tests that the controller surface matches Remnawave API 3.0."""
from remnawave.controllers.api_tokens_management import APITokensManagementController
from remnawave.controllers.bandwidthstats import BandWidthStatsController
from remnawave.controllers.connections import ConnectionsController
from remnawave.controllers.hosts_bulk_actions import HostsBulkActionsController
from remnawave.controllers.internal_squads import InternalSquadsController
from remnawave.controllers.node_integrations import NodeIntegrationsController
from remnawave.controllers.node_plugins import NodePluginsController
from remnawave.controllers.system import SystemController
from remnawave.controllers.users import UsersController


def _has(controller, name: str) -> bool:
    return hasattr(controller, name) and callable(getattr(controller, name))


class TestUsersControllerEndpoints:
    def test_crud(self):
        for name in ("create_user", "update_user", "delete_user", "get_all_users"):
            assert _has(UsersController, name), name

    def test_lookups_that_survived_3_0(self):
        for name in (
            "get_user_by_id",
            "get_user_by_short_uuid",
            "get_user_by_username",
            "resolve_user",
            "get_all_tags",
            "get_users_stream",
            "get_user_accessible_nodes",
            "get_user_subscription_request_history",
        ):
            assert _has(UsersController, name), name

    def test_actions(self):
        for name in (
            "enable_user",
            "disable_user",
            "reset_user_traffic",
            "revoke_user_subscription",
            "extend_user_expiration_date",
        ):
            assert _has(UsersController, name), name

    def test_lookups_removed_in_3_0(self):
        """by-email / by-tag / by-telegram-id were dropped — use get_users_stream filters."""
        for name in ("get_users_by_email", "get_users_by_tag", "get_users_by_telegram_id"):
            assert not hasattr(UsersController, name), name

    def test_uuid_lookup_removed_in_3_0(self):
        """Users are identified by numeric id in 3.0."""
        assert not hasattr(UsersController, "get_user_by_uuid")


class TestSystemControllerEndpoints:
    def test_stats(self):
        for name in (
            "get_metadata",
            "get_stats",
            "get_bandwidth_stats",
            "get_nodes_statistics",
            "get_health",
            "get_nodes_metrics",
            "get_x25519_key_pair",
            "debug_srr_matcher",
            "get_recap",
        ):
            assert _has(SystemController, name), name

    def test_new_3_0_stats(self):
        for name in ("get_stats_digest", "get_http_stats"):
            assert _has(SystemController, name), name

    def test_new_3_2_configuration(self):
        assert _has(SystemController, "get_configuration")

    def test_no_encrypt_happ_crypto_link(self):
        # Removed in 2.8 (use client-side happ link generation instead)
        assert not hasattr(SystemController, "encrypt_happ_crypto_link")


class TestApiTokensControllerEndpoints:
    def test_scopes_and_ott(self):
        assert _has(APITokensManagementController, "get_scopes")
        assert _has(APITokensManagementController, "get_ott")


class TestHostsBulkActionsControllerEndpoints:
    def test_has_update_hosts(self):
        assert _has(HostsBulkActionsController, "update_hosts")

    def test_removed_in_2_8(self):
        for name in ("set_inbound_to_hosts", "set_port_to_hosts"):
            assert not hasattr(HostsBulkActionsController, name), name


class TestBandwidthStatsControllerEndpoints:
    def test_stats(self):
        for name in (
            "get_stats_nodes_users_usage",
            "get_stats_node_users_usage",
            "get_stats_user_usage",
            "get_stats_nodes_usage",
        ):
            assert _has(BandWidthStatsController, name), name

    def test_legacy_removed_in_3_0(self):
        for name in ("get_user_usage_legacy_stats", "get_node_users_usage_legacy_stats"):
            assert not hasattr(BandWidthStatsController, name), name


class TestConnectionsControllerEndpoints:
    """`/api/ip-control` became `/api/connections` in 3.0."""

    def test_endpoints(self):
        for name in (
            "connections_by_user",
            "connections_by_user_result",
            "connections_by_node",
            "connections_by_node_result",
            "drop_connections",
        ):
            assert _has(ConnectionsController, name), name

    def test_legacy_controller_alias_still_importable(self):
        from remnawave.controllers.connections import IpControlController

        assert IpControlController is ConnectionsController

    def test_geocheck_added_in_3_3(self):
        for name in ("geocheck_by_node", "geocheck_by_node_result"):
            assert _has(ConnectionsController, name), name


class TestNodeIntegrationsControllerEndpoints:
    """Новый контроллер 3.3."""

    def test_crud(self):
        for name in (
            "get_all_node_integrations",
            "get_node_integration",
            "create_node_integration",
            "update_node_integration",
            "delete_node_integration",
        ):
            assert _has(NodeIntegrationsController, name), name


class TestNodePluginsControllerEndpoints:
    def test_shared_lists_added_in_3_3(self):
        for name in (
            "get_shared_lists",
            "get_shared_list",
            "create_shared_list",
            "update_shared_list",
            "delete_shared_list",
            "sync_shared_list",
        ):
            assert _has(NodePluginsController, name), name

    def test_plugin_sync_added_in_3_3(self):
        assert _has(NodePluginsController, "sync_node_plugin")


class TestInternalSquadsControllerEndpoints:
    def test_targeted_bulk_actions_added_in_3_0(self):
        for name in ("add_many_users_to_internal_squad", "remove_many_users_from_internal_squad"):
            assert _has(InternalSquadsController, name), name
