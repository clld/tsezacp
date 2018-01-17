from clld.web.assets import environment
from clldutils.path import Path

import tsezacp


environment.append_path(
    str(Path(tsezacp.__file__).parent.joinpath('static')), url='/tsezacp:static/')
environment.load_path = list(reversed(environment.load_path))
