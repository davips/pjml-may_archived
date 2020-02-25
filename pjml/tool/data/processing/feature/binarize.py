from sklearn.preprocessing import OneHotEncoder

from pjdata.data_creation import nominal_idxs
from pjml.tool.abc.configless import ConfigLess
import numpy as np


class Binarize(ConfigLess):
    def _apply_impl(self, data):
        self.nominal_idxs = nominal_idxs(data.Xt)
        self.model = OneHotEncoder()
        if len(self.nominal_idxs) > 0:
            self.model.fit(data.X[:, self.nominal_idxs])
        return self._use_impl(data)

    def _use_impl(self, data):
        # TODO: check Data object compatibility with applied one.
        # TODO: update Xt/Xd.

        if len(self.nominal_idxs) > 0:
            nom = self.model.transform(data.X[:, self.nominal_idxs]).toarray()
            num = np.delete(data.X, self.nominal_idxs, axis=1).astype(float)
            X = np.column_stack((nom, num))
            return data.updated(self.transformations(), X=X)
        else:
            return data
