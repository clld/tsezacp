from clldutils.path import Path

from clld.tests.util import TestWithApp

import tsezacp


class Tests(TestWithApp):
    __cfg__ = Path(tsezacp.__file__).parent.joinpath('..', 'development.ini').resolve()

    def test_home(self):
        res = self.app.get('/', status=200)
