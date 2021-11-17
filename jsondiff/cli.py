import argparse
import logging
import sys


class AssertFileNonEmpty(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        json_string = values.read()
        if not json_string:
            try:
                raise ValueError(f'file: {values.name} is empty')
            except ValueError as e:
                logging.error(e)
                sys.exit(1)
        setattr(namespace, self.dest, json_string)


class ValidateConfig(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        with open(values) as fh:
            json_string = fh.read()
        if not json_string:
            logging.warning('empty config given; ignoring')
            json_string = '{}'
        setattr(namespace, self.dest, json_string)


def get_args():
    description = 'json comparison utility'
    argparser = argparse.ArgumentParser(description)
    argparser.add_argument(
        '-c', '--config', type=str, dest='config',
        required=False, default='{}', help='<path/to/config.json>',
        action=ValidateConfig,
    )

    argparser.add_argument(
        '-f1', '--file1', type=argparse.FileType('r'),
        dest='file1', required=True, help='<path/to/file1.json>',
        action=AssertFileNonEmpty,
    )
    argparser.add_argument(
        '-f2', '--file2', type=argparse.FileType('r'),
        dest='file2', required=True, help='<path/to/file2.json>',
        action=AssertFileNonEmpty,
    )
    return argparser.parse_args()
