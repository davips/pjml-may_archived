from functools import partial

from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB

from pjml.config.description.cs.transformercs import TransformerCS
from pjml.config.description.distributions import choice
from pjml.config.description.node import Node
from pjml.config.description.parameter import CatP
from pjml.tool.data.modeling.supervised.predictor import Predictor


class NB(Predictor):
    """Naive Bayes implementations: gaussian, bernoulli."""

    def __init__(self, distribution="gaussian"):
        if distribution == "gaussian":
            algorithm_factory = partial(GaussianNB)
        elif distribution == "bernoulli":
            algorithm_factory = partial(BernoulliNB)
        else:
            raise Exception('Wrong distribution:', distribution)
        super().__init__({'distribution': distribution}, algorithm_factory)
        self.distribution = distribution

    @classmethod
    def _cs_impl(cls):
        params = {
            'distribution': CatP(choice, items=['gaussian', 'bernoulli'])
        }
        return TransformerCS(Node(params=params))
