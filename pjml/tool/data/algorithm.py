from abc import ABC
from functools import partial

from pjml.tool.abc.heavytransformer import HeavyTransformer
from pjml.tool.abc.lighttransformer import LightTransformer


class Algorithm:
    """    Base class for scikitlearn algorithms.    """

    def __init__(self, config, func, sklconfig=None, deterministic=False):
        sklconfig = config if sklconfig is None else sklconfig

        if not deterministic:
            sklconfig = sklconfig.copy()

            # TODO: this won't be needed after defaults are enforced in all
            #  components.
            if 'seed' not in sklconfig:
                sklconfig['seed'] = 0

            sklconfig['random_state'] = sklconfig.pop('seed')

        self.algorithm_factory = partial(func, **sklconfig)


class HeavyAlgorithm(Algorithm, HeavyTransformer, ABC):
    def __init__(self, config, func, sklconfig=None, deterministic=False):
        HeavyTransformer.__init__(self, config, deterministic)
        Algorithm.__init__(self, config, func, sklconfig, deterministic)
        # TODO: extend other Transformer args besides deterministic.


class LightAlgorithm(Algorithm, LightTransformer, ABC):
    def __init__(self, config, func, sklconfig=None, deterministic=False):
        LightTransformer.__init__(self, config, deterministic)
        Algorithm.__init__(self, config, func, sklconfig, deterministic)
