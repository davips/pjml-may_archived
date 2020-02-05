import traceback

from pjdata.data import NoData

from cururu.storer import Storer
from pjdata.step.apply import Apply
from pjdata.step.use import Use
from pjml.config.cs.containercs import ContainerCS
from pjml.config.node import Node
from pjml.config.parameter import FixedP
from pjml.tool.base.singleton import NoModel
from pjml.tool.base.transformer import Transformer
from pjml.tool.abc.configurablecontainer1 import ConfigurableContainer1


class Cache(ConfigurableContainer1, Storer):
    def __new__(cls, *args, fields=None, engine="dump", settings=None,
                transformers=None):
        """Shortcut to create a ConfigSpace."""
        if transformers is None:
            transformers = args
        if all([isinstance(t, Transformer) for t in transformers]):
            instance = ConfigurableContainer1.__new__(Cache)
            instance.__init__(transformers=transformers)
            return instance
        node = Node(params={
            'fields': FixedP(fields),
            'engine': FixedP(engine),
            'settings': FixedP(settings)
        })
        return ContainerCS(Cache.name, Cache.path, transformers, node)

    def __init__(self, *args, fields=None, engine="dump", settings=None,
                 transformers=None):
        if transformers is None:
            transformers = args
        if fields is None:
            fields = ['X', 'Y', 'Z']
        if settings is None:
            settings = {}
        config = self._to_config(locals())
        del config['args']
        super().__init__(config)

        self.fields = fields
        self._set_storage(engine, settings)

    def _apply_impl(self, data):
        # TODO: CV() is too cheap to be recovered from storage, specially if
        #  it is a LOO. Maybe transformers could inform whether they are cheap.
        transformation = Apply(self.transformer)
        output_data = self.storage.fetch(
            data, transformation, self.fields,
            lock=True
        )
        # pra carregar modelo:
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
                output_data = self.transformer.apply(data, exit_on_error=False)
            except:
                self.storage.unlock(data, transformation)
                traceback.print_exc()
                exit(0)

            # TODO: Source -> DT = entra NoData, sai None...
            #   AttributeError: type object 'NoData' has no attribute 'phantom'
            data_to_store = data.phantom if output_data is None else output_data
            self.storage.store(
                data_to_store,
                data, transformation,
                self.fields,
                check_dup=False
            )

        self.model = NoModel if self.transformer.model is None \
            else self.transformer.model

        return output_data

    def _use_impl(self, data):
        # exit(0)
        transformation = Use(self.transformer, self._last_training_data)
        output_data = self.storage.fetch(
            data, transformation, self.fields,
            lock=True
        )

        # Use if still needed  ----------------------------------
        if output_data is None:
            # If the component was applied (probably simulated by storage),
            # but there is no model, we reapply it...
            if self.transformer.model is None:
                # Melhor deixar quebrar caso um
                # apply() seja armazenado e o use() correspondente não?
                # Ou guardar referência pro conjunto de treino para reinduzir?
                # Fazer dump do transformer resolve melhor, mas pode ser
                # custoso.
                # Usuário pode decidir, escolhendo um cache local para isso.
                print('It is possible that a previous apply() was successfully'
                      ' stored, but use() with current data wasn\'t.\n'
                      'E.g. you are trying to use in new data, or use() never '
                      'was stored before.\n')
                print('Recovering training data from transformer to reapply it.'
                      'The goal is to induce a model usable by use()...\n'
                      f'comp: {self.transformer.sid} '
                      f'data: {data.sid}'
                      f'training data: {self._last_training_data}')
                # stored_train_data = self.storage.fetch(train_uuid)
                self.transformer.apply(self._last_training_data)

            try:
                output_data = self.transformer.use(data, exit_on_error=False)
            except:
                self.storage.unlock(data, transformation)
                traceback.print_exc()
                exit(0)

            self.storage.store(
                output_data,
                data, transformation, self.fields,
                check_dup=False
            )

        return output_data

    def _transformations(self, step=None, training_data=None):
        """Cache produce no transformations by itself , so it needs to
        override the list of expected transformations."""
        if step is None:
            step = self._current_step
        if training_data is None:
            training_data = self._last_training_data
        return self.transformer._transformations(step, training_data)
