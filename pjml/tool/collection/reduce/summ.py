import numpy
from numpy import mean
from numpy import std

from pjdata.data import Data
from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameter import CatP
from pjml.tool.collection.reduce.reduce import Reduce
from pjml.tool.collection.transform.shrink import Shrink


class Summ(Reduce):
    """Given a field, summarizes a Collection object to a Data object.

    The resulting Data object will have only the 's' field. To keep other
    fields, consider using a Keep containing all the concurrent part:
    Keep(Expand -> ... -> Summ).

    The collection history will be exported to the summarized Data object.
    """

    def __init__(self, field='r', function='mean'):
        super().__init__(self._to_config(locals()), self.functions[function], True)
        self.field = field

    def _use_impl(self, collection):
        if collection.has_nones:
            collection = Shrink().apply(collection)
            if len(collection.datas) == 0:
                print('WW: All Nones')
                return None
            else:
                print("Warning: collections containing Nones are shrunk before"
                      "summarization.")
        data = Data(
            dataset=collection.dataset,
            history=collection.history,
            failure=collection.failure
        )
        res = self.algorithm(collection)
        if isinstance(res, tuple):
            summ = numpy.array([res])
            return data.updated1(S=summ)
        else:
            return data.updated1(s=res)

    @classmethod
    def _cs_impl(cls):
        # TODO field
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        return ConfigSpace(params=params)

    def _fun_mean(self, collection):
        return mean([data.fields[self.field] for data in collection])

    def _fun_std(self, collection):
        return std([data.fields[self.field] for data in collection])

    def _fun_mean_std(self, collection):
        # TODO?: optimize calculating mean and stdev together
        values = [data.fields[self.field] for data in collection]
        return mean(values), std(values)
