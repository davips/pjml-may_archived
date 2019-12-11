from pjml.base.component import Component
from pjml.config.configspace import ConfigSpace
from pjml.config.distributions import choice
from pjml.config.parameters import CatP


class Report(Component):
    """Report printer.

    $r prints 'r'
    {dataset.name} prints the dataset name
    {dataset.failure} prints the failure
    """

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

    @classmethod
    def _interpolate(cls, text, data):
        segments = text.split('$')
        start = segments[0]
        rest = [str(data.fields[seg[0]]) + seg[1:] for seg in segments[1:]]
        return cls._eval(start + ''.join(rest), data)

    @classmethod
    def _eval(cls, text, data):
        txt = ''
        run = False
        expanded=[w.split('}') for w in ('_' + text + '_').split('{')]
        for seg in cls._flatten(expanded):
            if run:
                txt += str(eval('data.' + seg))
            else:
                txt += seg
            run = not run
        return txt[1:][:-1]

    @classmethod
    def _flatten(cls, lst):
        return [item for sublist in lst for item in sublist]
