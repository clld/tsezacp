from clld.web.assets import environment
from path import path

import tsezacp


environment.append_path(
    path(tsezacp.__file__).dirname().joinpath('static'), url='/tsezacp:static/')
environment.load_path = list(reversed(environment.load_path))
