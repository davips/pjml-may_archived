from operator import itemgetter

from pjml.config.description.cs.finitecs import FiniteCS


# nonTODO: PEP 8 requires lowercase in function names; so is that ok to use a
#  class instead? Or should we change all operators to function/lowercase?
def full(cs, data, n=1, field='s'):
    """Exhaustive search to maximize value at 'field'.

    Return 'n' best pipelines."""
    # TODO: seed?
    if isinstance(cs, FiniteCS):
        raise Exception('Exhaustive search is only possible on FiniteCS!')

    results = []
    for pipe in cs:
        pipe.apply(data)
        results.append((pipe, -pipe.use(data).s))

    return FiniteCS(x[0] for x in sorted(results, key=itemgetter(1))[:n])

