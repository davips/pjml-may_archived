import numpy as np
from pjml.config.description.cs.emptycs import EmptyCS
from pjml.tool.model import Model
from pjml.tool.abc.transformer import Transformer
from pjml.tool.abc.invisible import Invisible
from pjml.util import flatten

import re


class Report(Invisible):
    """Report printer.

    $r prints 'r'
    {dataset.name} prints the dataset name
    {dataset.failure} prints the failure
    """

    def __init__(self, text='Default report r=$R'):
        Transformer.__init__(self, {'text': text}, deterministic=True)
        self.text = text

    def _apply_impl(self, data):
        if data is not None:
            print('[apply] ', self._interpolate(self.text, data))

        def use_impl(data_use):
            print('[use] ', self._interpolate(self.text, data_use))
            return data_use

        return Model(data, use_impl, self)

    @classmethod
    def _interpolate(cls, text, data):
        def f(obj_match):
            M = data.field(obj_match.group(1), cls)
            return str(np.round(M, decimals=4))

        p = re.compile(r'\$([a-zA-Z]+)')
        return cls._eval(p.sub(f, text), data)

    @classmethod
    def _eval(cls, text, data):
        txt = ''
        run = False
        expanded = [w.split('}') for w in ('_' + text + '_').split('{')]
        for seg in flatten(expanded):
            if run:
                try:
                    txt += str(eval('data.' + seg))
                except Exception as e:
                    print(
                        f'Problems parsing\n  {text}\nwith data\n  {data}\n'
                        f'{data.history}\n!')
                    raise e
            else:
                txt += seg
            run = not run
        return txt[1:][:-1]

    @classmethod
    def _cs_impl(cls):
        return EmptyCS()
