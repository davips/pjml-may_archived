from pjml.pipeline import Pipeline
from pjml.tool.data.communication.report import Report
from pjml.tool.data.evaluation.metric import Metric
from pjml.tool.data.evaluation.split import Split
from pjml.tool.data.flow.applyusing import ApplyUsing
from pjml.tool.data.flow.file import File
from pjml.tool.data.manipulation.keep import Keep
from pjml.tool.data.modeling.supervised.classifier.dt import DT
from pjml.tool.data.modeling.supervised.classifier.nb import NB
from pjml.tool.data.modeling.supervised.classifier.svmc import SVMC

from pjml.tool.data.processing.feature.binarize import Binarize

# pipe = Pipeline(File("iris.arff"), ApplyUsing(NB()), Metric(), Report())
pipe = Pipeline(File("abalone3.arff"), Binarize(),
                Split(),
                ApplyUsing(NB()), Metric(), Report(),
                ApplyUsing(SVMC()), Metric(), Report())

model = pipe.apply()
# print(1111111111111111, model)
d2 = model.use()  # own_data=True)

# print(11111111111111, d2)
