import json

import numpy
from sklearn.model_selection import StratifiedShuffleSplit as HO, \
    StratifiedKFold as SKF, LeaveOneOut as LOO

from pjml.config.distributions import choice
from pjml.config.parameter import CatP
from pjml.tool.base.aux.functioninspector import FunctionInspector
from pjml.tool.base.transformer import Transformer


class Split(Transformer, FunctionInspector):
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

    def __init__(self, split_type='cv', steps=10,
                 partition=0, test=0.3, seed=0, fields=None):
        if fields is None:
            fields = ['X', 'Y']

        # Using 'self.algorithm' here to avoid 'algorithm' inside config.
        if split_type == "cv":
            self.algorithm = SKF(shuffle=True, n_splits=steps, random_state=seed)
        elif split_type == "loo":
            self.algorithm = LOO()
        elif split_type == 'holdout':
            self.algorithm = HO(n_splits=steps, test_size=test, random_state=seed)
        else:
            raise Exception('Wrong split_type: ', split_type)

        super().__init__(self._to_config(locals()), self.algorithm)

        self.steps = steps
        self.partition = partition
        self.test = test
        self.seed = seed
        self.fields = fields

    def _apply_impl(self, data):
        # TODO: Profile and if needed somehow optimize this without breaking
        #  pajé architecture.
        zeros = numpy.zeros(data.matrices[self.fields[0]].shape[0])
        partitions = list(self.algorithm.split(X=zeros, y=zeros))
        self.model = partitions[self.partition][1]
        return self._core(data, partitions[self.partition][0])

    def _use_impl(self, data):
        return self._core(data, self.model)

    def _core(self, data, idxs):
        new_dic = {f: data.matrices[f][idxs] for f in self.fields}
        return data.updated1(self._transformation(), **new_dic)

    @classmethod
    def _cs_impl(cls):
        # TODO CS for split
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        raise Exception('Split is not for external use for now!')
        # return ConfigSpace(params=params)
