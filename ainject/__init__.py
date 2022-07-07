from .ainject import *


__version__ = "0.0.3"
version = tuple(map(int, str.split(__version__, ".")))

__all__ = (
    ainject.__all__ +
    ("version", "__version__")
)
