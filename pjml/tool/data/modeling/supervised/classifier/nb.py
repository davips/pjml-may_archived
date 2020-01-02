from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB

from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import CatP
from pjml.tool.data.modeling.supervised.predictor import Predictor


class NB(Predictor):
    """Naive Bayes implementations: gaussian, bernoulli."""

    def __init__(self, distribution="gaussian"):
        if distribution == "gaussian":
            algorithm = GaussianNB()
        elif distribution == "bernoulli":
            algorithm = BernoulliNB()
        else:
            raise Exception('Wrong distribution:', distribution)
        super().__init__({'distribution': distribution}, algorithm)
        self.distribution = distribution

    @classmethod
    def _cs_impl(cls):
        params = {
            'distribution': CatP(choice, items=['gaussian', 'bernoulli'])
        }
        return ComponentCS(Node(params=params))
