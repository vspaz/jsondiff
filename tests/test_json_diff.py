from jsondiff.difference import JsonDiff

sample_config = {
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
    common_object = {"foo": "bar", "key_1": {"key_1": "value_1"}}
    jd = JsonDiff(config=sample_config)
    jd.find_diff(one=common_object, two=common_object, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}


def test_nested_objects_different_ok():
    object_1 = {"foo": "bar", "key_1": {"key_1": "value_1"}}
    object_2 = {"foo": "bar", "key_1": {"key_2": "value_2"}}
    jd = JsonDiff(config=sample_config)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'key_1': {'key_1': 'value_1', 'key_2': 'value_2'}}
