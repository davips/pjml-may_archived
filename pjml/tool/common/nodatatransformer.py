from abc import ABC

from pjml.tool.base.transformer import Transformer


class NoDataTransformer(Transformer, ABC):
    """All components that accept NoData should derive this class."""

