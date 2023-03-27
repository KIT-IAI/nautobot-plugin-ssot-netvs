from diffsync import DiffSyncModel
from typing import Optional


class Subnet(DiffSyncModel):
    """Subnet model."""

    _modelname = "subnet"
    _identifiers = ("cidr",)
    _attributes = ("description", "bcd")

    cidr: str
    bcd: str
    description: Optional[str]
