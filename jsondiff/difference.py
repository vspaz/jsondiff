import re
from cmath import isclose
from itertools import zip_longest
from numbers import Number


class DictDiff:
    def __init__(self, config=None):
        config = config or {}
        tolerance = config.get('tolerance', {})
        self.default_tol = tolerance.get('default', 1e-09)
        self.skip = {re.compile(i) for i in config.get('skipped', [])}
        self.required = {re.compile(i) for i in config.get('required', [])}
        self.tol_vals = {re.compile(k): v for k, v in tolerance.get('fields', {}).items()}
        self.diff = {}

    def find_diff(self, one, two, diff, prefix=''):
        if isinstance(one, dict) and isinstance(two, dict):
            diff.update(
                **{k: one[k] for k in one.keys() - two.keys() if not self.is_skip(k, self.skip)},
                **{k: two[k] for k in two.keys() - one.keys() if not self.is_skip(k, self.skip)}
            )

            common_keys = one.keys() & two.keys()
            for k in common_keys:
                full_path = k if not prefix else f'{prefix}.{k}'
                # exclude keys from diff
                if self.is_skip(full_path, self.skip):
                    continue
                # include required keys into diff, only
                if self.required and not any(i for i in self.required if re.search(i, full_path)):
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
                elif len({type(elem_1), type(elem_2)}) == 2:
                    diff.update({idx: [elem_1, elem_2]})
                elif isinstance(elem_1, str):
                    if elem_1 != elem_2:
                        diff.update({idx: [elem_1, elem_2]})
                elif isinstance(elem_1, dict):
                    diff[idx] = {}
                    self.find_diff(elem_1, elem_2, diff[idx], full_path)

    def get_diff(self):
        return self.del_empty(self.diff)

    def _get_tol(self, full_path):
        try:
            # get the last tolerance which is most specific to a particular key
            return [self.tol_vals[t] for t in self.tol_vals if re.search(t, full_path)][-1]
        except IndexError:
            return self.default_tol

    @staticmethod
    def is_skip(where, skip):
        return any(re.search(p, where) for p in skip)

    @staticmethod
    def del_empty(nested_dict):
        filtered_data = {}
        for k, v in nested_dict.items():
            if isinstance(v, dict):
                v = DictDiff.del_empty(v)
            if v != {}:
                filtered_data[k] = v
        return filtered_data
