from nautobot.extras.models import Tag


def create_tag_sync_from_netvs():
    """Create tag for tagging objects that have been created by Infoblox."""
    tag, _ = Tag.objects.get_or_create(
        slug="ssot-synced-from-netvs",
        defaults={
            "name": "SSoT Synced from Netvs",
            "description": "Object synced at some point from Netvs",
            "color": "00876c",
        }
    )
    return tag

