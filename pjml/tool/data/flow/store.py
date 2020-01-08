from cururu.persistence import DuplicateEntryException
from cururu.storer import Storer
from pjdata.data import Data
from pjdata.dataset import Dataset
from pjml.config.cs.componentcs import ComponentCS
from pjml.config.distributions import choice
from pjml.config.node import Node
from pjml.config.parameter import FixedP, CatP
from pjml.tool.base.transformer import Transformer


class Store(Transformer, Storer):
    """Store a Data object onto a storage like MySQL, Pickle files, ...
        as a new dataset (beware of the darkness!). It is a NoOp.

    """

    def __init__(self, name, description='', fields=None,
                 engine='dump', settings=None):
        if fields is None:
            fields = ['X', 'Y']
        if settings is None:
            settings = {}
        config = self._to_config(locals())

        self._set_storage(engine, settings)

        self.dataset = Dataset(name, description)
        self.model = f'{name}-{description}'
        self.fields = fields

        super().__init__(config, self.model, deterministic=True)

    def _apply_impl(self, data):
        new_data = Data(
            self.dataset, data.history, data.failure, **data.matrices
        )
        try:
            self.storage.store(new_data, fields=self.fields)
        except DuplicateEntryException as e:
            print(e)
        return data

    def _use_impl(self, data):
        new_data = Data(
            self.dataset, data.history, data.failure, **data.matrices
        )
        try:
            self.storage.store(new_data, fields=self.fields)
        except DuplicateEntryException as e:
            print(e)
        return data

    @classmethod
    def _cs_impl(cls):
        params = {
            'engine': CatP(choice, items=['dump', 'mysql', 'sqlite']),
            'settings': FixedP({})
        }
        return ComponentCS(Node(params=params))
