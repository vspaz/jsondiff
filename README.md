# jsondiff
yet another jsondiff utility helpful for data analysis.

unlike other json diff utilities:

* it's possible to **skip the fields** that you are not interesting for analysis.
* one can choose only required fields
* the jsondiff utility compares numeric values using relative or absolute **precision tolerance** e.g. `1e-03` or `0.001`, which can be set globally or per field.
* it's possible to use field **prefixes** or **regexes** to filter out fields.
* there's an **optional** config (see below) when dealing with a large number of fields.
* jsondiff requires no 3d party modules.

### install

```shell
git clone git@github.com:vspaz/jsondiff.git
cd jsondiff
python3 setup.py install
```

### config (optional)

```json
{
  "required": [],
  "skipped": [
    "barbaz"
  ],
  "tolerance": {
    "default": 1e-09,
    "fields": {
      "foo": 0.01,
      "baz": 0.1
    }
  }
}
```

```shell
jsondiff -f1 tests/data/file_1.json -f2 tests/data/file_2.json -c tests/data/config.json  # -> {}, as field "barbaz" is skipped in the config.
```

or
```shell
jsondiff -f1 tests/data/file_1.json -f2 tests/data/file_2.json  #  -> {'baz': {'barbaz': [90, 80]}}  # no fields are skipped
```

### run tests
```shell
git clone git@github.com:vspaz/jsondiff.git
cd jsondiff
pip install -r requirements/dev.txt
make test

```
