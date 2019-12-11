from numpy.random.mtrand import uniform
from sklearn.svm import SVC

from pjml.modelling.supervised.predictor import Predictor
from pjml.searchspace.configspace import ConfigSpace
from pjml.searchspace.distributions import choice
from pjml.searchspace.parameters import RealP, CatP, OrdP, IntP


class SVMC(Predictor):
    def __init__(self, **kwargs):
        self.config = kwargs
        self.algorithm = SVC(**self.config)

    @classmethod
    def _cs_impl(cls):
        # todo: set random seed; set 'cache_size'
        params = {
            'C': RealP(uniform, low=1e-4, high=100),
            'shrinking': CatP(choice, items=[True, False]),
            'probability': CatP(choice, items=[False]),
            'tol': OrdP(choice, items=[
                0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1,
                1, 10, 100, 1000, 10000
            ]),
            'class_weight': CatP(choice, items=[None, 'balanced']),
            # 'verbose': [False],
            'max_iter': CatP(choice, items=[1000000]),
            'decision_function_shape': CatP(choice, items=['ovr', 'ovo'])
        }

        kernel_linear = ConfigSpace(
            params={'kernel': CatP(choice, items=['linear'])}
        )

        kernel_poly = ConfigSpace({
            'kernel': CatP(choice, items=['poly']),
            'degree': IntP(uniform, low=0, high=10),
            'coef0': RealP(uniform, low=0.0, high=100)
        })

        kernel_rbf = ConfigSpace({
            'kernel': CatP(choice, items=['rbf'])
        })

        kernel_sigmoid = ConfigSpace({
            'kernel': CatP(choice, items=['sigmoid']),
            'coef0': RealP(uniform, low=0.0, high=100),
        })

        kernel_nonlinear = ConfigSpace(
            {'gamma': RealP(uniform, low=0.00001, high=100)},
            children=[kernel_poly, kernel_rbf, kernel_sigmoid]
        )

        return ConfigSpace(
            params=params,
            children=[kernel_linear, kernel_nonlinear]
        )
