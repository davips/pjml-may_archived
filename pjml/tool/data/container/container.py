# -*- coding: utf-8 -*-
""" Container module

For more information about the Container concept see [1].

.. _paje_arch Paje Architecture:
    TODO: put the link here
"""
from abc import ABC

from pjml.tool.base.component import Component


class Container(Component, ABC):
    """This component is a generic component to build a 'Container'.
    The idea of the Container is to modify a 'Component'.
    """

    def __init__(self, component):  # , seed):
        # TODO: pass seed to component, before Component changes it to randomsta
        # if not component.isdeterministic:

        super().__init__({'component': component}, component, False)
        self.model = self.algorithm

    def _apply_impl(self, data):
        return self.model.apply(data)

    def _use_impl(self, data):
        return self.model.use(data)

    @classmethod
    def cs(cls, component, **kwargs):
        """Config Space of this container. See Component.cs() for details.

        Parameters
        ----------
        component
            A container requires the config space of a component.
            'component' can be:
                * a Component object, which will be converted to a config
                space, implying that |ConfigSpace| = 1;
                * a ConfigSpace;
                * a Transformer, which will be converted to a config
                space, implying that |ConfigSpace| = 1;

        kwargs
            See Component.cs() for details.

        Returns
        -------
            Tree representing all remaining parameter spaces.
        """
        named_frozen_cs = super().cs(**kwargs)

        if named_frozen_cs.nested is not None:
            raise Exception('Container child classes cannot have nested CSs.'
                            'The parent creates the nested component.')
        return named_frozen_cs.updated(nested=component.cs)
