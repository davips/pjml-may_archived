from abc import ABC

from pjml.config.description.cs.emptycs import EmptyCS
from pjdata.aux.decorator import classproperty
from pjml.tool.abc.singleton import NoAlgorithm
from pjml.tool.abc.transformer import Transformer


class ConfigLess(Transformer, ABC):
    """Parent class of all transformers without config."""
    def __init__(self):
        super().__init__({}, deterministic=True)

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()
