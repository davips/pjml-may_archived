from pjml.tool.base.singleton import NoAlgorithm
from pjml.tool.common.configless import ConfigLess


class Shrink(ConfigLess):
    def _apply_impl(self, collection):
        return self._use_impl(collection)

    def _use_impl(self, collection):
        return collection.updated(
            transformation=self._transformation(),
            datas=[d for d in collection if d is not None],
            failure=collection.failure
        )
