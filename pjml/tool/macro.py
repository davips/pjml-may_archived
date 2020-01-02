"""
Shortcuts of common pipelines.
"""
from pjml.config.list import sampler
from pjml.tool.base.seq import Seq
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map
from pjml.tool.collection.transform.multi import Multi


def evaluator(transformer, sampler=sampler(steps=10), function='mean_std'):
    return Seq(
        Expand(),
        Multi(*sampler),
        Map(transformer),
        Summ(function=function)
    )
