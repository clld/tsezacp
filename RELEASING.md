# Releasing the TsezACP clld app

```shell
git clone https://github.com/clld/tsezacp
git clone --branch v2.0.1 --depth 1 https://github.com/cldf-datasets/tsezacp tsezacp-cldf
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
pg_dump -xO --compress gzip:9 tsezacp > tsezacp.sql.gz
```

