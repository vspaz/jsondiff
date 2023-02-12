import re
from cmath import isclose
from itertools import zip_longest
from numbers import Number


class DictDiff:

    default_config = dict(
        tolerance={"default": 1e-09, "fields": {}},
        skipped=[],
        required=[],
    )

    def __init__(self, config=None):
        config = config or self.default_config
        self.default_tol = config['tolerance']["default"]
        self.skip_fields = {re.compile(field) for field in config["skipped"]}
        self.required_fields = {re.compile(field) for field in config["required"]}
        self.field_to_tol = {re.compile(field): tol for field, tol in config["tolerance"]["fields"].items()}
        self.diff = {}

    def find_diff(self, one, two, diff, prefix=""):
        if isinstance(one, dict) and isinstance(two, dict):
            diff.update(
                **{k: one[k] for k in one.keys() - two.keys() if not is_skip(k, self.skip_fields)},
                **{k: two[k] for k in two.keys() - one.keys() if not is_skip(k, self.skip_fields)}
            )

            common_keys = one.keys() & two.keys()
            for k in common_keys:
                full_path = k if not prefix else f"{prefix}.{k}"
                # exclude keys from diff
                if is_skip(full_path, self.skip_fields):
                    continue
                # include required keys into diff, only
                if self.required_fields and not any(i for i in self.required_fields if re.search(i, full_path)):
                    continue
                diff[k] = {}
                if isinstance(one[k], Number) and isinstance(two[k], Number):
                    # apply specific tolerance to specific fields
                    if not isclose(one[k], two[k], rel_tol=self._get_tol(full_path)):
                        diff.update({k: [one[k], two[k]]})
                elif not isinstance(one[k], type(two[k])):
                    diff.update({k: [one[k], two[k]]})
                elif isinstance(one[k], str):
                    if one[k] != two[k]:
                        diff.update({k: [one[k], two[k]]})
                elif isinstance(one[k], dict):
                    self.find_diff(one[k], two[k], diff[k], full_path)
                elif isinstance(one[k], list):
                    self.find_diff(one[k], two[k], diff[k], full_path)
        elif isinstance(one, list) and isinstance(two, list):
            for idx, (elem_1, elem_2) in enumerate(zip_longest(one, two)):
                full_path = f"[{idx}]" if not prefix else f"{prefix}[{idx}]"
                if isinstance(elem_1, Number) and isinstance(elem_2, Number):
                    # apply specific tolerance to specific fields
                    if not isclose(elem_1, elem_2, rel_tol=self._get_tol(full_path)):
                        diff.update({idx: [elem_1, elem_2]})
                elif isinstance(elem_1, type(elem_2)):
                    diff.update({idx: [elem_1, elem_2]})
                elif isinstance(elem_1, str):
                    if elem_1 != elem_2:
                        diff.update({idx: [elem_1, elem_2]})
                elif isinstance(elem_1, dict):
                    diff[idx] = {}
                    self.find_diff(elem_1, elem_2, diff[idx], full_path)

    def get_diff(self):
        return del_empty(self.diff)

    def _get_tol(self, full_path):
        # get the most specific tolerance for a key e.g. foo.bar.baz
        tolerance_values_per_field = [self.field_to_tol[t] for t in self.field_to_tol if re.search(t, full_path)]
        if len(tolerance_values_per_field) > 0:
            return tolerance_values_per_field[-1]
        return self.default_tol


def is_skip(key, skipped_key_prefixes):
    return any(re.search(skipped_key_prefix, key) for skipped_key_prefix in skipped_key_prefixes)


def del_empty(nested_object):
    filtered_data = {}
    for k, v in nested_object.items():
        if isinstance(v, dict):
            v = del_empty(v)
        if v != {}:
            filtered_data[k] = v
    return filtered_data
