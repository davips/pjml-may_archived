from pjml.tool.abc.configless import ConfigLess


class Shrink(ConfigLess):
    def _apply_impl(self, collection):
        return self._use_impl(collection)

    def _use_impl(self, collection):
        newcoll = collection.updated(
            transformations=self._transformations(),
            datas=[d for d in collection if not d.isphantom],
            failure=collection.failure
        )
        if newcoll.size == 0:
            print('WW: All Nones')
            return None