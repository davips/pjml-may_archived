from ._version import __version__  # noqa: ignore
from pathlib import Path

# Include all classes when 'from pjml import *' is called.
fs = [f for f in Path('pjml').rglob('*.py') if not f.name.startswith('_')]

for f in [str(f).replace('/', '.')[:-3] for f in fs]:
    statement = f'from {f} import *'
    exec(statement)
