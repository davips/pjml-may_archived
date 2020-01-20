from imblearn.over_sampling import RandomOverSampler

from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import CatP
from pjml.tool.data.processing.instance.sampler.resampler import Resampler


class OverS(Resampler):
    def __init__(self, **kwargs):
        super().__init__(kwargs, RandomOverSampler(**kwargs))

    @classmethod
    def _cs_impl(cls, data=None):
        params = {
            'sampling_strategy':
                CatP(choice, items=['not minority', 'not majority', 'all'])
        }
        return ComponentCS(Node(params=params))
