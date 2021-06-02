"""Module containing the logic for utilities."""

import re
from collections import OrderedDict
from dlquery.argumenthelper import validate_argument_type


class UtilsError(Exception):
    """Use to capture utility error."""


class RegexConversionError(UtilsError):
    """Use to capture regular expression conversion error."""


class Printer:
    """A printer class.

    Methods
    Printer.print(data, header='', footer='', failure_msg='', print_func=None) -> None
    Printer.print_tabular(data, **kwargs) -> None
    """
    @classmethod
    def print(cls, data, header='', footer='', failure_msg='', print_func=None):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.
        footer (str): a footer text.
        failure_msg (str): a failure message.
        print_func (function): a print function.
        """
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
    def print_tabular(cls, data, **kwargs):
        """Print data in tabular format

        Parameters
        ----------
        data (list): a list of dictionary.
        kwargs (dict): keyword arguments.
        """
        msg = 'TODO: Need to implement Printer.print_tabular method'
        raise NotImplementedError(msg)


def convert_wildcard_to_regex(pattern, closed=False):
    """Convert a wildcard pattern to a regex pattern.

    Parameters
    ----------
    pattern (str): a wildcard pattern.
    closed (bool): will prepend ^ symbol and append $ symbol to pattern
            if set to True
    Returns
    -------
    str: a regular express pattern.

    Notes
    -----
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

    Parameters
    ----------
    data (Any): data
    choice (str): keys|values|items.  Default is keys.

    Returns
    -------
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
    """Return True if value is a number

    Parameters
    ----------
    value (str, int, float): a number.

    Returns
    -------
    bool: True if value is a number, otherwise, False
    """
    try:
        float(value)
        return True
    except Exception as ex:         # noqa
        return False
