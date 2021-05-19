"""Module containing the logic for predicate."""

import logging
from dlquery.validation import RegexValidation
from dlquery.validation import OpValidation
from dlquery.validation import CustomValidation


logger = logging.getLogger(__file__)


class PredicateError(Exception):
    """Use to capture the predicate error."""


class PredicateParameterDataTypeError(PredicateError):
    """Use to capture the parameter data type of predicate"""


def get_value(data, key):
    if not isinstance(data, dict):
        msg = 'data must be instance of dict (?? {} ??).'.format(type(data))
        raise PredicateParameterDataTypeError(msg)
    try:
        value = data.get(key)
        return value
    except Exception as ex:
        msg = 'Warning *** {}: {}'.format(type(ex).__name__, ex)
        logger.warning(msg)
        return '__EXCEPTION__'


class Predicate:
    """Contains Predicate classmethod for validation."""
    @classmethod
    def is_(cls, data, key='', custom='', on_exception=True):
        value = get_value(data, key)
        result = CustomValidation.validate(
            custom, value, on_exception=on_exception
        )
        return result

    @classmethod
    def isnot(cls, data, key='', custom='', on_exception=True):
        value = get_value(data, key)
        result = CustomValidation.validate(
            custom, value, valid=False, on_exception=on_exception
        )
        return result

    @classmethod
    def match(cls, data, key='', pattern='', on_exception=True):
        value = get_value(data, key)
        result = RegexValidation.match(
            pattern, value, on_exception=on_exception
        )
        return result

    @classmethod
    def notmatch(cls, data, key='', pattern='', on_exception=True):
        value = get_value(data, key)
        result = RegexValidation.match(
            pattern, value, valid=False, on_exception=on_exception
        )
        return result

    @classmethod
    def compare_number(cls, data, key='', op='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.compare_number(
            value, op, other, on_exception=on_exception
        )
        return result

    @classmethod
    def compare(cls, data, key='', op='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.compare(
            value, op, other, on_exception=on_exception
        )
        return result

    @classmethod
    def contain(cls, data, key='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.contain(
            value, other, on_exception=on_exception
        )
        return result

    @classmethod
    def notcontain(cls, data, key='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.contain(
            value, other, valid=False, on_exception=on_exception
        )
        return result

    @classmethod
    def belong(cls, data, key='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.belong(
            value, other, on_exception=on_exception
        )
        return result

    @classmethod
    def notbelong(cls, data, key='', other='', on_exception=True):
        value = get_value(data, key)
        result = OpValidation.belong(
            value, other, valid=False, on_exception=on_exception
        )
        return result

    @classmethod
    def true(cls, data):
        """Regardless a user provided data, it always returns True."""
        return True

    @classmethod
    def false(cls, data):
        """Regardless a user provided data, it always returns False."""
        return False
