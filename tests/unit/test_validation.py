from dlquery.validation import RegexValidation
from dlquery.validation import OpValidation
from dlquery.validation import CustomValidation
from dlquery.validation import VersionValidation
from dlquery.validation import DatetimeValidation
import pytest


class TestCustomValidation:
    """Test class for validating Regex."""
    @pytest.mark.parametrize(
        "case,data,status",
        [
            ('ipv4_address', '192.168.0.1', True),              # valid addresses in decimal
            ('ipv4_address', 'c0.a8.00.01', True),              # valid addresses in hexadecimal
            ('ipv4_address', '0300.0250.00.01', True),          # valid addresses in octal
            ('ipv4_address', '192.168.0.256', False),           # invalid addresses in decimal
            ('ipv4_address', 'c0.a8.00.100', False),            # invalid addresses in hexadecimal
            ('ipv4_address', '0300.0250.00.0400', False),       # invalid addresses in octal
            ('ipv6_address', '::', True),                       # valid addresses
            ('ipv6_address', '::1', True),                      # valid addresses
            ('ipv6_address', '2001::', True),                   # valid addresses
            ('ipv6_address', '2001::b1c2', True),               # valid addresses
            ('ipv6_address', '2001:a011:8d38:6ab8:1c50:3a2c:a953:c2b1', True),  # valid addresses
            ('ipv6_address', '2001::b1c2%64', True),            # valid address with prefix
            ('ipv6_address', '2001::b1c2/32', True),            # valid address with other prefix
            ('ipv6_address', '2001::8d38:a953::c2b1', False),   # invalid addresses
            ('ipv6_address', '::a011::3a2c::c2b1', False),      # invalid addresses
            ('ipv6_address', '2001::8d38:3a2c:a953::', False),  # invalid addresses
            ('ipv6_address', '2001::b1c2%130', False),          # addresses with invalid prefix
            ('ipv6_address', '2001::b1c2%1a', False),           # addresses with invalid prefix
            ('ipv6_address', '2001::b1c2/150', False),          # addresses with other invalid prefix
            ('ipv6_address', '2001::b1c2%5c', False),           # addresses with other invalid prefix
        ]
    )
    def test_validate_method(self, case, data, status):
        """Test validate method."""
        chk = CustomValidation.validate(case, data, valid=status, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '0.0.0.0', '1.1.1.1', '11.11.11.11',            # valid addresses in decimal
            '111.111.111.111', '255.255.255.255',           # valid addresses in decimal
            '00.00.00.00', 'aa.aa.aa.aa', 'ff.ff.ff.ff',    # valid addresses in hexadecimal
            '00.00.00.00', '011.011.011.011',               # valid addresses in octal digit
            '0111.0111.0111.0111', '0377.0377.0377.0377'    # valid addresses in octal digit
        ]
    )
    def test_is_ipv4_address(self, addr):
        """Test is an IPv4 address."""
        chk = CustomValidation.is_ipv4_address(addr, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '256.0.0.0', '1.256.1.1', '11.11.256.11',           # invalid addresses in decimal
            '111.111.111.256', '256.257.258.259',               # invalid addresses in decimal
            '1ff.00.00.00', 'aa.1ff.aa.aa', 'ff.ff.1ff.ff',     # invalid addresses in hexadecimal
            '0378.00.00.00', '011.0378.011.011',                # invalid addresses in octal
            '0111.0111.378.0111', '0377.0377.0377.0378'         # invalid addresses in octal
        ]
    )
    def test_is_not_ipv4_address(self, addr):
        """Test is not an IPv4 address."""
        chk = CustomValidation.is_ipv4_address(addr, valid=False, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '::', '::1', '2001::', '2001::b1c2',        # valid address
            '2001:a011:8d38:6ab8:1c50:3a2c:a953:c2b1',  # valid address
            '2001::b1c2%64',                            # valid address with prefix
            '2001::b1c2/32'                             # valid address with other prefix
        ]
    )
    def test_is_ipv6_address(self, addr):
        """Test is an IPv6 address."""
        chk = CustomValidation.is_ipv6_address(addr, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '2001::1c50::a953:c2b1',                    # invalid address
            '::a011:3a2c::c2b1',                        # invalid address
            '2001::8d38:3a2c:a953::',                   # invalid address
            '2001::b1c2%130',                           # address with invalid prefix
            '2001::b1c2%1a',                            # address with invalid prefix
            '2001::b1c2/150',                           # address with other invalid prefix
            '2001::b1c2/5c'                             # address with other invalid prefix
        ]
    )
    def test_is_not_ipv6_address(self, addr):
        """Test is not an IPv6 address."""
        chk = CustomValidation.is_ipv6_address(addr, valid=False, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '0.0.0.0', '1.1.1.1', '11.11.11.11',            # valid addresses in decimal
            '111.111.111.111', '255.255.255.255',           # valid addresses in decimal
            '00.00.00.00', 'aa.aa.aa.aa', 'ff.ff.ff.ff',    # valid addresses in hexadecimal
            '00.00.00.00', '011.011.011.011',               # valid addresses in octal digit
            '0111.0111.0111.0111', '0377.0377.0377.0377',   # valid addresses in octal digit
            '::', '::1', '1::', '2001::b1c2',               # valid address
            '2001:a011:8d38:6ab8:1c50:3a2c:a953:c2b1',      # valid address
            '2001::b1c2%64',                                # valid address with prefix
            '2001::b1c2/32'                                 # valid address with other prefix
        ]
    )
    def test_is_ip_address(self, addr):
        """Test is an IP address."""
        chk = CustomValidation.is_ip_address(addr, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "addr",
        [
            '256.0.0.0', '1.256.1.1', '11.11.256.11',           # invalid addresses in decimal
            '111.111.111.256', '256.257.258.259',               # invalid addresses in decimal
            '1ff.00.00.00', 'aa.1ff.aa.aa', 'ff.ff.1ff.ff',     # invalid addresses in hexadecimal
            '0378.00.00.00', '011.0378.011.011',                # invalid addresses in octal
            '0111.0111.378.0111', '0377.0377.0377.0378',        # invalid addresses in octal
            '2001::1c50::a953:c2b1',                            # invalid address
            '::a011:3a2c::c2b1',                                # invalid address
            '2001::8d38:3a2c:a953::',                           # invalid address
            '2001::b1c2%130',                                   # address with invalid prefix
            '2001::b1c2%1a',                                    # address with invalid prefix
            '2001::b1c2/150',                                   # address with other invalid prefix
            '2001::b1c2/5c'                                     # address with other invalid prefix
        ]
    )
    def test_is_not_ip_address(self, addr):
        """Test is not an IP address."""
        chk = CustomValidation.is_ip_address(addr, valid=False, on_exception=False)
        assert chk is True


