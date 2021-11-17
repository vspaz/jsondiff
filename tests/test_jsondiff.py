from jsondiff.difference import DictDiff

sample_config = {
    'required': [],
    'skipped': [],
    'tolerance': {
        'default': 1e-09,
        'fields': {
            'foo': 0.01,
        },
    },
}


def test_same_dict_ok():
    common_object = {'foo': 0.1, 'key_1': {'key_1': 'value_1'}}
    jd = DictDiff(config=sample_config)
    jd.find_diff(one=common_object, two=common_object, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}


def test_nested_objects_different_ok():
    object_1 = {'foo': 0.1, 'key_1': {'key_1': 'value_1'}}
    object_2 = {'foo': 0.1, 'key_1': {'key_2': 'value_2'}}
    jd = DictDiff(config=sample_config)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'key_1': {'key_1': 'value_1', 'key_2': 'value_2'}}


def test_fields_skip_ok():
    object_1 = {'foo': 10, 'key_1': {'key_1': 'value_1'}}
    object_2 = {'foo': 20, 'key_1': {'key_1': 'value_1'}}

    config_do_not_skip_fields = {'skipped': []}

    jd = DictDiff(config=config_do_not_skip_fields)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'foo': [10, 20]}

    config_skip_fields = {'skipped': ['foo']}

    jd = DictDiff(config=config_skip_fields)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}
