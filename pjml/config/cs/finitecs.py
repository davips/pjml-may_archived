# TODO: FiniteCS parece bom para operações de redução de CS. Entretanto para
#  listas de transformers, essencialmente p/ Multi, parece que tuplas
#  são mais práticas, pois simplificam o construtor dele com *args, e permite
#  estender seu conceito para aceitar também listas de CSs.
#  Um possível problema é conflitar com o fruto proibido (loop infito?).

from pjml.config.cs.configspace import ConfigSpace
from pjml.config.distributions import choice


class FiniteCS(ConfigSpace):
    """Iterable tree representing a finite set of (hyper)parameter spaces.

    TODO: decide if prohibition of RealP will be enforced.
    """

    def sample(self):
        return choice(self)

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

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        return self.trasformers[idx]
