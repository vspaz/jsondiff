# jsondiff
yet another jsondiff utility helpful for data analysis.
It doesn't require any 3d-party dependencies

unlike other json diff utilities, you can:
* **skip the fields** that you are not interested in.
* choose only required fields
* compare numeric values using relative or absolute **precision tolerance** e.g. `1e-03` or `0.001`, which can be set globally or per field.
* use field **prefixes** or **regexes** to filter out fields.
* use an optional config (see below) when dealing with a large number of fields.


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