class TestRegexValidation:
    """Test class for validating Regex."""
    @pytest.mark.parametrize(
        "data,pattern",
        [('Value 1', '[Vv]alue [0-9]+')]
    )
    def test_match(self, data, pattern):
        """Test matching regex."""
        chk = RegexValidation.match(pattern, data, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,pattern",
        [('Value 1', '[Vv]alue [a-z]+')]
    )
    def test_notmatch(self, data, pattern):
        """Test not matching regex."""
        chk = RegexValidation.match(pattern, data, valid=False, on_exception=False)
        assert chk is True


class TestOpValidation:
    """Test class for validating Operator."""
    @pytest.mark.parametrize(
        "data,other",
        [(5, 3), (5, 3.5), (5, '3.3')]
    )
    def test_compare_number_a_gt_b(self, data, other):
        """Test number a gt number b."""
        chk = OpValidation.compare_number(data, 'gt', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [
            (5, 3), (5, 3.5), (5, '3.3'),   # test greater than
            (5, 5), (5, 5.0), (5, '5.0')    # test equal
        ]
    )
    def test_compare_number_a_ge_b(self, data, other):
        """Test number a ge number b."""
        chk = OpValidation.compare_number(data, 'ge', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [(2, 3), (2, 3.5), (2, '3.3')]
    )
    def test_compare_number_a_lt_b(self, data, other):
        """Test number a lt number b."""
        chk = OpValidation.compare_number(data, 'lt', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [
            (2, 3), (2, 3.5), (2, '3.3'),   # test less than
            (2, 2), (2, 2.0), (2, '2.0')    # test equal
        ]
    )
    def test_compare_number_a_le_b(self, data, other):
        """Test number a le number b."""
        chk = OpValidation.compare_number(data, 'le', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [(2, 2), (2, 2.0), (2, '2.0')]
    )
    def test_compare_number_a_eq_b(self, data, other):
        """Test number a eq number b."""
        chk = OpValidation.compare_number(data, 'eq', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [(3, 2.1), (3, 2.2), (3, '2.3')]
    )
    def test_compare_number_a_ne_b(self, data, other):
        """Test number a ne number b."""
        chk = OpValidation.compare_number(data, 'ne', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('abc', 'abc')]
    )
    def test_compare_string_a_eq_b(self, data, other):
        """Test string a eq string b."""
        chk = OpValidation.compare(data, 'eq', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('abc', 'xyz')]
    )
    def test_compare_string_a_ne_b(self, data, other):
        """Test string a ne string b."""
        chk = OpValidation.compare(data, 'ne', other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('Clingstone Peaches', 'Clingstone')]
    )
    def test_string_a_contain_b(self, data, other):
        """Test string a contains string b."""
        chk = OpValidation.contain(data, other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('Clingstone Peaches', 'Freestone')]
    )
    def test_string_a_not_contain_b(self, data, other):
        """Test string a contains string b."""
        chk = OpValidation.contain(data, other, valid=False, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('Clingstone', 'Clingstone Peaches')]
    )
    def test_string_a_belong_b(self, data, other):
        """Test string a contains string b."""
        chk = OpValidation.belong(data, other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,other",
        [('Clingstone', 'Freestone Peaches')]
    )
    def test_string_a_not_belong_b(self, data, other):
        """Test string a contains string b."""
        chk = OpValidation.belong(data, other, valid=False, on_exception=False)
        assert chk is True


