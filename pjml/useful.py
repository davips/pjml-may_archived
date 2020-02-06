from pathlib import Path

paths = list(Path('pjml/tool').rglob('*.py')) + \
        list(Path('pjml/config/operator').rglob('*.py'))
fs = [str(f) for f in paths
      if not f.name.startswith('_')
      if not f.name.startswith('reduce')
      if '/abc/' not in str(f)]

for f in [f.replace('/', '.')[:-3] for f in fs]:
    statement = f'from {f} import *'
    print(statement)
    exec(statement)

things = 'All tools and operators imported (and corresponding pollutant ' \
         'namespaces as well)!'
