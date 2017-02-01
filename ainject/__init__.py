from .ainject import *


__version__ = "0.0.2"
version = tuple(map(int, str.split(__version__, ".")))

__all__ = (
    ainject.__all__ +
    ("version", "__version__")
)
