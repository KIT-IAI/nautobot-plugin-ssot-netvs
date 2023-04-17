"""Nautobot Adapter for netvs SSoT plugin."""

from diffsync import DiffSync
from nautobot.ipam.models import Prefix

from nautobot_plugin_ssot_netvs.diffsync.models.base import Subnet
from nautobot_plugin_ssot_netvs.diffsync.models.nautobot import NautobotPrefix
from nautobot_plugin_ssot_netvs.diffsync.utils import create_tag_sync_from_netvs


class NautobotAdapter(DiffSync):
    """DiffSync adapters for Nautobot."""

    top_level = ["subnet"]
    subnet = NautobotPrefix

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Nautobot.
        Args:
            job (object, optional): Nautobot job. Defaults to None.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load(self):
        """Load data from Nautobot into DiffSync models."""
        for prefix in Prefix.objects.filter(tags__in=(create_tag_sync_from_netvs(),)).all():
            diffsync_subnet = NautobotPrefix(cidr=prefix.prefix.__str__(), bcd=prefix.description, description=prefix.cf['netvs-description'])
            self.add(diffsync_subnet)
            self.job.log_success(message=f"Successfully loaded prefix {prefix} from Nautobot.")
