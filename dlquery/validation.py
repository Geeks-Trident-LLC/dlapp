"""Module containing the logic for validation."""

import operator
import re
from ipaddress import ip_address
import functools
import traceback
import logging
from datetime import datetime
from compare_versions.core import verify_list as version_compare

DEBUG = 0
logger = logging.getLogger(__file__)


class ValidationError(Exception):
    """Use to capture validation error."""


class ValidationIpv6PrefixError(ValidationError):
    """Use to capture validation error for a prefix of IPv6 address."""


class ValidationOperatorError(ValidationError):
    """Use to capture misused operator during Operator Validation."""


def get_ip_address(addr, is_prefix=False, on_exception=True):
    """Get an IP address.

    Parameters
    ----------
    addr (str): an IP address
    is_prefix(bool): check to return IP Address and prefix.  Default is False.
    on_exception (bool): raise Exception if it is True, otherwise, return None.

    Returns
    -------
    IPAddress: IP address, otherwise, None.
    """
    try:
        value, *grp = re.split(r'[/%]', str(addr).strip(), maxsplit=1)
        if grp:
            prefix = grp[0].strip()
            chk1 = not prefix.isdigit()
            chk2 = prefix.isdigit() and int(prefix) >= 128
            if chk1 or chk2:
                msg = '{} address containing invalid prefix.'.format(value)
                logger.warning(msg)
                raise ValidationIpv6PrefixError(msg)
        else:
            prefix = None

        if '.' in value:
            octets = value.split('.')
            if len(octets) == 4:
                if value.startswith('0'):
                    value = '.'.join(str(int(i, 8)) for i in octets)
                else:
                    len_chk = list(set(len(i) for i in octets)) == [2]
                    hex_chk = re.search(r'(?i)[a-f]', value)
                    if len_chk and hex_chk:
                        value = '.'.join(str(int(i, 16)) for i in octets)
        ip_addr = ip_address(str(value))
        return (ip_addr, prefix) if is_prefix else ip_addr
    except Exception as ex:  # noqa
        if on_exception:
            raise ex
        return (None, None) if is_prefix else None


def validate_interface(iface_name, pattern=''):
    """Verify a provided data is a network interface.

    Parameters
    ----------
    iface_name (str): a network interface
    pattern (str): sub pattern for interface name.  Default is empty.

    Returns
    -------
    bool: True if iface_name is a network interface, otherwise, False.
    """
    iface_name = str(iface_name)
    pattern = r'\b' + pattern + r' *[0-9]+(/[0-9]+)?([.][0-9]+)?\b'
    result = re.match(pattern, iface_name, re.I)
    return bool(result)


def false_on_exception_for_classmethod(func):
    """Wrap the classmethod and return False on exception.

    Parameters
    ----------
    func (function): a callable function

    Notes
    -----
    DO NOT nest this decorator.
    """
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        """A Wrapper Function"""
        chk = str(args[1]).upper()
        if chk == '__EXCEPTION__':
            return False
        try:
            result = func(*args, **kwargs)
            return result if kwargs.get('valid', True) else not result
        except Exception as ex:
            if DEBUG:
                traceback.print_exc()
            else:
                msg = 'Warning *** {}: {}'.format(type(ex).__name__, ex)
                logger.warning(msg)
            is_called_exception = kwargs.get('on_exception', False)
            if is_called_exception:
                raise ex
            else:
                return False if kwargs.get('valid', True) else True
    return wrapper_func


class RegexValidation:
    """A regular expression validation class.

    Methods
    -------
    RegexValidation.match(pattern, value, valid=True, on_exception=True) -> bool
    """
    @classmethod
    @false_on_exception_for_classmethod
    def match(cls, pattern, value, valid=True, on_exception=True):
        """Perform regular expression matching.

        Parameters
        ----------
        pattern (str): a regular expression pattern.
        value (str): data
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if match pattern, otherwise, False.
        """
        match = re.match(pattern, str(value))
        return bool(match)


