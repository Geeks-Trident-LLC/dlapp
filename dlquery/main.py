"""Module containing the logic for the dlquery entry-points."""

import sys
import argparse
from os import path


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
        self.result = None

        parser = argparse.ArgumentParser(
            prog='dlquery',
            usage='%(prog)s [options]',
            description='%(prog)s application',
        )

        parser.add_argument(
            '--application', action='store_true',
            help='launch a dlquery GUI application'
        )

        parser.add_argument(
            '--filename', type=str,
            default='',
            help='a json, yaml, or csv file name'
        )

        parser.add_argument(
            '--filetype', type=str, choices=['csv', 'json', 'yaml', 'yml'],
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
            help='show dlquery tutorial'
        )

        parser.add_argument(
            '--tutorial-csv', action='store_true', dest='tutorial_csv',
            help='show csv tutorial'
        )

        parser.add_argument(
            '--tutorial-json', action='store_true', dest='tutorial_json',
            help='show json tutorial'
        )

        parser.add_argument(
            '--tutorial-yaml', action='store_true', dest='tutorial_yaml',
            help='show yaml tutorial'
        )

        self.parser = parser

    @property
    def is_csv_type(self):
        """Return True if filetype is csv"""
        return self.filetype == 'csv'

    @property
    def is_json_type(self):
        """Return True if filetype is json"""
        return self.filetype == 'json'

    @property
    def is_yaml_type(self):
        """Return True if filetype is yml or yaml"""
        return self.filetype in ['yml', 'yaml']

    def validate_filename(self, options):
        """Validate `filename` flag which is a file type of `csv`,
        `json`, `yml`, or `yaml`

        Parameters
        ----------
        options (argparse.Namespace): a argparse.Namespace instance.

        Returns
        -------
        bool: True if `filename` is valid, otherwise, ``sys.exit(1)``
        """
        filename, filetype = str(options.filename), str(options.filetype)
        if not filename:
            print('*** --filename flag CAN NOT be empty.')
            sys.exit(1)

        self.filename = filename
        self.filetype = filetype

        _, ext = path.splitext(filename)
        ext = ext.lower()
        if ext in ['.csv', '.json', '.yml', '.yaml']:
            self.filetype = ext[1:]
            return True

        if not filetype:
            if ext == '':
                fmt = ('*** {} file doesnt have an extension.  '
                       'System cant determine a file type.  '
                       'Please rerun with --filetype=<filetype> '
                       'where filetype is csv, json, yml, or yaml.')

            else:
                fmt = ('*** {} file has an extension but it is not '
                       'csv, json, yml, or yaml.  If you think this file is'
                       'csv, json, yml, or yaml, '
                       'please rerun with --filetype=<filetype> '
                       'where filetype is csv, json, yml, or yaml.')
            print(fmt.format(filename))
            sys.exit(1)
        else:
            self.filetype = filetype

    def run(self):
        """Take CLI arguments, parse it, and process."""
        options = self.parser.parse_args()
        chk = any(bool(i) for i in vars(options).values())

        if not chk:
            self.parser.print_help()
            sys.exit(1)

        if options.tutorial or options.tutorial_csv or options.tutorial_json or options.tutorial_yaml:
            if options.tutorial:
                show_tutorial_dlquery()
            if options.tutorial_csv:
                show_tutorial_csv()
            if options.tutorial_json:
                show_tutorial_json()
            if options.tutorial_yaml:
                show_tutorial_yaml()
            sys.exit(0)

        self.validate_filename(options)


def execute():
    """Execute dlquery console CLI."""
    app = Cli()
    app.run()
