from pjdata.data_creation import read_arff
from cururu.file import load
from cururu.compression import pack_object, unpack_object
from cururu.file import save
from pjdata.data_creation import read_arff
from pjml.config.list import sampler
from pjml.pipeline import Pipeline
from pjml.tool.collection.expand.expand import Expand
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map
from pjml.tool.collection.transform.multi import Multi
from pjml.tool.data.container.applyusing import ApplyUsing
from pjml.tool.data.container.cache import Cache
from pjml.tool.data.container.seq import Seq
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.flow.report import Report
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC

datain = read_arff('iris.arff')


# ML 1 ========================================================================
def evaluator(transformer):
    return Seq(
        Expand(),
        Multi(sampler(split_type='cv', steps=2)),
        Map(transformer),
        Summ(function='mean_std')
    )


pipe = Pipeline(
    evaluator(
        Cache(
            Seq(
                (SVMC(kernel='linear')),
                Cache(Metric(function='accuracy'))
            )
        )
    ),
    Report("{history.last.config['function']} $S for dataset {dataset.name}.")
)

print('--------')
# save('/tmp/pipe', pipe)
#
# pipe = load('/tmp/pipe')
# print(pipe)

print(1111111111111111111111111111111)
pipe.apply(datain)
print(222222222222222222222222222221)
pipe.use(datain)
print(3333333333333333333333333333333)

# ML 2 ========================================================================
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
