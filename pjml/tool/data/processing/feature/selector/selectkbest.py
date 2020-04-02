from functools import partial

from sklearn.feature_selection import f_classif, mutual_info_classif, SelectPercentile, SelectFpr, SelectFdr, \
    SelectFwe, GenericUnivariateSelect, SelectKBest

from pjdata.step.use import Use
from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.data.algorithm import Algorithm
from pjml.tool.model import Model


class SelectKB(Algorithm):
    SCORE_FUNCTIONS = {
        "f_classif": f_classif,
        "mutual_info_classif": mutual_info_classif,
        "SelectPercentile": SelectPercentile,
        "SelectFpr": SelectFpr,
        "SelectFdr": SelectFdr,
        "SelectFwe": SelectFwe,
        "GenericUnivariateSelect": GenericUnivariateSelect
    }

    def __init__(self, **kwargs):
        internal_kwargs = kwargs.copy()
        if "score_func" in kwargs:
            internal_kwargs["score_func"] = self.SCORE_FUNCTIONS[kwargs["score_func"]]

        algorithm_factory = partial(SelectKBest, **internal_kwargs)
        super().__init__(kwargs, algorithm_factory)

    @classmethod
    def _cs_impl(cls):
        params = {
            'score_func': CatP(
                choice,
                items=[
                    "chi2", "f_classif", "mutual_info_classif",
                    "SelectPercentile", "SelectFpr", "SelectFdr",
                    "SelectFwe", "GenericUnivariateSelect"
                ]
            ),
        }
        return TransformerCS(Node(params=params))

    def _apply_impl(self, data):
        sklearn_model = self.algorithm_factory()
        X_new = sklearn_model.fit_transform(*data.Xy)
        applied = data.updated(self.transformations('a'), X=X_new)
        return Model(self, applied, sklearn_model)

    def _use_impl(self, data, sklearn_model=None):
        X_new = sklearn_model.transform(data.X)
        return data.updated(self.transformations('u'), X=X_new)

    def transformations(self, step):
        if step == 'a':
            return []
        elif step == 'u':
            return [Use(self, 0)]
        else:
            raise BadComponent('Wrong current step:', step)
