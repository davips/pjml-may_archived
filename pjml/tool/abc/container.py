from abc import ABC
from functools import lru_cache

from pjdata.aux.decorator import classproperty

from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
from pjml.tool.abc.transformer import HeavyTransformer


class Container(HeavyTransformer, NoDataHandler, ABC):
    """A container modifies 'transformer(s)'."""

    def __init__(self, transformers):
        if not transformers:
            raise Exception(
                f'A container ({self.name}) should have at least one '
                f'transformer!')
        super().__init__({'transformers': transformers})
        self.transformers = transformers

    @property
    @lru_cache()
    def wrapped(self):
        from pjml.tool.meta.wrap import Wrap
        for transformer in self.transformers:
            transformer = transformer.wrapped
            if isinstance(transformer, Wrap):
                return transformer
        return None

    @classmethod
    @classproperty
    def cs(cls):
        raise Exception(
            f'{cls.name} depends on transformers to build a CS.\n'
            f'Just instantiate the class {cls.name} instead of calling its .cs!'
        )

    @classmethod
    def _cs_impl(cls):
        raise Exception(f'Wrong calling of {cls.name}._cs_impl!')

    # def transformations(self, step=None):
    #     if step is None:
    #         step = self._current_step
    #     lst = []
    #     for tr in self.transformers:
    #         lst.append(tr.transformations(step, training_data))
    #     return flatten(lst)

    def __str__(self, depth=''):
        if not self._pretty_printing:
            return super().__str__()

        inner = []
        for t in self.transformers:
            inner.append('    ' + t.__str__(depth).replace('\n', '\n' + '    '))

        return f'{depth}{self.name}>>\n' + \
               '\n'.join(inner) + \
               f'\n{depth}<<{self.name}'
