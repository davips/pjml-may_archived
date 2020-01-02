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
from pjml.tool.data.processing.instance.sampler.over.rnd_over_sampler import ROS

datain = read_arff('iris.arff')


# ML 1 ========================================================================

pipe = Pipeline(
    evaluator(
        Cache(
            Seq(
                ApplyUsing(SVMC(kernel='linear')),
                Cache(Metric(function='accuracy')),
            ),
        )
    ),
    Report("{history.last.config['function']} $S for dataset {dataset.name}.")
)

print('--------')
save('/tmp/pipe', pipe)
#
# pipe = load('/tmp/pipe')
# print(pipe)

print(1111111111111111111111111111111)
pipe.apply(datain)
print(222222222222222222222222222221)
pipe.use(datain)
print(3333333333333333333333333333333)

# ML 2 ========================================================================
pipe = Pipeline(
    ROS(sampling_strategy='not minority'),

    NB('bernoulli'),
    Metric(function='accuracy'),
    Report('Accuracy: $r {history}'),

    DT(max_depth=2),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),

    SVMC(kernel='linear'),
    Metric(function='accuracy'),
    Report('Accuracy: $r'),
)
print(datain)
dataout = pipe.apply(datain)
dataout2 = pipe.use(datain)

print(dataout.history)
print(dataout2.history)
print('------------------')
print(SVMC.cs())

print('------------------')
print(SVMC.cs().sample())
Report('Mean $s for dataset {dataset.name}.')


