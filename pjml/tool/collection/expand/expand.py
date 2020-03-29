from pjdata.infinitecollection import InfiniteCollection
from pjml.tool.abc.configless import ConfigLess
from pjml.tool.abc.invisible import Invisible
from pjml.tool.model import Model


class Expand(ConfigLess, Invisible):
    def _apply_impl(self, data_apply):
        def use_impl(data_use):
            return InfiniteCollection(
                data_use, data_use.history, data_use.failure, data_use.dataset
            )

        applied = use_impl(data_apply)
        return Model(applied, use_impl, self)
