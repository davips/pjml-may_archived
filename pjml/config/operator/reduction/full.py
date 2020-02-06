from pjml.config.description.cs.finitecs import FiniteCS


# nonTODO: PEP 8 requires lowercase in function names; so is that ok to use a
#  class instead? Or should we change all operators to function/lowercase?
def full(cs, n=1, field='s'):
    """Exhaustive search to maximize value at 'field'.

    Return 'n' best pipelines."""
    # TODO: seed?
    if isinstance(cs, FiniteCS):
        raise Exception('Exhaustive search only possible on FiniteCS!')

    return FiniteCS(*[cs.cs.sample for _ in range(n)])
