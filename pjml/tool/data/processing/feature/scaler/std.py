from sklearn.preprocessing import StandardScaler, MinMaxScaler

from pjml.config.description.cs.componentcs import ComponentCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.data.processing.feature.scaler.scaler import Scaler


class Std(Scaler):
    def __init__(self, operation='full'):
        if operation == 'full':
            with_mean, with_std = True, True
        else:
            with_mean, with_std = 'translate' in operation, 'scale' in operation

        super().__init__({'operation': operation},
                         StandardScaler(with_mean=with_mean, with_std=with_std),
                         deterministic=True)

    @classmethod
    def _cs_impl(cls, data=None):
        params = {
            'operation':
                CatP(choice, items=['full', 'translate', 'scale'])
        }
        return ComponentCS(Node(params=params))
