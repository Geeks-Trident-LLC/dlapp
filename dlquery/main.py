"""Module containing the logic for the dlquery entry-points."""

import sys
import argparse


def show_tutorial_dlquery():
    msg = 'TODO: need to implement a tutorial for dlquery'
    raise NotImplementedError(msg)


def show_tutorial_csv():
    msg = 'TODO: need to implement a tutorial for dlquery-csv'
    raise NotImplementedError(msg)


def show_tutorial_json():
    msg = 'TODO: need to implement a tutorial for dlquery-json'
    raise NotImplementedError(msg)


def show_tutorial_yaml():
    msg = 'TODO: need to implement a tutorial for dlquery-yaml'
    raise NotImplementedError(msg)


class Cli:
    def __init__(self):
        self.filename = ''
        self.filetype = ''

        parser = argparse.ArgumentParser(
            prog='dlquery',
            usage='%(prog)s [options]',
            description='%(prog)s application',
        )

        parser.add_argument(
            '--app', action='store_true', dest='app',
            help='launch a dlquery GUI application'
        )

        parser.add_argument(
            '--filename', type=str,
            default='',
            help='a json, yaml, or csv file name'
        )

        parser.add_argument(
            '--filetype', type=str, choices=['json', 'yaml', 'yml', 'csv'],
            default='',
            help='a file type can be either json, yaml, yml, or csv'
        )

        parser.add_argument(
            '--find', type=str, dest='lookup',
            default='',
            help='a lookup criteria for searching a list or dictionary'
        )

        parser.add_argument(
            '--select', type=str, dest='select_statement',
            default='',
            help='a select statement to enhance multiple searching criteria'
        )

        parser.add_argument(
            '--tutorial', action='store_true', dest='tutorial',
            help='show DLQuery tutorial'
        )

        parser.add_argument(
            '--tutorial-csv', action='store_true', dest='tutorial_csv',
            help='show JSON tutorial'
        )

        parser.add_argument(
            '--tutorial-json', action='store_true', dest='tutorial_json',
            help='show JSON tutorial'
        )

        parser.add_argument(
            '--tutorial-yaml', action='store_true', dest='tutorial_yaml',
            help='show JSON tutorial'
        )

        self.parser = parser

    def validate_filename(self, filename, filetype):
        raise NotImplementedError('TODO: Need to implement validate_filename')

    def run(self):
        args = self.parser.parse_args()
        chk = any(bool(i) for i in vars(args).values())

        if not chk:
            self.parser.print_help()
            sys.exit(1)

        if args.tutorial or args.tutorial_csv or args.tutorial_json or args.tutorial_yaml:
            if args.tutorial:
                show_tutorial_dlquery()
            if args.tutorial_csv:
                show_tutorial_csv()
            if args.tutorial_json:
                show_tutorial_json()
            if args.tutorial_yaml:
                show_tutorial_yaml()
            sys.exit(0)

        if not args.filename:
            print('*** --filename flag CAN NOT be empty.')
            sys.exit(1)

        self.validate_filename(args.filename, args.filetype)


def execute():
    """Execute dlquery console CLI."""
    app = Cli()
    app.run()
