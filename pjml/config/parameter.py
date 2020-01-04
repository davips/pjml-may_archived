import traceback
from functools import partial

import numpy


class Param(dict):
    """Base class for all kinds of algorithm (hyper)parameters."""

    def __init__(self, function, **kwargs):
        dic = kwargs.copy()
        dic['function'] = function.__name__
        dict.__init__(self, dic)  # For pretty printing.

        self.function = partial(function, **kwargs)
        self.kwargs = kwargs

    def sample(self):
        try:
            return self.function()
        except Exception as e:
            traceback.print_exc()
            print(e)
            print('Problems sampling: ', self)
            exit(0)


class CatP(Param):
    pass


class SubP(Param):
    """Subset of values."""
    pass


class PermP(Param):
    """Permutation of a list."""
    pass


class OrdP(Param):
    pass


class RealP(Param):
    pass


class IntP(Param):
    def sample(self):
        try:
            return numpy.round(self.function())
        except Exception as e:
            traceback.print_exc()
            print(e)
            print('Problems sampling: ', self)
            exit(0)


class FixedP(Param):
    def __init__(self, value):
        super().__init__(lambda: value)
