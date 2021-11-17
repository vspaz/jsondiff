# jsondiff
yet another json diff utility helpful for data analysis.

unlike many other json diff utility, you can
* leave out from comparison the fields that you are not interested in.
* define only required fields
* compare numeric values using a particular precision tolerance e.g. `1e-03`, which can be set globally or per field.
* use regex to define fields.

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