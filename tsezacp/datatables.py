from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, IntegerIdCol

from tsezacp import models


class Texts(datatables.Contributions):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', sTitle='Number'),
            LinkCol(self, 'name', sTitle='Title'),
            Col(self, 'description', sTitle='English translation'),
        ]


class Glossary(datatables.Units):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Morpheme'),
            Col(self, 'pos', sTitle='Part of speech', model_col=models.Morpheme.pos),
            Col(self, 'description', sTitle='Glosses'),
        ]


class Lines(datatables.Sentences):
    def col_defs(self):
        res = datatables.Sentences.col_defs(self)
        return res[:-3] + res[-1:]


def includeme(config):
    config.register_datatable('contributions', Texts)
    config.register_datatable('sentences', Lines)
    config.register_datatable('units', Glossary)
