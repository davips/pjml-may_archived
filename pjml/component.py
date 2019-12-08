from abc import ABC, abstractmethod

from transformer import Transformer


class Component(ABC):
    config = {}

    def transformer(self):
        """
        Returns
        -------
        A Transformer object able to recreate this component from scratch.
        """
        name, path = self.__class__.__name__, self.__module__
        return Transformer(name, path, self.config)
