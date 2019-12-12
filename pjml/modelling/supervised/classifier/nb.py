from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB

from pjml.modelling.supervised.predictor import Predictor
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class NB(Predictor):
    """Naive Bayes implementations: gaussian, bernoulli."""

    def __init__(self, distribution="gaussian"):
        self._configure(locals())
        self.distribution = distribution

        if self.distribution == "gaussian":
            self.algorithm = GaussianNB()
        elif self.distribution == "bernoulli":
            self.algorithm = BernoulliNB()
        else:
            raise Exception('Wrong distribution:', distribution)

    @classmethod
    def _cs_impl(cls):
        params = {
            'distribution': CatP(choice, items=['gaussian', 'bernoulli'])
        }
        return ConfigSpace(params=params)
