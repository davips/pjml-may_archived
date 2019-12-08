from functools import partial

import numpy


class Parameter:
    def __init__(self, func, **kwargs):
        self.func = partial(func, **kwargs)
        self.kwargs = kwargs

    def sample(self):
        return self.func()

    def __str__(self):
        return str(self.kwargs)
        # return '\n'.join([str(x) for x in self.kwargs.items()])

    __repr__ = __str__


class CatHP(Parameter):
    pass


class RealHP(Parameter):
    pass


class IntHP(Parameter):
    def sample(self):
        return numpy.round(self.func())


class FixedHP(Parameter):
    def __init__(self, value):
        super().__init__(lambda _: value)
