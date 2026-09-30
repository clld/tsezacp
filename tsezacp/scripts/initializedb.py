import collections

from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common
from pyigt import IGT
from markdown import markdown

import tsezacp
from tsezacp import models


def main(args):
    data = Data()
    cldf = args.cldf

    dataset = common.Dataset(
        id=tsezacp.__name__,
        name=cldf.properties['dc:title'],
        description=markdown(cldf.properties['dc:description']),
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        contact='dlce.rdm@eva.mpg.de',
        domain='tsezacp.clld.org',
        license='http://creativecommons.org/licenses/by/4.0/',
        jsondata={
            'source_citation': cldf.properties['dc:bibliographicCitation'],
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)
    DBSession.add(common.Editor(
        dataset=dataset,
        contributor=common.Contributor(id='comrie', name='Bernard Comrie')))

    for o in cldf.objects('LanguageTable'):
        data.add(common.Language, o.id, id=o.id, name=o.cldf.name)

    for o in cldf.objects('ContributionTable'):
        data.add(
            models.Text, o.id,
            id=o.id,
            ord=int(o.id),
            name=o.cldf.name,
            description=o.cldf.description)

    for o in cldf.objects('ExampleTable'):
        full = o.related('exampleReference')
        if full:
            tid, _, lid = full.id.partition('-')
            l = data.add(
                models.Line, full.id,
                id=full.id,
                ord=full.cldf.position[0] * 1000 + full.cldf.position[1],
                language=data['Language']['dido1241'],
                text=data['Text'][full.cldf.contributionReference],
                name=full.cldf.primaryText,
                description=full.cldf.translatedText,
                analyzed='\t'.join(full.cldf.analyzedWord),
                gloss='\t'.join(full.cldf.gloss),
                russian=o.cldf.translatedText)

            igt = IGT(phrase=full.cldf.analyzedWord, gloss=full.cldf.gloss)
            for i, (gw, poss) in enumerate(zip(igt.glossed_words, full.data['Part_of_Speech']), start=1):
                if poss is None:
                    break

                w = data.add(
                    models.WordInLine, i,
                    id='{}-{}'.format(full.id, i),
                    ord=i,
                    name=gw.word_from_morphemes,
                    #description=wclear,
                    line=l)

                for j, (gm, pos) in enumerate(zip(gw.glossed_morphemes, poss.split('-')), start=1):
                    w.morphemes.append(models.MorphemeInWord(
                        id='{}-{}-{}'.format(full.id, i, j),
                        ord=j,
                        name=gm.morpheme,
                        description=gm.gloss,
                        pos=pos,
                        normpos=pos.replace('pl', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '')
                    ))

    senses = collections.defaultdict(set)
    for r in cldf.iter_rows('SenseTable', 'entryReference', 'description'):
        senses[r['entryReference']].add(r['description'])

    for o in cldf.objects('EntryTable'):
        data.add(
            models.Morpheme, o.id,
            id=o.id,
            name=o.cldf.headword,
            language=data['Language']['dido1241'],
            description='; '.join(sorted(senses[o.id])),
            pos=o.cldf.partOfSpeech)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for miw, m in DBSession.query(models.MorphemeInWord, models.Morpheme)\
            .filter(models.Morpheme.name == models.MorphemeInWord.name)\
            .filter(models.Morpheme.pos == models.MorphemeInWord.normpos):
        miw.morpheme = m
