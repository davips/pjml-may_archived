from functools import lru_cache

from sklearn.metrics import accuracy_score

from pjml.base.component import Component
from pjml.searchspace.configspace import ConfigSpace
from pjml.searchspace.distributions import choice
from pjml.searchspace.parameters import CatP


class Metric(Component):
    """Metric to evaluate a given Data field.

    Developer: new metrics can be added just following the pattern '_fun_xxxxx'
    where xxxxx is the name of the new metric.

    Parameters
    ----------
    function
        Name of the function to use to evaluate data objects.
    target
        Name of the matrix with expected values.
    prediction
        Name of the matrix to be evaluated.
    """

    def __init__(self, function, target='Y', prediction='Z'):
        self.config = locals()
        self.isdeterministic = True
        self.algorithm = self.functions[function]
        self.target, self.prediction = target, prediction

    def _apply_impl(self, data):
        self.model = self.algorithm
        return self._use_impl(data)

    def _use_impl(self, data):
        return data.updated(self, r=self.algorithm(data))

    @classmethod
    def _cs_impl(cls):
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        return ConfigSpace(params=params)

    @property
    @lru_cache()
    def functions(self):
        """Map each metric to its corresponding function."""
        return {name.split('_fun_')[1]: getattr(self, name)
                for name in dir(self) if '_fun' in name}

    def _fun_error(self, data):
        return 1 - accuracy_score(
            data.matrices[self.target], data.matrices[self.prediction]
        )

    def _fun_accuracy(self, data):
        return accuracy_score(
            data.matrices[self.target], data.matrices[self.prediction]
        )
