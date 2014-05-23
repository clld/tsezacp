from sqlalchemy.orm import joinedload, joinedload_all
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Integer

from clld.web import datatables
from clld.web.datatables.base import (
    Col, filter_number, LinkCol, DetailsRowLinkCol, IdCol, IntegerIdCol
)
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import linked_contributors, linked_references, link
from clld.web.util.htmllib import HTML

from tsezacp import models


class Texts(datatables.Contributions):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', sTitle='Number'),
            LinkCol(self, 'name', sTitle='Title'),
            Col(self, 'description', sTitle='English translation'),
            Col(self, 'russian', sTitle='Russian translation'),
        ]


class Glossary(datatables.Units):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Value'),
            Col(self, 'description', sTitle='Gloss'),
            Col(self, 'pos', sTitle='Part of speech', model_col=models.Morpheme.pos)
        ]


def includeme(config):
    config.register_datatable('contributions', Texts)
    config.register_datatable('units', Glossary)
