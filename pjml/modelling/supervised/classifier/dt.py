from numpy.random import choice, uniform
from sklearn.tree import DecisionTreeClassifier

from modelling.supervised.predictor import Predictor
from searchspace.configspace import ConfigSpace
from searchspace.parameters import CatP, IntP, RealP


class DT(Predictor):
    """Decision Tree."""

    def __init__(self, **kwargs):
        self.config = kwargs
        self.algorithm = DecisionTreeClassifier(**kwargs)

    @classmethod
    def _cs_impl(cls):
        params = {
            'criterion': CatP(choice, a=['gini', 'entropy']),
            'splitter': CatP(choice, a=['best']),
            'class_weight': CatP(choice, a=[None, 'balanced']),
            'max_features': CatP(choice, a=['auto', 'sqrt', 'log2', None]),

            'max_depth': IntP(uniform, low=2, high=1000),

            'min_samples_split': RealP(uniform, low=1e-6, high=0.3),
            'min_samples_leaf': RealP(uniform, low=1e-6, high=0.3),
            'min_weight_fraction_leaf': RealP(uniform, low=0.0, high=0.3),
            'min_impurity_decrease': RealP(uniform, low=0.0, high=0.2)
        }
        return ConfigSpace(params)
