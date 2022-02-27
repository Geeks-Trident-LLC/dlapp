"""Module containing the exception class for dlapp."""


class DLQueryError(Exception):
    """Use to capture error for DLQuery instance"""


class DLQueryDataTypeError(DLQueryError):
    """Use to capture error of unsupported query data type."""


class PredicateError(Exception):
    """Use to capture the predicate error."""


class PredicateParameterDataTypeError(PredicateError):
    """Use to capture the parameter data type of predicate."""
