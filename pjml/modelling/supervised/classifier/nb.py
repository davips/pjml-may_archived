from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB

from modelling.supervised.predictor import Predictor
from pjml.searchspace.configspace import ConfigSpace
from pjml.searchspace.distributions import choice
from pjml.searchspace.parameters import CatHP


class NB(Predictor):
    """Naive Bayes implementations: GaussianNB and BernoulliNB."""

    def __init__(self, **kwargs):
        self.config = kwargs
        self.nb_type = self.config['@nb_type']

        if self.nb_type == "GaussianNB":
            self.algorithm = GaussianNB()
        elif self.nb_type == "BernoulliNB":
            self.algorithm = BernoulliNB()
        else:
            raise Exception('Wrong NB!')

    @classmethod
    def _cs_impl(cls):
        params = {
            '@nb_type': CatHP(choice, items=['GaussianNB', 'BernoulliNB'])
        }
        return ConfigSpace(params)
