"""Module containing the logic for validation."""

import operator
import re
from ipaddress import ip_address
import functools
import traceback
import logging
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
    OpValidation.compare_string(value, op, other, valid=True, on_exception=True) -> bool
    OpValidation.compare_semantic(value, op, other, valid=True, on_exception=True) -> bool
    """
    @classmethod
    @false_on_exception_for_classmethod
    def compare_version(cls, value, op, other, valid=True, on_exception=True):
        """Perform operator comparison for version.

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

        value, other = str(value), str(other)
        result = version_compare([value, other], comparison=op, scheme='string')
        return result
