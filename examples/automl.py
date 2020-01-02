from cururu.file import save
from pjdata.data_creation import read_arff
from pjml.pipeline import Pipeline
from pjml.tool.base.macro import evaluator
from pjml.tool.data.container.applyusing import ApplyUsing
from pjml.tool.data.container.cache import Cache
from pjml.tool.data.container.seq import Seq
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.flow.report import Report
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC
import pjml.config.syntax
from pjml.tool.data.processing.feature.scaler.minmax import MinMax
from pjml.tool.data.processing.feature.scaler.std import Std
from pjml.tool.data.processing.instance.sampler.over.rnd_over_sampler import ROS
from pjml.tool.data.processing.instance.sampler.under.rnd_under_sampler import \
    RUS

datain = read_arff('iris.arff')

expr = [Std, {RUS, ROS}, MinMax], {DT, NB}
pipe = expr.sample()
print(pipe)

datain = read_arff('iris.arff')

dataout = pipe.apply(datain)
print(dataout.history)
# data morre no apply() do predictor

dataout = pipe.use(datain)
print(dataout.history)
# RUS desaparece no use()

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

