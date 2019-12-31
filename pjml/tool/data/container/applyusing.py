from functools import lru_cache

from pjml.tool.base.transformer import Transformer


class ApplyUsing(Transformer):
    """Run a 'use' step right after an 'apply' one.

    Useful to calculate training error in classifiers, which would otherwise
    return None in the 'apply' step."""

    def __init__(self, transformer):
        super().__init__({'transformer': transformer}, transformer, True)
        self.model = self.algorithm
        self.transformer = transformer

    def _apply_impl(self, data):
        self.transformer.apply(data)
        return self.transformer.use(data, internal=True)

    def _use_impl(self, data):
        return self.transformer.use(data, internal=True)

    @classmethod
    def _cs_impl(cls):
        pass

    # Saída do Apply não entra no Use, logo AppU precisa ser atômico.
    # @lru_cache()
    # def to_transformations(self, operation):
    #     lstu = self.transformer.to_transformations('u')
    #     if operation == 'a':
    #         lsta = self.transformer.to_transformations('a')
    #         return lsta + lstu
    #     else:
    #         return lstu
