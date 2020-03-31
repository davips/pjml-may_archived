import numpy as np
from sklearn.metrics import accuracy_score

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.abc.mixin.functioninspector import FunctionInspector
from pjml.tool.model import Model
from pjml.tool.abc.transformer import Transformer2


class Metric(Transformer2, FunctionInspector):
    """Metric to evaluate a given Data field.

    Developer: new metrics can be added just following the pattern '_fun_xxxxx'
    where xxxxx is the name of the new metric.

    Parameters
    ----------
    functions
        Name of the function to use to evaluate data objects.
    target
        Name of the matrix with expected values.
    prediction
        Name of the matrix to be evaluated.
    """

    def __init__(self, functions=None, target='Y', prediction='Z'):
        if functions is None:
            functions = ['accuracy']
        super().__init__(self._to_config(locals()), deterministic=True)
        self.functions = functions
        self.target, self.prediction = target, prediction
        self.selected = [self.function_from_name[name] for name in functions]

    def _apply_impl(self, data):
        output_data = self._use_impl(data, step='a')
        return Model(self, output_data)

    def _use_impl(self, data_use, step='u'):
        if self.target not in data_use.matrices:
            raise Exception(
                f'Impossible to calculate metric {self.functions}: Field '
                f'{self.target} does not exist!')
        if self.prediction not in data_use.matrices:
            raise Exception(
                f'Impossible to calculate metric {self.functions}: Field '
                f'{self.prediction} does not exist!')
        return data_use.updated(
            self.transformations(step),
            R=np.array([[f(data_use, self.target, self.prediction)
                         for f in self.selected]])
        )

    @classmethod
    def _cs_impl(cls):
        # TODO target and prediction
        params = {
            'function': CatP(choice, items=cls.names()),
            'target': CatP(choice, items=['Y']),
            'prediction': CatP(choice, items=['Z'])
        }
        return TransformerCS(Node(params=params))

    @staticmethod
    def _fun_error(data, target, prediction):
        return 1 - accuracy_score(
            data.matrices[target], data.matrices[prediction]
        )

    @staticmethod
    def _fun_accuracy(data, target, prediction):
        return accuracy_score(
            data.matrices[target], data.matrices[prediction]
        )

    @staticmethod
    def _fun_length(data, target, prediction):
        return data.history.size
