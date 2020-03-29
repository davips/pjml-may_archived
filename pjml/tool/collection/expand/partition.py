from pjml.tool.abc.transformer import Transformer
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.chain import Chain


class Partition(Transformer):
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
        self.model = Chain(
            Expand(),
            split(split_type, partitions, test_size, seed, fields)
        )

    def _apply_impl(self, data):
        collection = self.model.apply(data)
        return collection.last_transformation_replaced(
            self.transformations()[0]
        )

    def _use_impl(self, data):
        collection = self.model.use(data)
        return collection.last_transformation_replaced(
            self.transformations()[0]
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
