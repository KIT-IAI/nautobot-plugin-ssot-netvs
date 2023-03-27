from nautobot_plugin_ssot_netvs.diffsync.models.base import Subnet
from nautobot.ipam.models import Prefix
from nautobot.extras.models.statuses import Status

DEFAULT_STATUS = Status.objects.get(name="Active")


class NautobotPrefix(Subnet):
    """Nautobot implementation of the Subnet Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create prefix in Nautobot."""
        prefix = Prefix(prefix=ids["cidr"], description=attrs["bcd"], notes=attrs["description"], status=DEFAULT_STATUS)
        prefix.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update prefix in Nautobot"""
        prefix = Prefix.objects.get(prefix=self.cidr)
        prefix.description = self.bcd
        prefix.notes = self.description
        prefix.validated_save()
        return self

    def delete(self):
        """Delete prefix in Nautobot."""
        prefix = Prefix.objects.get(prefix=self.cidr)
        super().delete()
        prefix.delete()
        return self
