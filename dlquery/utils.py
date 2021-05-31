"""Module containing the logic for utilities."""

import re
from collections import OrderedDict
from dlquery.argumenthelper import validate_argument_type


class UtilsError(Exception):
    """Use to capture utility error."""


class RegexConversionError(UtilsError):
    """Use to capture regular expression conversion error."""


class Printer:
    @classmethod
    def print(cls, data, header='', footer='', failure_msg='', print_func=None):
        headers = str(header).splitlines()
        footers = str(footer).splitlines()
        data = data if isinstance(data, (list, tuple)) else [data]
        lst = []
        for item in data:
            lst.extend(str(item).splitlines())
        width = max(len(str(i)) for i in lst + headers + footers)
        print_func = print if print_func is None else print_func
        print_func('+-{}-+'.format('-' * width))
        if header:
            for item in headers:
                print_func('| {} |'.format(item.ljust(width)))
            print_func('+-{}-+'.format('-' * width))

        for item in lst:
            print_func('| {} |'.format(item.ljust(width)))
        print_func('+-{}-+'.format('-' * width))

        if footer:
            for item in footers:
                print_func('| {} |'.format(item.ljust(width)))
            print_func('+-{}-+'.format('-' * width))

        if failure_msg:
            print_func(failure_msg)

    @classmethod
    def print_tabular(cls, data):
        pass


def convert_wildcard_to_regex(pattern, closed=False):
    """Convert a wildcard pattern to a regex pattern.
    Parameters:
        pattern (str): a wildcard pattern.
        closed (bool): will prepend ^ symbol and append $ symbol to pattern
                if set to True
    Return:
        str: a regular express pattern.

    Wildcard support:
        ? (question mark): this can represent any single character.
        * (asterisk): this can represent any number of characters
            (including zero, in other words, zero or more characters).
        [] (square brackets): specifies a range.
        [!] : match any that not specifies in a range.

    """
    validate_argument_type(str, pattern=pattern)
    regex_pattern = ''
    try:
        regex_pattern = pattern.replace('.', r'\.')
        regex_pattern = regex_pattern.replace('+', r'\+')
        regex_pattern = regex_pattern.replace('?', '_replacetodot_')
        regex_pattern = regex_pattern.replace('*', '_replacetodotasterisk_')
        regex_pattern = regex_pattern.replace('_replacetodot_', '.')
        regex_pattern = regex_pattern.replace('_replacetodotasterisk_', '.*')
        regex_pattern = regex_pattern.replace('[!', '[^')
        regex_pattern = '^{}$'.format(regex_pattern) if closed else regex_pattern
        re.compile(regex_pattern)
        return regex_pattern
    except Exception as ex:
        fmt = 'Failed to convert wildcard({!r}) to regex({!r})\n{}'
        raise RegexConversionError(fmt.format(pattern, regex_pattern, ex))


def foreach(data, choice='keys'):
    """"a set-like object providing a view on D's keys/values/items
    Parameters:
        data (Any): data
        choice (str): keys|values|items.  Default is keys.
    Return:
        dict_keys or odict_keys if choice is keys
        dict_values or odict_values if choice is values
        dict_items or odict_items if choice is items
    """
    if isinstance(data, dict):
        node = data
    elif isinstance(data, (list, tuple)):
        total = len(data)
        node = OrderedDict(zip(range(total), data))
    else:
        node = dict()

    if choice == 'keys':
        return node.keys()
    elif choice == 'values':
        return node.values()
    else:
        return node.items()


def is_number(value):
    """Return True if value is a number"""
    try:
        float(value)
        return True
    except Exception as ex:         # noqa
        return False
