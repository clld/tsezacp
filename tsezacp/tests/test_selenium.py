from clld.tests.util import TestWithSelenium

import tsezacp


class Tests(TestWithSelenium):
    app = tsezacp.main({}, **{'sqlalchemy.url': 'postgres://robert@/tsezacp'})
