from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, IntegerIdCol

from tsezacp import models


class Texts(datatables.Contributions):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', sTitle='Number'),
            LinkCol(self, 'name', sTitle='Title'),
            Col(self, 'description', sTitle='English translation'),
            Col(self, 'russian', sTitle='Russian translation', model_col=models.Text.russian),
        ]


class Glossary(datatables.Units):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Value'),
            Col(self, 'description', sTitle='Gloss'),
            Col(self, 'pos', sTitle='Part of speech', model_col=models.Morpheme.pos)
        ]


class Lines(datatables.Sentences):
    def col_defs(self):
        res = datatables.Sentences.col_defs(self)
        return res[:-3] + res[-1:]


def includeme(config):
    config.register_datatable('contributions', Texts)
    config.register_datatable('sentences', Lines)
    config.register_datatable('units', Glossary)
