from abc import ABC

from pjml.config.description.cs.emptycs import EmptyCS
from pjml.tool.abc.transformer import HeavyTransformer, LightTransformer


class HeavyConfigLess(HeavyTransformer, ABC):
    """Parent class of all transformers without config."""

    def __init__(self):
        super().__init__({}, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()


class LightConfigLess(LightTransformer, ABC):
    """Parent class of all transformers without config."""

    def __init__(self):
        super().__init__({}, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()
