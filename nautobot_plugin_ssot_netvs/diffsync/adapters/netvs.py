import os

import netdb_client.api32
import netdb_client.api32.nd
from diffsync import DiffSync
from django.conf import settings

from nautobot_plugin_ssot_netvs.diffsync.models.netvs import NetvsSubnet


class NetVSAdapter(DiffSync):
    """DiffSync Adapter for NetVS."""

    top_level = ["subnet"]
    subnet = NetvsSubnet

    def __init__(self, *args, job=None, sync=None, **kwargs):
        super().__init__(*args, **kwargs)
        PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_plugin_ssot_netvs"]
        self.job = job
        self.sync = sync
        self.base_url = PLUGIN_SETTINGS.get("netvs_base_url")
        self.token = PLUGIN_SETTINGS.get("netvs_token")

    def load(self):
        endpoint = netdb_client.api32.APIEndpoint(base_url=self.base_url, token=self.token)
        api = netdb_client.api32.APISession(endpoint=endpoint)

        for api_subnet in netdb_client.api32.nd.IpSubnet.list(api_session=api):
            subnet, created = self.get_or_instantiate(
                NetvsSubnet, ids={"cidr": api_subnet.cidr}, attrs={"bcd": api_subnet.bcd, "description": api_subnet.description}
            )
            self.add(subnet)
            if created:
                self.job.log_success(message=f"Successfully loaded prefix {subnet} from Netvs")
