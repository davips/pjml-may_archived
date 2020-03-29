import numpy as np

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.abc.mixin.functioninspector import FunctionInspector
from pjml.tool.abc.singleton import NoAlgorithm, NoModel
from pjml.tool.abc.transformer import Transformer


class Copy(Transformer, FunctionInspector):
    """Calc to evaluate a given Data field.

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

    @classmethod
    def _cs_impl(cls):
        raise Exception('Not implemented!')

    def __init__(self, from_field, to_field):
        super().__init__(self._to_config(locals()), deterministic=True)
        self.from_field, self.to_field = from_field, to_field

    def _apply_impl(self, data):
        return self._use_impl(data)

    def _use_impl(self, data):
        for field in [self.from_field]:
            if field not in data.matrices:
                raise Exception(
                    f'Impossible to copy: Field '
                    f'{field} does not exist!')

        dic = {
            self.to_field: data.field(self.from_field, self)
        }

        return data.updated(self.transformations(), **dic)
