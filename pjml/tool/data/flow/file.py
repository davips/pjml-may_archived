from pjdata.data import NoData
from pjdata.data_creation import read_arff
from pjml.config.cs.componentcs import ComponentCS
from pjml.config.node import Node
from pjml.config.parameter import FixedP
from pjml.tool.base.transformer import Transformer
from pjml.tool.common.transformernodatafriendly import TransformerNoDataFriendly


class File(TransformerNoDataFriendly):
    """Source of Data object from CSV, ARFF, file.

    TODO: always classification task?
    There will be no transformations (history) on the generated Data.

    A short hash will be added to the name, to ensure unique names.
    Actually, the first collision is expected after 12M different datasets
    with the same name ( 2**(log(107**7, 2)/2) ).
    Since we already expect unique names like 'iris', and any transformed
    dataset is expected to enter the system through a transformer,
    12M should be safe enough. Ideally, a single 'iris' be will stored.
    In practice, no more than a dozen are expected.
    """

    def __init__(self, name, path='./'):
        config = self._to_config(locals())
        if not path.endswith('/'):
            raise Exception('Path should end with /', path)
        if name.endswith('arff'):
            data = read_arff(path + name)
        else:
            raise Exception('Unrecognized file extension:', name)
        super().__init__(config, data, deterministic=True)
        self.model = data
        self.data = data

    def _apply_impl(self, data):
        if data is not NoData:
            raise Exception('File component needs to be applied with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    def _use_impl(self, data):
        if data is not NoData:
            raise Exception('File component needs to be used with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    @classmethod
    def _cs_impl(cls):
        params = {
            'path': FixedP('./'),
            'name': FixedP('iris.arff')
        }
        return ComponentCS(Node(params=params))
