from functools import partial

from sqlalchemy.orm import joinedload_all

from clld.web.app import get_configurator, CtxFactoryQuery, menu_item
from clld.db.models.common import Contribution, Unit
from clld.interfaces import ICtxFactoryQuery

# we must make sure custom models are known at database initialization!
from tsezacp import models


_ = lambda s: s
_('Contributions')
_('Contribution')
_('Units')
_('Unit')
_('Sentence')
_('Sentences')


class AcpCtxFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        """Derived classes may override this method to add model-specific query
        refinements of their own.
        """
        if model == Unit:
            return query.options(joinedload_all(
                models.Morpheme.occurrences, models.MorphemeInWord.word, models.WordInLine.line, models.Line.text))
        if model == Contribution:
            return query.options(joinedload_all(
                models.Text.lines, models.Line.words, models.WordInLine.morphemes, models.MorphemeInWord.morpheme))
        return query


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('tsezacp', (AcpCtxFactoryQuery(), ICtxFactoryQuery), settings=settings)
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('contributions', partial(menu_item, 'contributions')),
        ('units', partial(menu_item, 'units')),
        #('examples', partial(menu_item, 'sentences')),
    )
    config.include('clldmpg')
    config.include('tsezacp.datatables')
    config.include('tsezacp.adapters')
    return config.make_wsgi_app()
