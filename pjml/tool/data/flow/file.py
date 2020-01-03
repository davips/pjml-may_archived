from pjdata.data_creation import read_arff
from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import CatP
from pjml.tool.base.aux.singleton import NoData
from pjml.tool.base.transformer import Transformer


class File(Transformer):
    def __init__(self, name, path='.'):
        config = self._to_config(locals())
        if name.endswith('arff'):
            data = read_arff(path + '/' + name)
        else:
            raise Exception('Unrecognized file extension:', name)
        super().__init__(config, data, isdeterministic=True)
        self.model = data
        self.data = data

    def _apply_impl(self, data):
        if data is not NoData:
            raise Exception('File component needs to be applied with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    def _use_impl(self, data):
        return self.data

    @classmethod
    def _cs_impl(cls):
        params = {
            'path': CatP(choice, items=['.']),
            'name': CatP(choice, items=['iris.arff'])
        }
        return ComponentCS(Node(params=params))

