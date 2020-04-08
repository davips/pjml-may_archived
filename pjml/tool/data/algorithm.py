from abc import ABC
from functools import partial

from pjml.tool.abc.heavytransformer import HeavyTransformer


class Algorithm(HeavyTransformer, ABC):
    """    Base class for scikitlearn algorithms.    """

    def __init__(self, config, func, kwargs=None, deterministic=False):
        super().__init__(config, deterministic)

        sklconfig = config if kwargs is None else kwargs

        if not deterministic:
            sklconfig = sklconfig.copy()

            # TODO: this won't be needed after defaults are enforced in all
            #  components.
            if 'seed' not in sklconfig:
                sklconfig['seed'] = 0

            sklconfig['random_state'] = sklconfig.pop('seed')

        self.algorithm_factory = partial(func, **sklconfig)
