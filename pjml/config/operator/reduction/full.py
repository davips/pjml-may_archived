from operator import itemgetter

from pjdata.data import NoData
from pjml.config.description.cs.finitecs import FiniteCS


# nonTODO: PEP 8 requires lowercase in function names; so is that ok to use a
#  class instead? Or should we change all operators to function/lowercase?
def full(cs, data=NoData, n=1, field='S'):
    """Exhaustive search to maximize value at 'field'.

    Return 'n' best pipelines."""
    # TODO: seed?
    if not isinstance(cs, FiniteCS):
        raise Exception('Exhaustive search is only possible on FiniteCS!')

    results = []
    for pipe in cs:
        pipe.apply(data)
        res = pipe.use(data).field(field).item(0)
        results.append((pipe, -res))

    print(len(results), '?')
    pipes = [x[0] for x in sorted(results, key=itemgetter(1))[:n]]
    return FiniteCS(trasformers=pipes)
