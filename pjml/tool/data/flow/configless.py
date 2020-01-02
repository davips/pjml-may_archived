from abc import ABC

from pjml.config.cs.emptycs import EmptyCS
from pjml.tool.base.aux.decorator import classproperty
from pjml.tool.base.transformer import Transformer


class ConfigLess(Transformer, ABC):
    """Parent class of all transformers without config."""

    @classmethod
    @classproperty
    def _cs_impl(cls):
        return EmptyCS()
