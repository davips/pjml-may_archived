from abc import ABC

from pjml.tool.base.transformer import Transformer


class TransformerNoDataFriendly(Transformer, ABC):
    """All components that accept NoData should derive this class."""

