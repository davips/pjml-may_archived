from abc import ABC
from functools import lru_cache

from pjml.tool.base.transformer import Transformer


class NoOp(Transformer, ABC):
    """Parent class of all inert transformers.

    They are useful, but do nothing to Data objects."""

    @classmethod
    def _cs_impl(cls):
        raise Exception(f'{cls.name} is a NoOp, it has no ConfigSpace.')

    @lru_cache()
    def to_transformations(self, operation):
        return []
