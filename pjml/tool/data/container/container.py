# -*- coding: utf-8 -*-
""" Container module

For more information about the Container concept see [1].

.. _paje_arch Paje Architecture:
    TODO: put the link here
"""
from abc import ABC

from pjml.config.cs.supercs import SuperCS
from pjml.tool.base.transformer import Transformer


class Container(Transformer, ABC):
    """This component is a generic component to build a 'Container'.
    The idea of the Container is to modify a 'transformer'.
    """

    def __init__(self, transformer):  # , seed):
        # TODO: pass seed to transformer, before Transformer changes it to
        #  randomstate
        # if not transformer.isdeterministic:

        super().__init__({'transformer': transformer}, transformer, False)
        self.model = self.algorithm

    def _apply_impl(self, data):
        return self.model.apply(data)

    def _use_impl(self, data):
        return self.model.use(data)

    @classmethod
    def cs(cls, component, **kwargs):
        """Config Space of this container. See Component.cs() for details.

        Child classes should implement _cs_impl returning a Node.

        Parameters
        ----------
        component
            A container requires the config space of a component.
            'component' can be:
                * a Transformer object, which will be converted to a config
                space, implying that |ConfigSpace| = 1;
                * a ConfigSpace;
                * a component aka Transformer class, which will be converted
                to a config space, implying that |ConfigSpace| = 1;

        kwargs
            See Transformer.cs() for details.

        Returns
        -------
            Tree representing all remaining parameter spaces.
        """
        from pjml.config.util import freeze
        node = freeze(cls._cs_impl(), **kwargs)
        return SuperCS(cls.name, cls.path, component.cs, nodes=[node])
