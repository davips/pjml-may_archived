import json

from aux.identifyable import Identifyable


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
            dictionary with algorithm parameters
        """
        self.name = name
        self.path = path
        self.config = config

    def create_object(self):
        """Incarnate the respective component for this transformer.

        Returns
        -------
        A ready to use component.
        """
        class_ = self._get_class(self.path, self.name)
        return class_(**self.config)

    def _uuid_impl(self):
        return self.name + self.path + json.dumps(self.config, sort_keys=True)

    @staticmethod
    def _get_class(module, class_name):
        import importlib
        module = importlib.import_module(module)
        class_ = getattr(module, class_name)
        return class_
