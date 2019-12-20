from itertools import repeat

from pjdata.data_creation import read_arff
from pjml.base.aux.seq import Seq
from pjml.base.pipeline import Pipeline
from pjml.concurrence.expand import Expand
from pjml.concurrence.map import Map
from pjml.concurrence.multi import Multi
from pjml.concurrence.reduce.summ import Summ
from pjml.config.lists import sampler, bag
from pjml.container.applyusing import ApplyUsing
from pjml.evaluation.metric import Metric
from pjml.flow.report import Report
from pjml.modelling.supervised.classifier.dt import DT
from pjml.modelling.supervised.classifier.nb import NB
from pjml.modelling.supervised.classifier.svmc import SVMC
from pjml.processing.instance.sampler.over.rnd_over_sampler import \
    RndOverSampler


def map(x):
    return 0


def seq(*x):
    return 0


def shuffle(*x):
    return 0


datain = read_arff('iris.arff')


# pipe = Pipeline(
#     RndOverSampler(sampling_strategy='not minority'),
#
#     NB('bernoulli'),
#     Metric(function='accuracy'),
#     Report('Accuracy: $r {history}'),
#
#     DT(max_depth=2),
#     Metric(function='accuracy'),
#     Report('Accuracy: $r'),
#
#     SVMC(kernel='linear'),
#     Metric(function='accuracy'),
#     Report('Accuracy: $r'),
# )
# print(datain)
# dataout = pipe.apply(datain)
# dataout2 = pipe.use(datain)
#
# print(dataout.history)
# print(dataout2.history)
# print('------------------')
# print(SVMC.cs())
#
# print('------------------')
# print(SVMC.cs().sample())
# Report('Mean $s for dataset {dataset.name}.')


# ML ========================================================================
def evaluator(pipe):
    return Seq(
        Expand(),
        Multi(sampler(split_type='cv')),
        Map(pipe),
        Summ(function='mean_std')
    )


pipe = Pipeline(
    evaluator(
        Seq(ApplyUsing(SVMC(kernel='linear')), Metric(function='accuracy'))
    ),
    Report("{history.last.config['function']} $S for dataset {dataset.name}.")
)

pipe.apply(datain)
pipe.use(datain)

#
# # AutoML ===================================================================
# def evaluator(pipe):
#     # |CS| = |Seq.cs(*)| = |new_cs| = oo
#     return seq(
#         # |CS| = 1
#         Expand,
#
#         # |CS| = 1
#         Multi(sampler(split_type='cv')),
#
#         # |CS| = |Map.cs(pipe)| = |pipe.cs| = oo
#         map(pipe),
#
#         # |CS| = 1
#         Summ(function='mean_std')
#     )
#
#
# # workflow_to_eval = seq(shuffle(PCA, NR, Norm), SVMC)
# workflow_to_eval = seq(shuffle(Mark(PCA), Mutable(NR), Mark(Norm)), SVMC)
#
# workflow = evaluator(seq(workflow_to_eval, Metric(function='accuracy')))
#
# chosen = seq(Multi(Rnd(workflow, size=100)), Map(Report), Best())
# chosen = GA(workflow, data, size=1)
#
# pipeline = Pipeline(
#     chosen.sample(),
#     Report("{history.last.config['function']} $S for dataset {dataset.name}.")
# )
#
# pipe.apply(datain)
# pipe.use(datain)
#
#
# def ga(cs, data, size):
#     return Seq(   # Var()
#         Assign(X, Rnd(cs, size=100)),
#         Loop(
#             Expand(),
#             Multi(X),
#             Assign(Y, Select(n=10, field='s', function='max')),
#             Multi(Y),
#             Crossover(...),
#             Mutation(...),
#             Assign(X, CollectionToTransformers()),
#             Assign(Z, Rnd(cs, size=50)),
#             concat(X,Z)
#         )
#     )
#
#
#
# def rnd(cs, size):
#     return bag(*repeat(cs.sample(), size))
#
#
#
# seq(rnd(seq(ga(workflow, 100), SVMC), 100), Select(n=10, field='s',
# function='max'))
