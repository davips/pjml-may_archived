from functools import lru_cache

from sklearn.metrics import accuracy_score

from pjml.base.aux.functioninspector import FunctionInspector
from pjml.base.component import Component
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class Metric(Component, FunctionInspector):
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
        return data.updated(self.transformation(), r=self.algorithm(data))

    @classmethod
    def _cs_impl(cls):
        # TODO target and prediction
        params = {
            'function': CatP(choice, items=cls.functions.keys())
        }
        return ConfigSpace(params=params)

    def _fun_error(self, data):
        return 1 - accuracy_score(
            data.matrices[self.target], data.matrices[self.prediction]
        )

    def _fun_accuracy(self, data):
        return accuracy_score(
            data.matrices[self.target], data.matrices[self.prediction]
        )
