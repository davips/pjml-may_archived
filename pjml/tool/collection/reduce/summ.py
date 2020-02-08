import numpy
from numpy import mean
from numpy import std

from pjdata.data import Data
from pjml.config.description.cs.componentcs import ComponentCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
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
        self.function = self.functions[function]
        super().__init__(self._to_config(locals()), self.function, True)
        self.field = field

    def _use_impl(self, collection):
        if collection.has_nones:
            collection = Shrink().apply(collection)
            print("Warning: collections containing Nones are shrunk before "
                  "summarization.")
        if collection is None:
            return None
        data = Data(
            dataset=collection.dataset,
            history=collection.history,
            failure=collection.failure
        )
        res = self.function(collection)
        if isinstance(res, tuple):
            summ = numpy.array([res])
            return data.updated(self._transformations(), S=summ)
        else:
            return data.updated(self._transformations(), s=res)

    @classmethod
    def _cs_impl(cls):
        params = {
            'function': CatP(choice, items=cls.functions.keys()),
            'field': CatP(choice, items=['z', 'r', 's'])
        }
        return ComponentCS(Node(params))

    def _fun_mean(self, collection):
        return mean([data.field(self.field, self) for data in collection])

    def _fun_std(self, collection):
        return std([data.field(self.field, self) for data in collection])

    def _fun_mean_std(self, collection):
        # TODO?: optimize calculating mean and stdev together
        values = [data.field(self.field, self) for data in collection]
        return mean(values), std(values)
