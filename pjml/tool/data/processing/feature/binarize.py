import numpy as np
from sklearn.preprocessing import OneHotEncoder

from pjdata.data_creation import nominal_idxs
from pjml.tool.abc.configless import ConfigLess
from pjml.tool.model import Model


class Binarize(ConfigLess):
    def _apply_impl(self, data_apply):
        self.nominal_idxs = nominal_idxs(data_apply.Xt)
        self.model = OneHotEncoder()
        if len(self.nominal_idxs) > 0:
            self.model.fit(data_apply.X[:, self.nominal_idxs])

        def use_impl(data_use, step='u'):
            # TODO: check Data object compatibility with applied one.
            # TODO: update Xt/Xd.

            if len(self.nominal_idxs) > 0:
                nom = self.model.transform(
                    data_use.X[:, self.nominal_idxs]).toarray()
                num = np.delete(data_use.X, self.nominal_idxs, axis=1).astype(
                    float)
                X = np.column_stack((nom, num))
                return data_use.updated(self.transformations(step), X=X)
            else:
                return data_use

        output_data = use_impl(data_apply, step='a')
        return Model(output_data, self, use_impl)
