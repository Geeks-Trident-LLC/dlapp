"""Module containing the exception class for dlapp."""


class DLQueryError(Exception):
    """Use to capture error for DLQuery instance"""


class DLQueryDataTypeError(DLQueryError):
    """Use to capture error of unsupported query data type."""


class PredicateError(Exception):
    """Use to capture the predicate error."""


class PredicateParameterDataTypeError(PredicateError):
    """Use to capture the parameter data type of predicate."""


class ValidationError(Exception):
    """Use to capture validation error."""


class ValidationIpv6PrefixError(ValidationError):
    """Use to capture validation error for a prefix of IPv6 address."""


class ValidationOperatorError(ValidationError):
    """Use to capture misused operator during Operator Validation."""


class ParsedTimezoneError(Exception):
    """Use to capture timezone during parsing custom datetime."""
