from abc import ABC

from pjml.tool.abc.transformer import Transformer


class NoDataHandler(Transformer, ABC):
    """All components that accept NoData should derive this class."""

