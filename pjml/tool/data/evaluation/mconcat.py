import numpy as np

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.abc.mixin.functioninspector import FunctionInspector
from pjml.tool.abc.transformer import LightTransformer
from pjml.tool.model import Model


class MConcat(LightTransformer, FunctionInspector):
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

    def __init__(self, input_field1, input_field2, output_field, direction):
        super().__init__(self._to_config(locals()), deterministic=True)
        self.input_field1, self.input_field2 = input_field1, input_field2
        self.output_field = output_field

        if direction == 'vertical':
            self.direction = 1
        elif direction == 'horizontal':
            self.direction = 0
        else:
            raise Exception(
                f"Wrong parameter: "
                f"direction = {direction}."
            )

    def _apply_impl(self, data):
        applied = self._use_impl(data, step='a')
        return Model(self, data, applied)

    def _use_impl(self, data, step='u'):
        m1 = data.field(self.input_field1, self)
        m2 = data.field(self.input_field2, self)
        dic = {
            self.output_field: np.concatenate(
                (m1, m2), axis=self.direction
            )
        }
        return data.updated(
            self.transformations(step), **dic
        )

    @classmethod
    def _cs_impl(cls):
        # TODO target and prediction
        params = {
            'input_field1': CatP(choice, items=['S']),
            'input_field2': CatP(choice, items=['S']),
            'direction': CatP(choice, items=[0, 1]),
            'output_field': CatP(choice, items=['S'])
        }
        return TransformerCS(Node(params=params))
