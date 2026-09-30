# Releasing the TsezACP clld app

```shell
git clone https://github.com/clld/tsezacp
cd tsezacp
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../tsezacp-cldf/cldf/TextCorpus-metadata.json
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO tsezacp > tsezacp.sql
zip tsezacp.sql.zip tsezacp.sql
rm tsezacp.sql
```

