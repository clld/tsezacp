import pathlib

from clld.web.assets import environment

import tsezacp


environment.append_path(
    str(pathlib.Path(tsezacp.__file__).parent.joinpath('static')), url='/tsezacp:static/')
environment.load_path = list(reversed(environment.load_path))
