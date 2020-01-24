from sklearn.preprocessing import OneHotEncoder

from pjml.tool.common.configless import ConfigLess
import numpy as np


class Binarize(ConfigLess):
    def _apply_impl(self, data):
        self.nominal_idxs = [idx for idx, val in list(enumerate(data.Xt)) if
                             isinstance(val, list)]
        self.model = OneHotEncoder()
        self.model.fit(data.X[:, self.nominal_idxs])
        return self._use_impl(data)

    def _use_impl(self, data):
        # TODO: check Data object compatibility with applied one.
        nom = self.model.transform(data.X[:, self.nominal_idxs]).toarray()
        num = np.delete(data.X, self.nominal_idxs, axis=1).astype(float)
        X = np.column_stack((nom, num))
        return data.updated(self._transformations(), X=X)
