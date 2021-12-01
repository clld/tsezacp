import sys

from sqlalchemy import create_engine

from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common

import tsezacp
from tsezacp import models


def main(args):
    db = create_engine('sqlite:///' + args.data_file('sqlite3.db').resolve().as_posix())

    data = Data()

    dataset = common.Dataset(
        id=tsezacp.__name__,
        name="The Tsez Annotated Corpus Project",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        contact='forkel@shh.mpg.de',
        domain='tsezacp.clld.org',
        license='http://creativecommons.org/licenses/by/4.0/',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    #
    # TODO: add editors!
    #

    lang = data.add(common.Language, 'tsez', id='tsez', name='Tsez')

    for row in db.execute('select * from texts_data_text'):
        data.add(
            models.Text, row.id,
            id=str(row.Number),
            ord=row.Number,
            name=row.Title_in_Tsez,
            description=row.Title_in_English,
            russian=row.Title_in_Russian)

    for row in db.execute('select * from texts_data_line'):
        text = data['Text'][row.to_Text_id]
        data.add(
            models.Line, row.id,
            id='%s-%s' % (text.id, row.Line_Position),
            ord=row.Line_Position,
            language=lang,
            text=text,
            name=row.Tsez_Line,
            description=row.English_Translation,
            russian=row.Russian_Translation)

    for row in db.execute('select w.id, w.to_Line_id, w.Lex_Position, w.Word_in_Phrase, w.Word_Clear, m.id, m.Position, m.Value, m.Gloss, m.Part_of_Speech from texts_data_word as w, texts_data_morpheme as m where m.to_Word_id = w.id order by w.to_Line_id, w.Lex_Position, m.Position'):
        wid, lid, wpos, wname, wclear, mid, mpos, mname, mgloss, mpartofspeech = row
        if wid in data['WordInLine']:
            w = data['WordInLine'][wid]
        else:
            w = data.add(
                models.WordInLine, wid,
                id=str(wid),
                ord=wpos,
                name=wname,
                description=wclear,
                line=data['Line'][lid])

        w.morphemes.append(models.MorphemeInWord(
            id=str(mid),
            ord=mpos,
            name=mname,
            description=mgloss,
            normgloss=mgloss[1:] if mgloss.startswith('-') else mgloss,
            pos=mpartofspeech.replace('-', '').strip()))

    for lid in sorted(data['Line'].keys()):
        line = data['Line'][lid]
        #print line.name
        #print '  '.join(w.name for w in line.words)
        line.analyzed = '\t'.join('\t'.join(m.name for m in w.morphemes) for w in line.words)
        line.gloss = '\t'.join('\t'.join(m.description for m in w.morphemes) for w in line.words)

    for row in db.execute('select * from texts_data_glossary'):
        data.add(
            models.Morpheme, row.id,
            id=str(row.id),
            name=row.Value,
            language=lang,
            description=row.Gloss,
            notes=row.Notes,
            pos=row.Part_of_Speech.replace('-', '').strip())


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for miw, m in DBSession.query(models.MorphemeInWord, models.Morpheme)\
            .filter(models.Morpheme.name == models.MorphemeInWord.name)\
            .filter(models.Morpheme.description.ilike('%' + models.MorphemeInWord.normgloss + '%'))\
            .filter(models.Morpheme.pos.ilike('%' + models.MorphemeInWord.pos + '%')):
        miw.morpheme = m
