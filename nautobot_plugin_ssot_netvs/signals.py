from nautobot.extras.choices import CustomFieldTypeChoices


def nautobot_database_ready_callback(sender, *, apps, **kwargs):
    content_type = apps.get_model("contenttypes", "ContentType")
    custom_field = apps.get_model("extras", "CustomField")
    prefix = apps.get_model("ipam", "Prefix")
    tag = apps.get_model("extras", "Tag")
    custom_field, _ = custom_field.objects.get_or_create(
        type=CustomFieldTypeChoices.TYPE_TEXT,
        name="netvs-description",
        defaults={
            "label": "Netvs Description",
        },
    )
    custom_field.content_types.add(content_type.objects.get_for_model(prefix))
    tag.objects.get_or_create(
        slug="ssot-synced-from-netvs",
        defaults={
            "name": "SSoT Synced from Netvs",
            "description": "Object synced at some point from Netvs",
            "color": "00876c",
        }
    )
