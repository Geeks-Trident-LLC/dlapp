"""Module containing the logic for the dlquery entry-points."""

import sys
import argparse


class Application:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='dlquery',
            usage='%(prog)s [options]',
            description='%(prog)s application.',
        )

        parser.add_argument(
            '-f', '--filename', type=str,
            default='',
            help='A JSON or YAML file name.'
        )

        parser.add_argument(
            '--filetype', type=str, choices=['json', 'yaml', 'yml', 'csv'],
            default='',
            help='A file type can be either JSON, YAML, or CSV.'
        )

        parser.add_argument(
            '--find', type=str,
            default='',
            help='Querying dictionary or list using wildcard pattern.'
        )

        parser.add_argument(
            '--select', type=str,
            default='',
            help='A SELECT statement.'
        )

        parser.add_argument(
            '--to-csv', type=str, dest='to_csv',
            default='',
            help='Searching a dlquery using wildcard pattern.'
        )

        parser.add_argument(
            '--tabular', action='store_true',
            help='Displaying result in tabular format.'
        )

        parser.add_argument(
            '--summary', type=str,
            default='',
            help='Displaying result in tabular format.'
        )

        self.parser = parser

    def is_valid_file(self, filename, filetype):
        pass

    def run(self):
        args = self.parser.parse_args()
        chk = any(bool(i) for i in vars(args).values())
        if not chk:
            self.parser.print_help()
            sys.exit(1)

        if not args.filename:
            print('*** --filename CAN NOT be empty.')
            sys.exit(1)


def execute():
    """Execute dlquery application."""
    app = Application()
    app.run()