from pathlib import Path

# Include all classes when 'from <this module> import *' is called.
fs = [str(f) for f in Path('pjml').rglob('*.py')
      if not f.name.startswith('_')
      if not f.name.startswith('reduce')
      if not str(f).startswith('base')]

for f in [f.replace('/', '.')[:-3] for f in fs]:
    statement = f'from {f} import *'
    exec(statement)
