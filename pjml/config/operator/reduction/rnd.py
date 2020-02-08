from pjml.config.description.cs.finitecs import FiniteCS


def rnd(cs, n=100):
    """Reduces CS by random sampling."""
    # TODO: seed?
    return FiniteCS(trasformers=[cs.cs.sample() for _ in range(n)])
