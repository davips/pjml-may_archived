from abc import ABC

from pjml.tool.base.seq import Seq
from pjml.tool.abc.container import Container


class Container1(Container, ABC):
    """Container for a single transformer.

    If more are given, they will be handled as a single Seq transformer."""