class OpValidation:
    """The operator validation class

    Methods
    -------
    OpValidation.compare_number(value, op, other, valid=True, on_exception=True) -> bool
    OpValidation.compare(value, op, other, valid=True, on_exception=True) -> bool
    OpValidation.contain(value, other, valid=True, on_exception=True) -> bool
    OpValidation.belong(value, other, valid=True, on_exception=True) -> bool
    """
    @classmethod
    @false_on_exception_for_classmethod
    def compare_number(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for number.

        Parameters
        ----------
        value (str): data.
        op (str): an operator can be lt, le, gt, ge, eq, ne
        other (str): a number.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value lt|le|gt|ge|eq|ne other, otherwise, False.
        """
        op = str(op).lower().strip()
        valid_ops = ('lt', 'le', 'gt', 'ge', 'eq', 'ne')
        if op not in valid_ops:
            fmt = 'Invalid {!r} operator for validating number.  It MUST be {}.'
            raise ValidationOperatorError(fmt.format(op, valid_ops))

        v, o = str(value).lower(), str(other).lower()
        value = True if v == 'true' else False if v == 'false' else value
        other = True if o == 'true' else False if o == 'false' else other
        num = float(other)
        value = float(value)
        result = getattr(operator, op)(value, num)
        return bool(result)

    @classmethod
    @false_on_exception_for_classmethod
    def compare(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for string.

        Parameters
        ----------
        value (str): data.
        op (str): an operator can be eq or ne
        other (str): other value
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value eq|ne other, otherwise, False.
        """
        op = str(op).lower().strip()
        valid_ops = ('eq', 'ne')
        if op not in valid_ops:
            fmt = ('Invalid {!r} operator for checking equal '
                   'or via versa.  It MUST be {}.')
            raise ValidationOperatorError(fmt.format(op, valid_ops))

        result = getattr(operator, op)(value, other)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def contain(cls, value, other, valid=True, on_exception=True):
        """Perform operator checking that value contains other.

        Parameters
        ----------
        value (str): data.
        other (str): other value
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value contains other, otherwise, False.
        """
        result = operator.contains(value, other)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def belong(cls, value, other, valid=True, on_exception=True):
        """Perform operator checking that value belongs other.

        Parameters
        ----------
        value (str): data.
        other (str): other value
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value belongs other, otherwise, False.
        """
        result = operator.contains(other, value)
        return result


class CustomValidation:
    """A custom keyword validation class.

    Methods
    -------
    CustomValidation.validate(case, value, valid=True, on_exception=True) -> bool
    CustomValidation.is_ip_address(addr, valid=True, on_exception=True) -> bool
    CustomValidation.is_ipv4_address(addr, valid=True, on_exception=True) -> bool
    CustomValidation.is_ipv6_address(addr, valid=True, on_exception=True) -> bool
    CustomValidation.is_mac_address(addr, valid=True, on_exception=True) -> bool
    CustomValidation.is_loopback_interface(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_bundle_ether(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_port_channel_interface(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_hundred_gigabit_ethernet(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_ten_gigabit_ethernet(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_gigabit_ethernet(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_fast_ethernet(iface_name, valid=True, on_exception=True) -> bool
    CustomValidation.is_empty(value, valid=True, on_exception=True) -> bool
    CustomValidation.is_optional_empty(value, valid=True, on_exception=True) -> bool
    CustomValidation.is_true(value, valid=True, on_exception=True) -> bool
    CustomValidation.is_false(value, valid=True, on_exception=True) -> bool
    """

    @classmethod
    def validate(cls, case, value, valid=True, on_exception=True):
        """Look for a valid custom classmethod and process it.

        Parameters
        ----------
        case: custom validation keyword.
        value: data for validation.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if match condition, otherwise, False.

        Raise:
        NotImplementedError: if custom method doesnt exist.
        """
        case = str(case).lower()
        name = 'is_{}'.format(case)
        method = getattr(cls, name, None)
        if callable(method):
            return method(value, valid=valid, on_exception=on_exception)
        else:
            msg = 'Need to implement this case {}'.format(case)
            raise NotImplementedError(msg)

    @classmethod
    @false_on_exception_for_classmethod
    def is_ip_address(cls, addr, valid=True, on_exception=True):
        """Verify a provided data is an IP address.

        Parameters
        ----------
        addr (str): an IP address
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if addr is an IP address, otherwise, False.
        """
        ip_addr = get_ip_address(addr, on_exception=on_exception)
        chk = True if ip_addr else False
        if not chk:
            logger.info('{!r} is not an IP address.'.format(addr))
        return chk

    @classmethod
    @false_on_exception_for_classmethod
    def is_ipv4_address(cls, addr, valid=True, on_exception=True):
        """Verify a provided data is an IPv4 address.

        Parameters
        ----------
        addr (str): an IPv4 address
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if addr is an IPv4 address, otherwise, False.
        """
        ip_addr = get_ip_address(addr, on_exception=on_exception)
        chk = True if ip_addr and ip_addr.version == 4 else False
        if not chk:
            logger.info('{!r} is not an IPv4 address.'.format(addr))
        return chk

    @classmethod
    @false_on_exception_for_classmethod
    def is_ipv6_address(cls, addr, valid=True, on_exception=True):
        """Verify a provided data is an IPv6 address.

        Parameters
        ----------
        addr (str): an IPv6 address
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if addr is an IPv6 address, otherwise, False.
        """
        ip_addr = get_ip_address(addr, on_exception=on_exception)
        chk = True if ip_addr and ip_addr.version == 6 else False
        if not chk:
            logger.info('{!r} is not an IPv6 address.'.format(addr))
        return chk

    @classmethod
    @false_on_exception_for_classmethod
    def is_mac_address(cls, addr, valid=True, on_exception=True):
        """Verify a provided data is a MAC address.

        Parameters
        ----------
        addr (str): a MAC address
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if addr is a MAC address, otherwise, False.
        """
        addr = str(addr)
        patterns = [
            r'\b[0-9a-f]{2}([-: ])([0-9a-f]{2}\1){4}[0-9a-f]{2}\b',
            r'\b[a-f0-9]{4}[.][a-f0-9]{4}[.][a-f0-9]{4}\b'
        ]
        for pattern in patterns:
            result = re.match(pattern, addr, re.I)
            if result:
                return True
        return False

    # @classmethod
    # @false_on_exception_for_classmethod
    # def is_network_interface(cls, iface_name, valid=True, on_exception=True):
    #     """Verify a provided data is a network interface.
    #
    #     Parameters
    #     ----------
    #     iface_name (str): a network interface
    #     valid (bool): check for a valid result.  Default is True.
    #     on_exception (bool): raise Exception if it is True, otherwise, return None.
    #
    #     Returns
    #     -------
    #     bool: True if iface_name is a network interface, otherwise, False.
    #     """
    #     pattern = r'[a-z]+(-?[a-z0-9]+)?'
    #     result = validate_interface(iface_name, pattern=pattern)
    #     return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_loopback_interface(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a loopback interface.

        Parameters
        ----------
        iface_name (str): a loopback interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a loopback interface, otherwise, False.
        """
        pattern = r'lo(opback)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_bundle_ethernet(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a bundle-ether interface.

        Parameters
        ----------
        iface_name (str): a bundle-ether interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a bundle-ether interface, otherwise, False.
        """
        pattern = r'bundle-ether|be'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_port_channel(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a port-channel interface.

        Parameters
        ----------
        iface_name (str): a port-channel interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a bundle-ether interface, otherwise, False.
        """
        pattern = r'po(rt-channel)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_hundred_gigabit_ethernet(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a HundredGigaBit interface.

        Parameters
        ----------
        iface_name (str): a HundredGigaBitEthernet interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a HundredGigaBit interface, otherwise, False.
        """
        pattern = 'Hu(ndredGigE)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_ten_gigabit_ethernet(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a TenGigaBitEthernet interface.

        Parameters
        ----------
        iface_name (str): a TenGigaBitEthernet interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a TenGigaBitEthernet interface, otherwise, False.
        """
        pattern = 'Te(nGigE)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_gigabit_ethernet(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a TenGigaBitEthernet interface.

        Parameters
        ----------
        iface_name (str): a TenGigaBitEthernet interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a TenGigaBitEthernet interface, otherwise, False.
        """
        pattern = 'Gi(gabitEthernet)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_fast_ethernet(cls, iface_name, valid=True, on_exception=True):
        """Verify a provided data is a FastEthernet interface.

        Parameters
        ----------
        iface_name (str): a FastEthernet interface
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if iface_name is a FastEthernet interface, otherwise, False.
        """
        pattern = r'fa(stethernet)?'
        result = validate_interface(iface_name, pattern=pattern)
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def is_empty(cls, value, valid=True, on_exception=True):
        """Verify a provided data is an empty string.

        Parameters
        ----------
        value (str): a string data.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value is an empty string, otherwise, False.
        """
        value = str(value)
        return value == ''

    @classmethod
    @false_on_exception_for_classmethod
    def is_optional_empty(cls, value, valid=True, on_exception=True):
        """Verify a provided data is an optional empty string.

        Parameters
        ----------
        value (str): a string data.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value is an optional empty string, otherwise, False.
        """
        value = str(value)
        result = re.match(r'\s+$', value)
        return bool(result)

    @classmethod
    @false_on_exception_for_classmethod
    def is_true(cls, value, valid=True, on_exception=True):
        """Verify a provided data is True.

        Parameters
        ----------
        value (bool or str): a boolean or string data.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value is a True, otherwise, False.
        """
        if isinstance(value, bool):
            return value is True
        value = str(value)
        return value.lower() == 'true'

    @classmethod
    @false_on_exception_for_classmethod
    def is_false(cls, value, valid=True, on_exception=True):
        """Verify a provided data is False.

        Parameters
        ----------
        value (bool or str): a boolean or string data.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if value is a False, otherwise, False.
        """
        if isinstance(value, bool):
            return value is False
        value = str(value)
        return value.lower() == 'false'


class VersionValidation:
    """The Version comparison validation class

    Methods
    -------
    VersionValidation.compare_version(value, op, other, valid=True, on_exception=True) -> bool
    VersionValidation.compare_semantic_version(value, op, other, valid=True, on_exception=True) -> bool
    """
    @classmethod
    @false_on_exception_for_classmethod
    def compare_version(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for version.

        Parameters
        ----------
        value (str): a version.
        op (str): an operator can be lt, le, gt, ge, eq, ne
        other (str): an other version.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if a version lt|le|gt|ge|eq|ne other version, otherwise, False.
        """
        op = str(op).lower().strip()
        valid_ops = ('lt', 'le', 'gt', 'ge', 'eq', 'ne')
        if op not in valid_ops:
            fmt = 'Invalid {!r} operator for validating version.  It MUST be {}.'
            raise ValidationOperatorError(fmt.format(op, valid_ops))

        value, other = str(value), str(other)
        result = version_compare([value, other], comparison=op, scheme='string')
        return result

    @classmethod
    @false_on_exception_for_classmethod
    def compare_semantic_version(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for semantic version.

        Parameters
        ----------
        value (str): a version.
        op (str): an operator can be lt, le, gt, ge, eq, ne
        other (str): an other version.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if a version lt|le|gt|ge|eq|ne other version, otherwise, False.
        """
        op = str(op).lower().strip()
        valid_ops = ('lt', 'le', 'gt', 'ge', 'eq', 'ne')
        if op not in valid_ops:
            fmt = 'Invalid {!r} operator for validating version.  It MUST be {}.'
            raise ValidationOperatorError(fmt.format(op, valid_ops))

        value, other = str(value), str(other)
        result = version_compare([value, other], comparison=op, scheme='semver')
        return result


class DatetimeValidationError(Exception):
    """Use to capture DatetimeValidation error."""


class DatetimeValidation:
    """The Datetime comparison validation class

    Methods
    -------
    DatetimeValidation.parse_custom_date(data) -> tuple
    DatetimeValidation.apply_skips(data, skips) -> str
    DatetimeValidation.compare_datetime(value, op, other, valid=True, on_exception=True) -> bool
    """

    @classmethod
    def parse_custom_date(cls, data):
        """parse custom datetime and return date, format, and skips

        Parameters
        ----------
        data (str): datetime format=...? skips=...?

        Returns
        -------
        tuple: datetime, format, skips
        """
        if 'format=' not in data and 'skips=' not in data:
            return data, '', []
        pattern = '(?i) +(format|skips.?)='
        start = 0
        date_val, fmt, skips = '', '', []
        match_data = ''
        for m in re.finditer(pattern, data):
            before_match_data = m.string[start:m.start()]
            if not date_val:
                date_val = before_match_data
            elif not fmt and match_data.startswith('format='):
                fmt = before_match_data.strip()
            elif not skips and match_data.startswith('skips'):
                m1 = re.search(r'skips(?P<separator>.?)=', match_data)
                separator = m1.group('separator')
                separator = separator or ','
                skips = before_match_data.rstrip(separator).split(separator)
            match_data = m.group().strip()
            start = m.end()
        else:
            if not fmt and match_data.startswith('format='):
                fmt = m.string[m.end():].strip()
            elif not skips and match_data.startswith('skips'):
                m1 = re.search(r'skips(?P<separator>.?)=', match_data)
                separator = m1.group('separator')
                separator = separator or ','
                skips = m.string[m.end():].rstrip(separator).split(separator)
        return date_val, fmt, skips

    @classmethod
    def get_default_datetime_format(cls, data):
        """Return a default format for a datetime

        Parameters
        ----------
        data (str): a datetime.

        Returns
        -------
        str: a default format for datetime

        Raises
        ------
        DatetimeValidationError: if datetime format is unknown or not found.
        """
        def get_default_date_format(v):
            """get default date format.

            Parameters
            ----------
            v (str): a date data.

            Returns
            -------
            str: return a date format if matched, otherwise, empty string.
            """
            v = str(v).strip()
            pattern = r'[0-9]{1,2}([/-])[0-9]{1,2}\1[0-9]{4}$'
            match = re.match(pattern, v)
            if match:
                return '%m/%d/%Y' if '/' in match.string else '%m-%d-%Y'

            return ''

        def get_default_time_format(v):
            """get default time format.

            Parameters
            ----------
            v (str): a time data.

            Returns
            -------
            str: return a time format if matched, otherwise, empty string.
            """
            v = str(v).strip()
            time_pattern = r'''
                (?i)[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}
                (?P<microsecond>[.][0-9]+)?
                (?P<ampm> ?([ap]m)?)$
            '''
            time_pattern = r'''
                (?i)[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}
                (?P<microsecond>[.][0-9]+)?
            '''
            match = re.match(time_pattern, v, flags=re.VERBOSE)
            if match:
                fmt = '%H:%M:%S'
                if match.group('microsecond'):
                    fmt += '.%f'
                if v.lower().endswith(' am') or v.lower().endswith(' pm'):
                    fmt += ' %p'
                    fmt = fmt.replace('%H', '%I')
                return fmt
            return ''

        date_fmt = get_default_date_format(data)
        if date_fmt:
            return date_fmt

        time_fmt = get_default_time_format(data)
        if time_fmt:
            return time_fmt

        lst = data.split(' ', maxsplit=1)
        if len(lst) == 2:
            date_val, time_val = lst
            date_fmt = get_default_date_format(date_val)
            time_fmt = get_default_time_format(time_val)
            if date_fmt and time_val:
                return '{} {}'.format(date_fmt, time_fmt)
            else:
                msg = ('{!r} is a custom datetime.  '
                       'Need to end-user provide a custom format.')
                raise DatetimeValidationError(msg)
        else:
            msg = ('{!r} is a custom datetime.  '
                   'Need to end-user provide a custom format.')
            raise DatetimeValidationError(msg)

    @classmethod
    def apply_skips(cls, data, skips):
        """Take out any skip data and return datetime without skip data

        Parameters
        ----------
        data (str): datetime <skip data>
        skips (list): a list of skip data

        Returns
        -------
        str: new datetime without skip data
        """
        for skip in skips:
            try:
                re.compile(skip)
                pattern = skip
            except Exception as ex:     # noqa
                pattern = re.escape(skip)

            data = re.sub(pattern, '', data, re.I)
        return data.strip()

    @classmethod
    @false_on_exception_for_classmethod
    def compare_datetime(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for datetime.

        Parameters
        ----------
        value (str): a datetime.
        op (str): an operator can be lt, le, gt, ge, eq, ne
        other (str): an other datetime.
        valid (bool): check for a valid result.  Default is True.
        on_exception (bool): raise Exception if it is True, otherwise, return None.

        Returns
        -------
        bool: True if a datetime lt|le|gt|ge|eq|ne other datetime, otherwise, False.
        """
        other_date_str, fmt, skips = DatetimeValidation.parse_custom_date(other)

        a_date_str = DatetimeValidation.apply_skips(value, skips)
        other_date_str = DatetimeValidation.apply_skips(other_date_str, skips)

        if not fmt:
            fmt = DatetimeValidation.get_default_datetime_format(other_date_str)

        a_date = datetime.strptime(a_date_str, fmt)
        other_date = datetime.strptime(other_date_str, fmt)

        result = getattr(operator, op)(a_date, other_date)
        return result
