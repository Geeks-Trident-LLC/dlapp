"""Module containing the logic for the argument helper."""


class ArgumentError(Exception):
    """Use to capture argument error."""


class ArgumentValidationError(ArgumentError):
    """Use to capture argument validation."""


def validate_argument_type(*args, **kwargs):
    """Validate function/method argument type.

    Parameters:
        args (tuple): list of data type
        kwargs (dict): list of argument that needs to valid their types

    Return:
        bool: True if arguments match their types.

    Exception:
        ArgumentError, ArgumentValidationError
    """
    if len(args) == 0:
        msg = 'Cannot validate argument with no reference data type.'
        raise ArgumentError(msg)
    else:
        for arg in args:
            if not issubclass(arg, object):
                msg = 'args must contain all classes.'
                raise ArgumentError(msg)

    fmt = '{} argument must be a data type of {}.'
    type_name = ', '.join(arg.__name__ for arg in args)
    type_name = '({})'.format(type_name) if len(args) > 1 else type_name

    for name, obj in kwargs.items():
        if not isinstance(obj, args):
            raise ArgumentValidationError(fmt.format(name, type_name))
    return True


def validate_argument_choice(**kwargs):
    """Validate function/method argument choice.

    Parameters:
        kwargs (dict): list of argument that needs to valid their types
            a value of (key, value) pair must consist
            argument value and a list of choices.

    Return:
        bool: True if argument matches its argument choice.

    Exception:
        ArgumentError, ArgumentValidationError
    """
    for name, value in kwargs.items():
        try:
            argument, choices = value
        except Exception as ex:
            msg = 'Invalid argument for verifying validate_argument_choice'
            raise ArgumentError(msg)

        is_not_a_list = not isinstance(choices, (list, tuple))
        is_empty = not bool(choices)

        if is_not_a_list or is_empty:
            raise ArgumentError('choices CAN NOT be empty.')

        if argument not in choices:
            fmt = '{} argument must be a choice of {}.'
            raise ArgumentValidationError(fmt.format(name, choices))
    return True
