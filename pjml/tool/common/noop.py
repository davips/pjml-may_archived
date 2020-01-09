from abc import ABC

from pjml.tool.base.transformer import Transformer


class NoOp(Transformer, ABC):
    """Parent class of all inert transformers.

    They are useful, but do nothing to Data objects."""
