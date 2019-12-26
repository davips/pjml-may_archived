from abc import ABC

from pjml.config.cs.configspace import ConfigSpace


class FiniteConfigSpace(ConfigSpace, ABC):
    """Iterable tree representing a finite set of (hyper)parameter spaces.

    TODO: expand it to traverse more than just the top level nested nodes.
    TODO: decide if prohibition of RealP will be enforced.
    """

    def __init__(self, trasformers):
        self.trasformers = trasformers
        self.current_index = 0
        self.size = len(self.trasformers)

    def __iter__(self):
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index >= self.size:
            self.current_index = 0
            raise StopIteration('No more Data objects left.')
        return self.trasformers[self.current_index]
