from pjml.tool.abc.heavytransformer import HeavyTransformer
from pjml.tool.chain import Chain
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.model.model import Model


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
        config = self._to_config(locals())

        # config cleaning.
        if split_type == "cv":
            del config['test_size']
        elif split_type == "loo":
            del config['partitions']
            del config['partition']
            del config['test']
            del config['seed']
        elif split_type == 'holdout':
            pass
        else:
            raise Exception('Wrong split_type: ', split_type)

        super().__init__(config)
        from pjml.macro import split
        self.transformer = Chain(
            Expand(),
            split(split_type, partitions, test_size, seed, fields)
        )

    def _apply_impl(self, data):
        splitter_model = self.transformer.apply(data)
        applied = splitter_model.data.last_transformations_replaced(
            drop=self.transformer.size,
            transformation=self.transformations('a')[0]
        )

        return Model(self, data, applied, splitter_model=splitter_model)

    def _use_impl(self, data, splitter_model=None):
        used = splitter_model.use(data)
        return used.last_transformations_replaced(
            drop=self.transformer.size,
            transformation=self.transformations('u')[0]
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
