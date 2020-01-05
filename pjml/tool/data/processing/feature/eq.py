from operator import itemgetter

from pjml.tool.base.singleton import NoAlgorithm
from pjml.tool.common.configless import ConfigLess
import numpy as np
from bisect import bisect

class Eq(ConfigLess):
    def __init__(self):
        super().__init__({}, NoAlgorithm, deterministic=True)

    def _apply_impl(self, data):
        newX = []
        for xs in np.transpose(data.X):
            xso = sorted(enumerate(xs), key=itemgetter(1))
            xs2 = sorted(self._enumerate(xso), key=itemgetter(1))
            newxs = [x[0] for x in xs2]
            newX.append(newxs)
        np.transpose(newX)

    def _use_impl(self, data):
        self.

    def _convert(self,x):
        bisect(self.mo)  # precisa remover repetidos, repartir o espaço original

    def _enumerate(self, lst):
        """Enumerate a sorted list, repeating the index for duplicate values."""
        idx = 0
        old = lst[0]
        res = []
        for x in lst:
            if x > old:
                idx += 1
            old = x
            res.append((idx, x))
        return res