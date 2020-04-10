import inspect
import traceback

from cururu.storer import Storer
from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.node import Node
from pjml.config.description.parameter import FixedP
from pjml.tool.abc.container1 import Container1
from pjml.tool.abc.transformer import Transformer
from pjml.tool.specialmodel import Model, CachedApplyModel


class Cache(Container1, Storer):
    def __new__(cls, *args, fields=None, engine="dump", settings=None, seed=0,
                transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            return object.__new__(cls)
        node = Node(params={
            'fields': FixedP(fields),
            'engine': FixedP(engine),
            'settings': FixedP(settings)
        })
        return ContainerCS(Cache.name, Cache.path, transformers, nodes=[node])

    def __init__(self, *args, fields=None, engine="dump", settings=None,
                 seed=0, transformers=None):
        if transformers is None:
            transformers = args
        if fields is None:
            fields = ['X', 'Y', 'Z']
        if settings is None:
            settings = {}
        config = self._to_config(locals())
        del config['args']
        super().__init__(config, seed, transformers, deterministic=True)

        self.fields = fields
        self._set_storage(engine, settings)

    def _apply_impl(self, data):
        # TODO: CV() is too cheap to be recovered from storage, specially if
        #  it is a LOO. Maybe transformers could inform whether they are cheap.

        transformations = self.transformer.transformations('a')
        hollow = data.hollow_extended(transformations=transformations)
        output_data = self.storage.fetch(hollow, self.fields, lock=True)

        # pra carregar modelo [outdated code here!!]:
        # self.transformer = self.storage.fetch_transformer(
        #     data, self.transformer, lock=True
        # )
        #
        # pra guardar modelo:
        # self.storage.store_transformer(self.transformer, self.fields,
        #                                check_dup=True)

        # Apply if still needed  ----------------------------------
        if output_data is None:
            try:
                # model usável
                model = self.transformer.apply(data, exit_on_error=False)
                output_data = model.data
            except:
                self.storage.unlock(data)
                traceback.print_exc()
                exit(0)

            # TODO: quando 'output_data is None', está gravando sem matrizes!
            #  Na hora de recuperar, isso precisa ser interpretado como None.
            data_to_store = hollow if output_data is None else output_data
            self.storage.store(data_to_store, self.fields, check_dup=False)
        else:
            # model não usável
            model = CachedApplyModel(self.transformer, data, output_data)

        return Model(self, data, model.data, model)

    def _use_impl(self, data, model=None):
        transformations = self.transformer.transformations('u')
        hollow = data.hollow_extended(transformations=transformations)
        output_data = self.storage.fetch(
            hollow, self.fields,
            training_data_uuid=model.data.uuid, lock=True
        )

        # Use if still needed  ----------------------------------
        if output_data is None:
            # If the apply step was simulated by cache, but the use step is
            # not fetchable, the internal model is not usable. We need to
            # create a usable Model resurrecting the internal transformer or
            # loading it from a previously dumped model.
            if isinstance(model, CachedApplyModel):
                print('It is possible that a previous apply() was successfully'
                      ' stored, but use() with current data wasn\'t.\n'
                      'E.g. you are trying to use in new data, or use() never '
                      'was stored before.\n')
                print('Recovering training data from model to reapply it.'
                      'The goal is to induce a model usable by use()...\n'
                      f'comp: {self.transformer.sid} '
                      f'data: {data.sid}'
                      f'training data: {model.data}')
                # stored_train_data = self.storage.fetch(train_uuid)
                model = self.transformer.apply(model.data)

            try:
                output_data = model.use(data, exit_on_error=False)
            except:
                self.storage.unlock(data, training_data_uuid=model.data.uuid)
                traceback.print_exc()
                exit(0)

            self.storage.store(output_data, self.fields,
                               training_data_uuid=model.data.uuid,
                               check_dup=False)
        return output_data

    def transformations(self, step, clean=True):
        """Cache produce no transformations by itself , so it needs to
        override the list of expected transformations."""
        return self.transformer.transformations(step, clean)
