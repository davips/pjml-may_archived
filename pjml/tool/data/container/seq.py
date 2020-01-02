from functools import lru_cache

from pjdata.transformation import Transformation
from pjml.config.cs.seqcs import SeqCS
from pjml.tool.base.transformer import Transformer


def seq(*args, components=None):
    # TODO: convert components as classes to CSs?
    if components is None:
        components = args
    return Seq.cs(components=components)


class Seq(Transformer):
    """Chain the execution of the given transformers.

    Each arg is a transformer. Optionally, a list of them can be passed as a
    named arg called 'transformers'."""

    def __init__(self, *args, transformers=None):
        if transformers is None:
            transformers = args
        self.transformers = transformers
        super().__init__({'transformers': transformers}, transformers)
        # TODO: seed

    def _apply_impl(self, data):
        self.model = self.transformers
        for transformer in self.transformers:
            data = transformer.apply(data)
            if data and (data.failure is not None):
                raise Exception(
                    f'Applying subtransformer {transformer} failed! ',
                    data.failure)
        return data

    def _use_impl(self, data):
        for transformer in self.transformers:
            data = transformer.use(data)
            if data and (data.failure is not None):
                raise Exception(f'Using subtransformer {transformer} failed! ',
                                data.failure)
        return data

    @classmethod
    def _cs_impl(cls):
        raise Exception('Seq._cs_impl should never be called!')

    @classmethod
    def cs(cls, components):
        return SeqCS(components)

    @lru_cache()
    def to_transformations(self, operation):
        from itertools import chain
        lst = [tr.to_transformations(operation) for tr in self.transformers]
        return list(chain.from_iterable(lst))
