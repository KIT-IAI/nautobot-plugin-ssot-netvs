import django.db.utils
import nautobot.ipam.models

from nautobot_plugin_ssot_netvs.diffsync.models.base import Subnet
from nautobot.ipam.models import Prefix
from nautobot.extras.models.statuses import Status
from nautobot_plugin_ssot_netvs.diffsync.utils import create_tag_sync_from_netvs

try:
    DEFAULT_STATUS = Status.objects.get(name="Active")
except django.db.utils.ProgrammingError:
    pass

from pprint import pprint
class NautobotPrefix(Subnet):
    """Nautobot implementation of the Subnet Model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create prefix in Nautobot."""
        prefix = Prefix(prefix=ids["cidr"], description=attrs["bcd"], status=DEFAULT_STATUS)
        prefix.cf['netvs-description'] = attrs["description"]
        prefix.tags.add(create_tag_sync_from_netvs())
        prefix.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update prefix in Nautobot"""
        prefix = Prefix.objects.get(prefix=self.cidr)
        if attrs.get("bcd"):
            prefix.description = attrs["bcd"]
        if attrs.get("description"):
            prefix.cf['netvs-description'] = attrs["description"]
        prefix.validated_save()
        return self

    def delete(self):
        """Delete prefix in Nautobot."""
        prefix = Prefix.objects.get(prefix=self.cidr)
        super().delete()
        prefix.delete()
        return self
