from .base import BaseModel

# Import modules, not classes, to avoid circular imports between request/property/notification.
# Import submodules so their classes register with the mapper registry.
from . import user
from . import course
from . import assignment
from . import enrollment
# add future models here as needed

__all__ = ["BaseModel"]