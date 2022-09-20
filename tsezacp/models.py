from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declared_attr

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin, DBSession
from clld.db.models.common import Sentence, Contribution, Unit, IdNameDescriptionMixin


@implementer(interfaces.IContribution)
class Text(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    ord = Column(Integer, nullable=False)


@implementer(interfaces.ISentence)
class Line(CustomModelMixin, Sentence):
    pk = Column(Integer, ForeignKey('sentence.pk'), primary_key=True)
    ord = Column(Integer, nullable=False)
    text_pk = Column(Integer, ForeignKey('text.pk'))
    russian = Column(Unicode)

    @declared_attr
    def text(cls):
        return relationship(Text, backref=backref('lines', order_by=cls.ord))


class WordInLine(Base, IdNameDescriptionMixin):
    line_pk = Column(Integer, ForeignKey('line.pk'))
    ord = Column(Integer, nullable=False)

    @declared_attr
    def line(cls):
        return relationship(Line, backref=backref('words', order_by=cls.ord))


@implementer(interfaces.IUnit)
class Morpheme(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)
    pos = Column(Unicode)

    def lines(self):
        res = sorted(set(miw.word.line for miw in self.occurrences), key=lambda l: l.ord)
        total = len(res)
        res = res[:200]
        DBSession.query(Line)\
            .filter(Line.pk.in_([l.pk for l in res]))\
            .options(joinedload(Line.words).joinedload(WordInLine.morphemes).joinedload(MorphemeInWord.morpheme))\
            .all()
        return total, res


class MorphemeInWord(Base, IdNameDescriptionMixin):
    word_pk = Column(Integer, ForeignKey('wordinline.pk'))
    ord = Column(Integer, nullable=False)
    pos = Column(Unicode)
    normpos = Column(Unicode)
    morpheme_pk = Column(Integer, ForeignKey('morpheme.pk'))
    morpheme = relationship(Morpheme, backref='occurrences')

    @declared_attr
    def word(cls):
        return relationship(WordInLine, backref=backref('morphemes', order_by=cls.ord))
