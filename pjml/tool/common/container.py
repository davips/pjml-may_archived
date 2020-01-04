from abc import ABC

from pjml.tool.base.aux.decorator import classproperty
from pjml.tool.base.transformer import Transformer


class Container(Transformer, ABC):
    """Container modify  'transformer(s)'."""

    # @property
    # @lru_cache()
    # def wrapped(self):
    #     """Subpipeline inside the first Wrap().
    #
    #     Example:
    #     pipe = Pipeline(
    #         File(name='iris.arff'),
    #         Wrap(Std(), SVMC()),
    #         Metric(function='accuracy')
    #     )
    #     pipe.wrapped  # -> Pipeline(Std(), SVMC())
    #     """
    #     while self.tr

    @classmethod
    @classproperty
    def cs(cls):
        raise Exception(
            f'{cls.name} depends on transformers to build a CS. Use CS '
            f'shortcut for class {cls.name} instead of calling its .cs!'
        )

    @classmethod
    def _cs_impl(cls):
        raise Exception(f'Wrong calling of {cls.name}._cs_impl!')
