from pjml.pipeline import Pipeline
from pjml.tool.collection.expand.partition import Partition
from pjml.tool.collection.reduce.summ import Summ
from pjml.tool.collection.transform.map import Map
from pjml.tool.data.communication.report import Report
from pjml.tool.data.evaluation.calc import Calc
from pjml.tool.data.evaluation.mconcat import MConcat
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.flow.applyusing import ApplyUsing
from pjml.tool.data.flow.file import File
from pjml.tool.data.flow.onlyoperation import OnlyApply, OnlyUse
from pjml.tool.data.manipulation.copy import Copy
from pjml.tool.data.modeling.supervised.classifier.rf import RF
from pjml.tool.data.processing.feature.binarize import Binarize
from pjml.tool.data.processing.feature.scaler.minmax import MinMax
from pjml.tool.data.processing.instance.sampler.over.random import OverS
from pjml.tool.data.processing.instance.sampler.under.random import UnderS
from pjml.tool.meta.wrap import Wrap

print('Construindo...')
pipe = Pipeline(
    OnlyApply(File("iris.arff")),
    # Binarize(),
    ApplyUsing(RF()),
    Partition(),
    Map(
        Wrap(
            MinMax(),
            ApplyUsing(RF()),
            OnlyApply(Metric(functions=['length'])),
            OnlyUse(Metric(functions=['accuracy', 'error'])),
            # AfterUse(Metric(function=['diversity']))
        ),
    ),
    Summ(function='mean_std'),
    Report('$S'),

    # ApplyUsing(RF()),
    # Partition(),
    # Map(
    #     Wrap(
    #         MinMax(),
    #         ApplyUsing(RF()),
    #         OnlyApply(Metric(functions=['length'])),
    #         OnlyUse(Metric(functions=['accuracy', 'error'])),
    #         # AfterUse(Metric(function=['diversity']))
    #     ),
    # ),
    # Summ(function='mean_std'),
    # Report('$S'),
)

# pipe = Pipeline(
#     File("abalone3.arff"),
#     Binarize(),
#     Partition(),
#     Map(
#         UnderS(sampling_strategy='not minority'),
#         RF(),
#         Metric()
#     ),
#     Summ(function='mean_std'),
#     Report('mean S --> \n$S'),
#
#     Report('mean S --> $S'),
#     OnlyApply(Copy(from_field="S", to_field="B")),
#     OnlyUse(MConcat(input_field1="S", input_field2="S",
#                     output_field="S", direction='vertical')),
#     Calc(functions=['flatten']),
#     Report('mean S --> $S')
# )

print('Applying...')
model = pipe.apply()

print('DDDDDDD\n', model.data.history)
exit()
print('Using...')
d2 = model.use(File("iris.arff").apply().data)
