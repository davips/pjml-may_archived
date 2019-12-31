from pjml.tool.collection.expand.expand import NoAlgorithm
from pjml.tool.base.transformer import Transformer


class Shrink(Transformer):
    def __init__(self):
        super().__init__({}, NoAlgorithm, isdeterministic=True)

    def _apply_impl(self, collection):
        return self._use_impl(collection)

    def _use_impl(self, collection):
        return collection.updated(self._transformation(),
                                  datas=[d for d in collection
                                         if d is not None],
                                  failure=collection.failure)

    @classmethod
    # TODO: define a CS that has a single transformer with zero parameters?
    def _cs_impl(cls):
        raise Exception(
            'TODO: define a CS that has a single transformer with zero '
            'parameters?')

# return ConfigSpace()
