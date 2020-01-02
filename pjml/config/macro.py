"""
Shortcuts of common pipelines.
"""
from pjml.config.list import sampler
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map, mapa
from pjml.tool.collection.transform.multi import multi
from pjml.tool.data.container.seq import seq


def evaluator(component, sampler=sampler(steps=10), function='mean_std'):
    return seq(
        Expand,
        multi(sampler),
        mapa(component),
        Summ(function=function)
    )
