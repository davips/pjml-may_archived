from functools import lru_cache

from sklearn.metrics import accuracy_score

from pjml.base.aux.functioninspector import FunctionInspector
from pjml.base.component import Component
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class Split(Component, FunctionInspector):
    """Split a given Data field into training/apply set and testing/use set.

    Developer: new metrics can be added just following the pattern '_fun_xxxxx'
    where xxxxx is the name of the new metric.

    Parameters
    ----------
    train_indexes
        Indexes of rows to get from data objects during apply().
    test_indexes
        Indexes of rows to get from data objects during use().
    fields
        Name of the matrices to be modified.
    """

    def __init__(self, train_indexes, test_indexes, fields=None):
        if fields is None:
            fields = ['X', 'Y']
        self.config = locals()
        self.isdeterministic = True
        self.algorithm = fields
        self.train_indexes = train_indexes
        self.test_indexes = test_indexes

    def _core(self, data, idxs):
        new_dic = {f: data.get_matrix(f)[idxs] for f in self.algorithm}
        return data.updated(self.transformation(), **new_dic)

    def _apply_impl(self, data):
        self.model = self.algorithm
        return self._core(data, self.train_indexes)

    def _use_impl(self, data):
        return self._core(data, self.test_indexes)

    @classmethod
    def _cs_impl(cls):
        # TODO CS for split
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        raise Exception('Split is not for external use for now!')
        # return ConfigSpace(params=params)
