from abc import ABC

from pjml.config.description.cs.emptycs import EmptyCS
from pjdata.aux.decorator import classproperty
from pjml.tool.abc.singleton import NoAlgorithm
from pjml.tool.abc.transformer import Transformer2, Transformer1


class ConfigLess2(Transformer2, ABC):
    """Parent class of all transformers without config."""
    def __init__(self):
        super().__init__({}, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()


class ConfigLess1(Transformer1, ABC):
    """Parent class of all transformers without config."""
    def __init__(self):
        super().__init__({}, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()