from functools import partial

from sklearn.preprocessing import StandardScaler, MinMaxScaler

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.data.processing.feature.scaler.sklscaler import SKLScaler


class Std(SKLScaler):
    def __init__(self, operation='full'):
        if operation == 'full':
            with_mean, with_std = True, True
        else:
            with_mean, with_std = 'translate' == operation, 'scale' == operation

        algorithm_factory = partial(
            StandardScaler,
            with_mean=with_mean, with_std=with_std
        )
        config = {'operation': operation}
        super().__init__(config, algorithm_factory)

    @classmethod
    def _cs_impl(cls, data=None):
        params = {
            'operation':
                CatP(choice, items=['full', 'translate', 'scale'])
        }
        return TransformerCS(Node(params=params))
