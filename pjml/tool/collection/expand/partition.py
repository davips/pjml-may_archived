from pjml.tool.abc.transformer import HeavyTransformer
from pjml.tool.chain import Chain
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.model import Model


class Partition(HeavyTransformer):
    """Class to perform, e.g. Expand+kfoldCV.

    This task is already done by function split(),
    but if performance becomes a concern, this less modular solution is a
    good choice.

    TODO: the current implementation is just an alias for the nonoptimized
        previous solution.
    """

    def __init__(self, split_type='cv', partitions=10, test_size=0.3, seed=0,
                 fields=None):
        if fields is None:
            fields = ['X', 'Y']
        super().__init__(self._to_config(locals()))
        from pjml.macro import split
        self.transformer = Chain(
            Expand(),
            split(split_type, partitions, test_size, seed, fields)
        )

    def _apply_impl(self, data_apply):
        splitter_model = self.transformer.apply(data_apply)
        applied = splitter_model.data.last_transformation_replaced(
            self.transformations('a')[0]
        )

        return Model(self, applied, splitter_model)

    def _use_impl(self, data_use, splitter_model=None):
        used = splitter_model.use(data_use)
        return used.last_transformation_replaced(
            self.transformations('u')[0]
        )

    @classmethod
    def _cs_impl(cls):
        raise NotImplementedError

    # TODO: draft of optimized solution:
    # def __init__(self, train_indexes, test_indexes, fields=None):
    #     if fields is None:
    #         fields = ['X', 'Y']
    #     self.config = locals()
    #     self.isdeterministic = True
    #     self.algorithm = fields
    #     self.train_indexes = train_indexes
    #     self.test_indexes = test_indexes
    #
    # def _core(self, data, idxs):
    #     new_dic = {f: data.get_matrix(f)[idxs] for f in self.algorithm}
    #     return data.updated(self._transformation(), **new_dic)
    #
    # def _apply_impl(self, data):
    #     self.model = self.algorithm
    #     return self._core(data, self.train_indexes)
    #
    # def _use_impl(self, data):
    #     return self._core(data, self.test_indexes)
