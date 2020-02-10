import json


class Printer(dict):
    _pretty_printing = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enable_pretty_printing(self):
        self._pretty_printing = True

    def disable_pretty_printing(self):
        self._pretty_printing = True

    def __str__(self, depth=''):
        if not self._pretty_printing:
            return super().__str__()

        js = json.dumps(self, sort_keys=True, indent=4)
        return js.replace('\n', '\n' + depth)
