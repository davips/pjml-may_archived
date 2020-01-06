from cururu.storer import Storer
from pjdata.data import NoData
from pjml.config.cs.componentcs import ComponentCS
from pjml.config.node import Node
from pjml.config.parameter import FixedP
from pjml.tool.common.nodatatransformer import NoDataTransformer


class Source(NoDataTransformer, Storer):
    """Source of Data object from a storage like MySQL, Pickle files, ...

    The first data object named 'name*' without transformations will be
    retrieved.

    #TODO: componente para recuperar resultados de transformação?"""

    def __init__(self, name, fields=None, engine='dump', settings=None):
        if fields is None:
            fields = ['X', 'Y']
        if settings is None:
            settings = {}
        config = self._to_config(locals())

        self._set_storage(engine, settings)
        lst = self.storage.list_by_name(name)
        if len(lst) == 0:
            raise Exception(f'{name} dataset not found!')
        phantom_data = lst[0]
        data = self.storage.fetch(phantom_data, fields=fields)
        if data is None:
            raise Exception('Dataset not found: ', phantom_data.name)
        self.model = self.data = data
        super().__init__(config, self.data, deterministic=True)

    def _apply_impl(self, data):
        if data is not NoData:
            raise Exception('Source component needs to be applied with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    def _use_impl(self, data):
        if data is not NoData:
            raise Exception('Source component needs to be used with NoData. '
                            'Use Sink before it if needed.')
        return self.data

    @classmethod
    def _cs_impl(cls):
        params = {
            'path': FixedP('./'),
            'name': FixedP('iris.arff')
        }
        return ComponentCS(Node(params=params))
