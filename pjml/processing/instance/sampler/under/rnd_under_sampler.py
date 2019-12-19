from imblearn.under_sampling import RandomUnderSampler

from pjml.processing.instance.sampler.resampler import Resampler
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class RndUnderSampler(Resampler):
    def __init__(self, **kwargs):
        super().__init__(kwargs, RandomUnderSampler(**kwargs))

    @classmethod
    def _cs_impl(cls, data=None):
        params = {
            'sampling_strategy':
                CatP(choice, a=['not minority', 'not majority', 'all'])
        }
        return ConfigSpace(params=params)
