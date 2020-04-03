from functools import partial

from sklearn.preprocessing import MinMaxScaler

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.data.processing.feature.scaler.scaler import Scaler


class MinMax(Scaler):
    def __init__(self, **kwargs):
        algorithm_factory = partial(MinMaxScaler, **kwargs)
        super().__init__(kwargs, algorithm_factory)

    @classmethod
    def _cs_impl(cls):
        params = {
            'feature_range': CatP(choice, items=[(-1, 1), (0, 1)])
        }
        return TransformerCS(Node(params=params))