class TestVersionValidation:
    """Test class for validating Operator."""
    @pytest.mark.parametrize(
        "data,op,other",
        [
            ('b', 'gt', 'a'),               # version a > version b
            ('b', 'gt', 'a.b.c.d'),         # version a > version b
            ('3', 'gt', '2'),               # version a > version b
            ('6.4', 'gt', '6.3.9-a'),       # version a > version b
            ('3.1', 'ge', '2.9'),           # version a >= version b
            ('6.3.9', 'lt', '6.4'),         # version a < version b
            ('6.3.9', 'le', '6.4'),         # version a <= version b
            ('5.3.5', 'eq', '5.3.5'),       # version a == version b
            ('1.0.1.a', 'eq', '1.0.1.a'),   # version a == version b
            ('6.3.9', 'ne', '6.4.1'),       # version a != version b
        ]
    )
    def test_compare_version(self, data, op, other):
        """Test version a gt|ge|lt|le|eq|ne version b."""
        chk = VersionValidation.compare_version(data, op, other, on_exception=False)
        assert chk is True

    @pytest.mark.parametrize(
        "data,op,other",
        [
            ('6.4.0', 'gt', '6.3.9-a'),         # semantic version a > semantic version b
            ('3.1.0', 'ge', '2.9.9'),           # semantic version a >= semantic version b
            ('6.3.9', 'lt', '6.4.0'),           # semantic version a < semantic version b
            ('6.3.9', 'le', '6.4.0'),           # semantic version a <= semantic version b
            ('1.0.1-a', 'eq', '1.0.1-a'),       # semantic version a == semantic version b
            ('6.3.9', 'ne', '6.4.1'),           # semantic version a != semantic version b
        ]
    )
    def test_compare_semantic_version(self, data, op, other):
        """Test version a gt|ge|lt|le|eq|ne version b."""
        chk = VersionValidation.compare_semantic_version(
            data, op, other, on_exception=False
        )
        assert chk is True


class TestDatetimeValidation:
    """Test class for validating Datetime comparison."""
    @pytest.mark.parametrize(
        "data,op,other",
        [
            ('06/06/2021', 'gt', '01/01/2021'),                     # a date > other date
            ('6/6/2021', 'gt', '01/01/2021'),                       # a date > other date
            ('06-06-2021', 'gt', '01-01-2021 format=%m-%d-%Y'),     # a date > other date with format
            (
                # a date > other date with custom format and skips
                '2021Jun06 PDT',                                    # a date
                'gt',                                               # operator greater than
                '2021Jan01 PST format=%Y%b%d skips= PDT, PST'       # other day with format and skips
            ),
            ('Jun 3, 2021', 'ge', 'Jan 29, 2021 format=%b %d, %Y'),     # a date >= other date
            ('01/01/2021', 'lt', '06/06/2021'),                         # a date < other date
            ('01/01/2021', 'le', '06/06/2021'),                         # a date < other date
            ('06/06/2021', 'eq', '06/06/2021'),                         # a date == other date
            ('01/01/2021', 'ne', '06/06/2021'),                         # a date != other date

        ]
    )
    def test_compare_version(self, data, op, other):
        """Test a date gt|ge|lt|le|eq|ne other date."""
        result = DatetimeValidation.compare_date(
            data, op, other, on_exception=False
        )
        assert result is True
