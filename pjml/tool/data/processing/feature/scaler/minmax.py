from sklearn.preprocessing import MinMaxScaler

from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import CatP
from pjml.tool.data.processing.feature.scaler.scaler import Scaler


class MinMax(Scaler):
    def __init__(self, **kwargs):
        super().__init__(kwargs, MinMaxScaler(**kwargs))

    @classmethod
    def _cs_impl(cls):
        params = {
            'feature_range': CatP(choice, items=[(-1, 1), (0, 1)])
        }
        return ComponentCS(Node(params=params))
