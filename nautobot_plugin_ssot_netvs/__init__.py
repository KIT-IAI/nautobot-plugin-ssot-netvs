"""nautobot_ssot_netvs Plugin Initilization."""
import os

from nautobot.core.signals import nautobot_database_ready
from nautobot.extras.plugins import PluginConfig

from nautobot_plugin_ssot_netvs.signals import nautobot_database_ready_callback


class NautobotSsotNetvsConfig(PluginConfig):
    """Plugin configuration for the nautobot_ssot_netvs plugin."""

    name = "nautobot_plugin_ssot_netvs"  # Raw plugin name; same as the plugin's source directory.
    verbose_name = "nautobot_ssot_netvs"  # Human-friendly name for the plugin.
    base_url = "nautobot_ssot_netvs"  # (Optional) Base path to use for plugin URLs. Defaulting to app_name.
    required_settings = []  # A list of any configuration parameters that must be defined by the user.
    min_version = "1.0.0"  # Minimum version of Nautobot with which the plugin is compatible.
    max_version = "1.999"  # Maximum version of Nautobot with which the plugin is compatible.
    default_settings = {
        "netvs_base_url": os.getenv("NETVS_BASE_URL"),
        "netvs_token": os.environ.get("NETVS_TOKEN")
    }
    caching_config = {}  # Plugin-specific cache configuration.

    def ready(self):
        """Trigger callback when database is ready."""
        super().ready()

        nautobot_database_ready.connect(nautobot_database_ready_callback, sender=self)


config = NautobotSsotNetvsConfig
