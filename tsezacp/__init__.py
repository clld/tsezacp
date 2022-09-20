from functools import partial

from sqlalchemy.orm import joinedload
from pyramid.config import Configurator

from clld.web.app import CtxFactoryQuery, menu_item
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
            return query.options(joinedload(
                models.Morpheme.occurrences).joinedload(
                models.MorphemeInWord.word).joinedload(
                models.WordInLine.line).joinedload(
                models.Line.text))
        if model == Contribution:
            return query.options(joinedload(
                models.Text.lines).joinedload(
                models.Line.words).joinedload(
                models.WordInLine.morphemes).joinedload(models.MorphemeInWord.morpheme))
        return query


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(AcpCtxFactoryQuery(), ICtxFactoryQuery)
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('contributions', partial(menu_item, 'contributions')),
        ('examples', partial(menu_item, 'sentences')),
        ('units', partial(menu_item, 'units')),
    )
    return config.make_wsgi_app()
