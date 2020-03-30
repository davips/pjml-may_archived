from pjml.pipeline import Pipeline
from pjml.tool.collection.expand.partition import Partition
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map
from pjml.tool.data.communication.report import Report
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.flow.applyusing import ApplyUsing
from pjml.tool.data.flow.file import File
from pjml.tool.data.modeling.supervised.classifier.rf import RF
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC

from pjml.tool.data.processing.feature.binarize import Binarize

# pipe = Pipeline(File("iris.arff"), ApplyUsing(NB()), Metric(), Report())
from pjml.tool.data.processing.instance.sampler.under.random import UnderS

pipe = Pipeline(
    File("abalone3.arff"), Binarize(),
    Partition(),
    Map(
        UnderS(sampling_strategy='not minority'),
        RF(),
        Metric()
    ),
    # Summ(function='mean_std'),
    # Report('mean S --> $S')
)

model = pipe.apply()
# print(1111111111111111, model)
d2 = model.use()  # own_data=True)

# print(11111111111111, d2)
