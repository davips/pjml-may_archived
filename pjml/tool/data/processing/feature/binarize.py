import numpy as np
from sklearn.preprocessing import OneHotEncoder

from pjdata.data_creation import nominal_idxs
from pjml.tool.abc.configless import LightConfigLess
from pjml.tool.model import Model


class Binarize(LightConfigLess):
    def _apply_impl(self, data_apply):
        output_data = self._use_impl(data_apply, step='a')
        return Model(self, data_apply, output_data)

    def _use_impl(self, data, step='u'):
        # TODO: check Data object compatibility with applied one.
        # TODO: update Xt/Xd.
        data_nominal_idxs = nominal_idxs(data.Xt)
        encoder = OneHotEncoder()
        if len(data_nominal_idxs) > 0:
            nom = encoder.fit_transform(
                data.X[:, data_nominal_idxs]
            ).toarray()
            num = np.delete(data.X,
                            data_nominal_idxs, axis=1).astype(float)
            X = np.column_stack((nom, num))
            return data.updated(self.transformations(step), X=X)
        else:
            return data
