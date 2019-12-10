from functools import partial

import numpy

from searchspace.distributions import choice


class Param:
    """Base class for all kinds of algorithm (hyper)parameters."""

    def __init__(self, func, **kwargs):
        self.func = partial(func, **kwargs)
        self.kwargs = kwargs

    def sample(self):
        return self.func()

    def __str__(self):
        return str(self.kwargs)
        # return '\n'.join([str(x) for x in self.kwargs.items()])

    __repr__ = __str__


class CatP(Param):
    pass


class RealP(Param):
    pass


class IntP(Param):
    def sample(self):
        return numpy.round(self.func())


class FixedP(Param):
    def __init__(self, value):
        super().__init__(lambda _: value)
