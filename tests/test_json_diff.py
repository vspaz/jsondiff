from jsondiff.difference import JsonDiff

confg = {
  "required": [],
  "skipped": ["dummy"],
  "tolerance": {
    "default": 1e-09,
    "fields": {
      "coeffs.impressions": 0.01
    }
  }
}


def test_same_dict_ok():
    common_object = {"foo": "bar"}
    jd = JsonDiff(object_1=common_object, object_2=common_object, config=confg)
    jd.find_diff(jd.file1, jd.file2, jd.diff)
    difference = jd.get_diff()
    assert difference == {}
