from abc import ABC

from pjml.config.cs.emptycs import EmptyCS
from pjml.tool.base.aux.decorator import classproperty
from pjml.tool.base.singleton import NoAlgorithm
from pjml.tool.base.transformer import Transformer


class ConfigLess(Transformer, ABC):
    """Parent class of all transformers without config."""
    def __init__(self):
        super().__init__({}, NoAlgorithm, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()
