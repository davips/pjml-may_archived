import traceback

from cururu.storer import Storer
from pjml.config.description.cs.containercs import ContainerCS
from pjml.config.description.node import Node
from pjml.config.description.parameter import FixedP
from pjml.tool.abc.container1 import Container1
from pjml.tool.abc.transformer import Transformer
from pjml.tool.containermodel import ContainerModel
from pjml.tool.model import Model


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
        return ContainerCS(Cache.name, Cache.path, transformers, node)

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

        # pra carregar modelo [outdated!!]:
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
            except:
                print('unlocking due to exception...')
                self.storage.unlock(data)
                traceback.print_exc()
                exit(0)

            # TODO: Source -> DT = entra NoData, sai None...
            #   AttributeError: type object 'NoData' has no attribute 'hollow'
            data_to_store = data.hollow if output_data is None else output_data
            self.storage.store(data_to_store, self.fields, check_dup=False)
        else:
            # model não usável
            model = Model(self.transformer, data, output_data,
                          use_impl=self._use_for_cached_apply)
        print('===========\n', model._use_impl)

        m = ContainerModel(self.transformer, data, model.data, [model])
        print('===========\n', m._use_impl)
        return m

    def _use_impl(self, data, model=None):
        exit()
        transformations = self.transformer.transformations('u')
        hollow = data.hollow_extended(transformations=transformations)
        output_data = self.storage.fetch(
            hollow, self.fields, training_data_uuid=model.data.uuid, lock=True
        )

        # Use if still needed  ----------------------------------
        if output_data is None:
            # If the apply step was simulated by cache, but the use step is
            # not fetcheable, the internal model is not usable. We need to
            # create a usable Model resurrecting the internal transformer or
            # loading it from a previously dumped model.
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

    def transformations(self, step, clean=True):
        """Cache produce no transformations by itself , so it needs to
        override the list of expected transformations."""
        return self.transformer.transformations(step, clean)
