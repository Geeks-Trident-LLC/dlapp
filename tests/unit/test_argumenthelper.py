import pytest

from dlquery.argumenthelper import validate_argument_type
from dlquery.argumenthelper import validate_argument_choice
from dlquery.argumenthelper import validate_argument_is_not_empty
from dlquery.argumenthelper import ArgumentValidationError
from dlquery.argumenthelper import ArgumentError


class Dummy:
    pass


def argument_type(arg_type_lst_or_dict=None):
    validate_argument_type(list, dict, arg_type_lst_or_dict=arg_type_lst_or_dict)


def argument_choice(choice=''):
    # choice argument must be 'car', 'bicycle'
    validate_argument_choice(choice=(choice, ('car', 'bicycle')))


def argument_is_not_empty(data='', **kwargs):
    validate_argument_is_not_empty(data=data, **kwargs)


def test_validate_argument_type():
    argument_type(arg_type_lst_or_dict=list())
    argument_type(arg_type_lst_or_dict=dict())

    with pytest.raises(ArgumentValidationError):
        argument_type()

    with pytest.raises(ArgumentValidationError):
        argument_type(arg_type_lst_or_dict='abc')

    with pytest.raises(ArgumentValidationError):
        argument_type(arg_type_lst_or_dict=123)

    with pytest.raises(ArgumentValidationError):
        argument_type(arg_type_lst_or_dict=Dummy())

    with pytest.raises(ArgumentError):
        validate_argument_type(arg_type_lst_or_dict=list())


def test_validate_argument_choice():
    argument_choice(choice='car')
    argument_choice(choice='bicycle')

    with pytest.raises(ArgumentValidationError):
        argument_choice(choice='house')

    with pytest.raises(ArgumentError):
        validate_argument_choice(choice='choice')


def test_validate_argument_is_not_empty():
    argument_is_not_empty(data='abc')
    argument_is_not_empty(data='abc', arg1='mno', arg2='xyz')

    with pytest.raises(ArgumentValidationError):
        argument_is_not_empty(data='')

    with pytest.raises(ArgumentValidationError):
        argument_is_not_empty(data='abc', arg1='', arg2='xyz')
