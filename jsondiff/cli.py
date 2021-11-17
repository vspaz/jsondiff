import argparse
import logging
import sys


class ValidateNonEmpty(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ValidateNonEmpty, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        json_string = values.read()
        if not json_string:
            try:
                raise ValueError(f'file: {values.name} is empty')
            except ValueError as e:
                logging.error(e)
                sys.exit(1)
        else:
            setattr(namespace, self.dest, json_string)


def get_args():
    description = 'json comparison utility'

    argparser = argparse.ArgumentParser(description)
    argparser.add_argument(
        '-c', '--config', type=argparse.FileType('r'), dest='config',
        required=False, default='{}', help='<config.json>',
        action=ValidateNonEmpty,
    )

    argparser.add_argument(
        '-f1', '--file1', type=argparse.FileType('r'),
        dest='file1', required=True, help='<file1.json>',
        action=ValidateNonEmpty,
    )
    argparser.add_argument(
        '-f2', '--file2', type=argparse.FileType('r'),
        dest='file2', required=True, help='<file2.json>',
        action=ValidateNonEmpty,
    )
    return argparser.parse_args()
