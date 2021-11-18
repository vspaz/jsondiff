from jsondiff.difference import DictDiff


def test_same_dict_ok():
    common_object = {'foo': 0.1, 'key_1': {'key_1': 'value_1'}}
    jd = DictDiff()
    jd.find_diff(one=common_object, two=common_object, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}


def test_nested_objects_different_ok():
    object_1 = {'foo': 0.1, 'key_1': {'key_1': 'value_1'}}
    object_2 = {'foo': 0.1, 'key_1': {'key_2': 'value_2'}}
    test_config = {
        'required': [],
        'skipped': [],
        'tolerance': {
            'default': 1e-09,
            'fields': {
                'foo': 0.01,
            },
        },
    }
    jd = DictDiff(config=test_config)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'key_1': {'key_1': 'value_1', 'key_2': 'value_2'}}


def test_fields_skip_ok():
    object_1 = {'foo': 10, 'key_1': {'key_1': 'value_1'}}
    object_2 = {'foo': 20, 'key_1': {'key_1': 'value_1'}}

    jd = DictDiff(config={'skipped': []})
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'foo': [10, 20]}

    jd = DictDiff(config={'skipped': ['foo']})
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}


def test_default_relative_tolerance():
    object_1 = {'foo': 10.0001}
    object_2 = {'foo': 10.001}

    jd = DictDiff(config={'tolerance': {'default': 1e-04}})
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}

    jd = DictDiff(config={'tolerance': {'default': 1e-05}})
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {'foo': [10.0001, 10.001]}


def test_relative_tolerance_per_field():
    object_1 = {'foo': 100}
    object_2 = {'foo': 90}
    config = {
        'tolerance': {
            'fields': {
                'foo': 0.1
            },
        },
    }
    jd = DictDiff(config=config)
    jd.find_diff(one=object_1, two=object_2, diff=jd.diff)
    difference = jd.get_diff()
    assert difference == {}
