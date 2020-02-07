from pjml.config.description.cs.finitecs import FiniteCS


def rnd(cs, n=5):
    """Reduces CS by random sampling."""
    # TODO: seed?
    return FiniteCS(cs.cs.sample for _ in range(n))
