import json

from pjdata.identifyable import Identifyable


class Transformer(Identifyable):
    def __init__(self, name, path, config):
        """
        Parameters
        ----------
        name
            algorithm identification
            (e.g. python class that implements the algorithm)
        path
            algorithm location
            (e.g. python module that contains the class)
        config
            dictionary with algorithm arguments
        """
        self.name = name
        self.path = path
        self.config = config

    def _uuid_impl(self):
        return self.name + self.path + json.dumps(self.config, sort_keys=True)
