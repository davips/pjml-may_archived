import json
from functools import lru_cache

from pjdata.aux.identifyable import Identifyable
from pjml.config.list import bag


class Transformer(Identifyable, dict):
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
        dict.__init__(self, transformer=name + '@' + path, config=config)

    def materialize(self):
        """Incarnate the respective component for this transformer.

        Returns
        -------
        A ready to use component.
        """
        class_ = self._get_class(self.path, self.name)
        return class_(**self.config)

    @property
    @lru_cache()
    def serialized(self):
        return json.dumps(self, sort_keys=True)

    @classmethod
    def deserialize(cls, txt):
        return cls._dict_to_transformer(json.loads(txt))

    @property
    @lru_cache()
    def transformer(self):
        """Helper function to avoid conditional Transformer vs Component.
        """
        return self

    @property
    @lru_cache()
    def cs(self=None):
        """Convert a transformer into a config space."""
        return bag(self)

    @classmethod
    def _dict_to_transformer(cls, dic):
        """Convert recursively a dict to a transformer."""
        if 'transformer' not in dic:
            raise Exception('Provided dict does not represent a transformer.')
        name, path = dic['transformer'].split('@')
        cfg = dic['config']
        if 'component' in cfg:
            cfg['component'] = cls._dict_to_transformer(cfg['component'])

        return Transformer(
            name=name, path=path,
            config=cfg
        )

    def _uuid_impl(self):
        return self.serialized

    @staticmethod
    def _get_class(module, class_name):
        import importlib
        module = importlib.import_module(module)
        class_ = getattr(module, class_name)
        return class_

    def __str__(self, depth=''):
        rows = '\n'.join([f'  {k}: {v}' for k, v in self.config.items()])
        return f'{self.name} "{self.path}" [\n{rows}\n]'
