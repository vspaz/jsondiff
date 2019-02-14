#!/usr/bin/env python3

import argparse
import re
import sys
from cmath import isclose
from itertools import zip_longest
from numbers import Number

import ujson


class ValidateNonEmpty(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ValidateNonEmpty, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        json_string = values.read()
        if not json_string:
            try:
                raise ValueError("file: {} is empty".format(values.name))
            except ValueError as e:
                print(('{}'.format(e)))
                sys.exit(1)
        else:
            setattr(namespace, self.dest, json_string)


class JsonDiff:
    def __init__(self):
        args = self.get_args()
        self.file1 = ujson.loads(args.file1)
        self.file2 = ujson.loads(args.file2)
        cfg = ujson.loads(args.config)

        self.default_tol = cfg['tolerance']['default']
        self.skip = {re.compile(i) for i in cfg['skipped']}
        self.required = {re.compile(i) for i in cfg['required']}
        self.tol_vals = {re.compile(k): v for k, v in cfg['tolerance']['fields'].items()}
        self.diff = {}

    def get_diff(self, one, two, diff, prefix=""):
        if isinstance(one, dict) and isinstance(two, dict):
            diff.update(
                **{k: one[k] for k in one.keys() - two.keys() if not self.is_skip(k, self.skip)},
                **{k: two[k] for k in two.keys() - one.keys() if not self.is_skip(k, self.skip)}
            )

            common_keys = one.keys() & two.keys()
            for k in common_keys:
                full_path = k if not prefix else ".".join([prefix, k])
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
                elif len({type(one[k]), type(two[k])}) == 2:
                    diff.update({k: [one[k], two[k]]})
                elif isinstance(one[k], str):
                    if one[k] != two[k]:
                        diff.update({k: [one[k], two[k]]})
                elif isinstance(one[k], dict):
                    self.get_diff(one[k], two[k], diff[k], full_path)
                elif isinstance(one[k], list):
                    self.get_diff(one[k], two[k], diff[k], full_path)
        elif isinstance(one, list) and isinstance(two, list):
            for indx, (elem1, elem2) in enumerate(zip_longest(one, two)):
                full_path = "[%s]" % indx if not prefix else "".join([prefix, "[%s]" % indx])
                if isinstance(elem1, Number) and isinstance(elem2, Number):
                    # apply specific tolerance to specific fields
                    if not isclose(elem1, elem2, rel_tol=self._get_tol(full_path)):
                        diff.update({indx: [elem1, elem2]})
                elif len({type(elem1), type(elem2)}) == 2:
                    diff.update({indx: [elem1, elem2]})
                elif isinstance(elem1, str):
                    if elem1 != elem2:
                        diff.update({indx: [elem1, elem2]})
                elif isinstance(elem1, dict):
                    diff[indx] = {}
                    self.get_diff(elem1, elem2, diff[indx], full_path)

    def print_diff(self):
        print(ujson.dumps(self.del_empty(self.diff), indent=4))

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
                v = JsonDiff.del_empty(v)
            if v != {}:
                filtered_data[k] = v
        return filtered_data

    @staticmethod
    def get_args():
        description = 'json comparison utility'

        argparser = argparse.ArgumentParser(description)
        argparser.add_argument(
            '-c', '--config', type=argparse.FileType('r'), dest='config',
            required=True, help='<config.json>',
            action=ValidateNonEmpty
        )

        argparser.add_argument(
            '-f1', '--file1', type=argparse.FileType('r'),
            dest='file1', required=True, help='<file1.json>',
            action=ValidateNonEmpty
        )
        argparser.add_argument(
            '-f2', '--file2', type=argparse.FileType('r'),
            dest='file2', required=True, help='<file2.json>',
            action=ValidateNonEmpty
        )
        args = argparser.parse_args()

        return args


def main():
    d = JsonDiff()
    d.get_diff(d.file1, d.file2, d.diff)
    d.print_diff()


if __name__ == "__main__":
    main()
