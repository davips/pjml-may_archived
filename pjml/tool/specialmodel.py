from abc import ABC
from functools import lru_cache

from pjdata.abc.abstractdata import AbstractData
from pjdata.collection import Collection
from pjdata.data import Data
from pjdata.mixin.identifyable import Identifyable
from pjml.tool.abc.mixin.exceptionhandler import ExceptionHandler
from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
from pjml.tool.abc.mixin.timers import Timers
from pjml.tool.model import Model


class FailedModel(Model):
    def __init__(self, transformer, data_before_apply, data_after_apply,
                 **kwargs):
        super().__init__(transformer, data_before_apply, data_after_apply,
                         **kwargs)

    def _use_impl(self, data, **kwargs):
        raise Exception(
            f"A {self.name} model from failed pipelines during apply is not "
            f"usable!"
        )


class EarlyEndedModel(Model):
    def __init__(self, transformer, data_before_apply, data_after_apply,
                 **kwargs):
        super().__init__(transformer, data_before_apply, data_after_apply,
                         **kwargs)

    def _use_impl(self, data, **kwargs):
        raise Exception(
            f"A {self.name} model from early ended pipelines during apply is "
            f"not usable!"
        )


class CachedApplyModel(Model):
    def __init__(self, transformer, data_before_apply, data_after_apply,
                 **kwargs):
        super().__init__(transformer, data_before_apply, data_after_apply,
                         **kwargs)

    def _use_impl(self, data, **kwargs):
        raise Exception(
            f"A {self.name} model from a succesfully cached apply is not "
            f"usable!"
        )
