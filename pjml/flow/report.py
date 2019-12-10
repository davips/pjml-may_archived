from base.component import Component
from pjml.searchspace.configspace import ConfigSpace
from pjml.searchspace.distributions import choice
from pjml.searchspace.parameters import CatP


class Report(Component):
    """Report printer."""

    def __init__(self, text):
        self.config = locals()
        self.isdeterministic = True
        self.algorithm = text

    def _apply_impl(self, data):
        self.model = self.algorithm
        print('[apply] ', self._interpolate(self.model, data))
        return data

    def _use_impl(self, data):
        print('[use] ', self._interpolate(self.model, data))
        return data

    @classmethod
    def _cs_impl(cls):
        params = {
            'text': CatP(choice, items=['Random report X=$X',
                                        'Random report y=$y',
                                        'Random report z=$z',
                                        'Random report r=$r',
                                        'Random report s=$s'])
        }
        return ConfigSpace(params=params)

    @staticmethod
    def _interpolate(text, data):
        segments = text.split('$')
        start = segments[0]
        rest = [str(data.fields[seg[0]]) + seg[1:] for seg in segments[1:]]
        return start + ''.join(rest)
