from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Sentence, Contribution, Unit, IdNameDescriptionMixin


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
"""
CREATE TABLE "texts_data_dictionary_entry" (
    "id" integer NOT NULL PRIMARY KEY,
    "Number" integer NOT NULL,
    "Value" varchar(50) NOT NULL,
    "Part_of_Speech" varchar(50) NOT NULL,
    "Gloss" varchar(50) NOT NULL,
    "Notes" text NOT NULL,
    "Changed" date NOT NULL
);
CREATE TABLE "texts_data_glossary" (
    "id" integer NOT NULL PRIMARY KEY,
    "Number" integer NOT NULL,
    "Value" varchar(50) NOT NULL,
    "Part_of_Speech" varchar(50) NOT NULL,
    "Gloss" varchar(50) NOT NULL,
    "Notes" text NOT NULL,
    "Changed" date NOT NULL
);
CREATE TABLE "texts_data_line" (
    "id" integer NOT NULL PRIMARY KEY,
    "to_Text_id" integer NOT NULL REFERENCES "texts_data_text" ("id"),
    "Line_Position" integer NOT NULL,
    "Tsez_Line" varchar(400) NOT NULL,
    "English_Translation" varchar(400) NOT NULL,
    "Russian_Translation" varchar(400) NOT NULL
);
CREATE TABLE "texts_data_morpheme" (
    "id" integer NOT NULL PRIMARY KEY,
    "to_Word_id" integer NOT NULL REFERENCES "texts_data_word" ("id"),
    "Position" integer NOT NULL,
    "Value" varchar(10) NOT NULL,
    "Gloss" varchar(10) NOT NULL,
    "Part_of_Speech" varchar(10) NOT NULL
);
CREATE TABLE "texts_data_text" (
    "id" integer NOT NULL PRIMARY KEY,
    "Number" integer NOT NULL,
    "Title_in_Tsez" varchar(200) NOT NULL,
    "Title_in_English" varchar(200) NOT NULL,
    "Title_in_Russian" varchar(200) NOT NULL
);
CREATE TABLE "texts_data_word" (
    "id" integer NOT NULL PRIMARY KEY,
    "to_Line_id" integer NOT NULL REFERENCES "texts_data_line" ("id"),
    "Lex_Position" integer NOT NULL,
    "Word_in_Phrase" varchar(20) NOT NULL,
    "Word_Clear" varchar(15) NOT NULL
);
"""


@implementer(interfaces.IContribution)
class Text(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    ord = Column(Integer, nullable=False)
    russian = Column(Unicode)


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
    notes = Column(Unicode)


class MorphemeInWord(Base, IdNameDescriptionMixin):
    word_pk = Column(Integer, ForeignKey('wordinline.pk'))
    ord = Column(Integer, nullable=False)
    pos = Column(Unicode)
    normgloss = Column(Unicode)
    morpheme_pk = Column(Integer, ForeignKey('morpheme.pk'))
    morpheme = relationship(Morpheme, backref='occurrences')

    @declared_attr
    def word(cls):
        return relationship(WordInLine, backref=backref('morphemes', order_by=cls.ord))
