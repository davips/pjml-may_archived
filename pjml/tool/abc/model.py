from abc import ABC, abstractmethod
from functools import lru_cache

from pjdata.data import NoData

from pjml.tool.abc.mixin.exceptionhandler import BadComponent
from pjml.tool.abc.mixin.runnable import Runnable


class Model(Runnable):
    @abstractmethod
    def _use_impl(self, data):
        """Each component should implement its core 'use' functionality."""

    @abstractmethod
    def _data_impl(self):
        """Each component should return the resulting 'data', if any."""

    @property
    @lru_cache()
    def data(self):
        return self._data_impl()

    def use(self, data=NoData, exit_on_error=True, own_data=False):
        """Testing step (usually).

        Predict/transform/do nothing/evaluate/... Data.

        Parameters
        ----------
        data_use
        exit_on_error

        Returns
        -------
        transformed data, normally
        None, when data is None
            (probably meaning the pipeline finished before this transformer)
        same data, but annotated with a failure

        Exception
        ---------
        BadComponent
            Data object resulting history should be consistent with
            _transformations() implementation.
        """
        data_use = self.data if own_data else data
        if data_use is None:  # or self.model is NoModel:
            return None

        from pjml.tool.abc.nodatahandler import NoDataHandler
        if data_use is NoData and not isinstance(self, NoDataHandler):
            raise Exception(f'NoData is not accepted by {self.name}!')

        return self._run(self._use_impl, data_use, exit_on_error=exit_on_error)

    def transformations(self, step=None, training_data=None):
        """Ongoing transformation described as a list of Transformation
        objects.

        Child classes should override this method to perform non-atomic or
        non-trivial transformations.
        A missing implementation will be detected during apply/use."""
        # if step is None:
        #     step = self._current_step
        # if training_data is None:
        #     training_data = self._last_training_data
        # if step == 'a':
        #     return [Apply(self)]
        # elif step == 'u':
        #     return [Use(self, training_data)]
        # else:
        #     raise BadComponent('Wrong current step:', step)
        return None