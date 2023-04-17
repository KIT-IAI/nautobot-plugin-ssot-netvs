from typing import Iterable

from nautobot.extras.jobs import Job, BooleanVar
from nautobot_ssot.jobs.base import DataSource, DataMapping
from diffsync import DiffSyncFlags
from django.urls import reverse
from nautobot_plugin_ssot_netvs.diffsync.adapters import netvs, nautobot

name = "Netvs SSoT"


class NetvsDataSource(DataSource, Job):
    debug = BooleanVar(description="Enable for verbose logging", default=False)

    def __init__(self):
        super().__init__()
        self.diffsync_flags = DiffSyncFlags.NONE

    class Meta:
        name = "Netvs to Nautobot"
        data_source = "Netvs"
        description = "Sync information from Netvs to Nautobot"

    @classmethod
    def config_information(cls):
        """Dictionary describing the configuration of this DataSource."""
        return {}

    @classmethod
    def data_mappings(cls) -> Iterable:
        return (
         DataMapping("Subnet (remote)", None, "Prefix (local)", reverse("ipam:prefix_list")),
        )

    def load_source_adapter(self):
        self.source_adapter = netvs.NetVSAdapter(job=self, sync=self.sync)
        self.source_adapter.load()

    def load_target_adapter(self):
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()

    def execute_sync(self):
        if self.source_adapter is not None and self.target_adapter is not None:
            self.source_adapter.sync_to(self.target_adapter, flags=self.diffsync_flags)
        else:
            self.log_warning(message="Not both adapters were properly initialized.")


jobs = [NetvsDataSource, ]
