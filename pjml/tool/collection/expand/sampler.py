from pjml.tool.base.transformer import Transformer


class Sampler(Transformer):
    """Class to perform, e.g. Expand+kfoldCV.

    This task is already done by function sampler,
    but if performance becomes a concern, this less modular solution is a
    good choice."""

    # Version that would break the architecture, because of the need for a
    # super component Sampler = expand + container + finiteconfigspace.

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
    #     return data.updated(self.transformation(), **new_dic)
    #
    # def _apply_impl(self, data):
    #     self.model = self.algorithm
    #     return self._core(data, self.train_indexes)
    #
    # def _use_impl(self, data):
    #     return self._core(data, self.test_indexes)
