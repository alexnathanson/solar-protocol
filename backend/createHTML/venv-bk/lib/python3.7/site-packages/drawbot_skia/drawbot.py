from .drawing import Drawing
from .runner import makeDrawbotNamespace


__all__ = []
_db = Drawing()
_dbNamespace = makeDrawbotNamespace(_db)
globals().update(_dbNamespace)
__all__.extend(_dbNamespace.keys())
