from nautobot_plugin_ssot_netvs.diffsync.models.base import Subnet


class NetvsSubnet(Subnet):
    """Netvs implementation of the Subnet Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create prefix in NetVS."""
        raise NotImplementedError()

    def update(self, attrs):
        """Update prefix in Nautobot"""
        raise NotImplementedError()

    def delete(self):
        """Delete prefix in Nautobot."""
        raise NotImplementedError()
