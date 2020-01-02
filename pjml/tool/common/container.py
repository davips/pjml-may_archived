from abc import ABC, abstractmethod

from pjml.tool.base.aux.decorator import classproperty
from pjml.tool.base.transformer import Transformer


class Container(Transformer, ABC):
    """This component is a generic component to build a 'Container'.
    The idea of the Container is to modify  'transformer(s)'.
    """

    def __init__(self, *t_or_ts, own_config=None):
        # TODO: propagar seed
        config = {self._parname: t_or_ts}
        if own_config is not None:
            config.update(**own_config)
        super().__init__(config, t_or_ts)

        self.transformer = t_or_ts[0]
        self.transformers = t_or_ts
        self.size = len(t_or_ts) if isinstance(t_or_ts, tuple) else 1

    @property
    @abstractmethod
    def _parname(self):
        pass

    @classmethod
    @classproperty
    def cs(cls):
        raise Exception(
            f'{cls.name} depends on {cls._parname} to build a CS. Use CS '
            f'shortcut for class {cls.name} instead of calling its .cs!'
        )

    @classmethod
    def _cs_impl(cls):
        raise Exception(f'Wrong calling of {cls.name}._cs_impl!')


class Container1(Container, ABC):
    _parname = 'transformer'

    def __init__(self, transformer, own_config=None):
        super().__init__(transformer, own_config=own_config)


class ContainerN(Container, ABC):
    _parname = 'transformers'

    def __init__(self, *args, own_config=None, transformers=None):
        if transformers is None:
            transformers = args
        super().__init__(*transformers, own_config=own_config)
