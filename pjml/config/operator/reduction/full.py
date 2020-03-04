from operator import itemgetter

from pjdata.data import NoData
from pjml.config.description.cs.configlist import ConfigList


# nonTODO: PEP 8 requires lowercase in function names; so is that ok to use a
#  class instead? Or should we change all operators to function/lowercase?
from pjml.tool.data.manipulation.keep import Keep


def full(cs, data=NoData, n=1, field='S'):
    """Exhaustive search to maximize value at 'field'.

    Return 'n' best pipelines."""
    # TODO: seed?
    if not isinstance(cs, ConfigList):
        raise Exception('Exhaustive search is only possible on FiniteCS!')

    results = []
    for pipe in cs:
        p = pipe
        result_data = p.apply()
        res = p.use(result_data).field(field, 'full search').item(0)
        results.append((p, -res))

    pipes = [x[0] for x in sorted(results, key=itemgetter(1))[:n]]
    return ConfigList(transformers=pipes)
