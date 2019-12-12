from numpy import mean

from pjdata.data import Data
from pjml.concurrence.reduce.reduce import Reduce
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class Summ(Reduce):
    """Given a field, summarizes a Collection object to a Data object.

    The resulting Data object will have only the 's' field. To keep other
    fields, consider using a Keep containing all the concurrent part:
    Keep(Expand -> ... -> Summ).

    The collection history will be exported to the summarized Data object.
    """

    def __init__(self, field='r', function='mean'):
        self._configure(locals())
        self.algorithm = self.functions[function]
        self.field = field

    def _use_impl(self, collection):
        return Data(
            dataset=collection.dataset,
            history=collection.history.extended(self.transformation()),
            failure=collection.failure,
            s=self.algorithm(collection)
        )

    @classmethod
    def _cs_impl(cls):
        # TODO field
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        return ConfigSpace(params=params)

    def _fun_mean(self, collection):
        return mean([data.fields[self.field] for data in collection])
