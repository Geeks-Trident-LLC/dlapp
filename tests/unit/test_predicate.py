from dlquery.predicate import Predicate
import pytest


class TestPredicateRegex:
    """Test class for validating Regex."""
    @pytest.mark.parametrize(
        "data,key,pattern",
        [(dict(key1='Value 1'), 'key1', '[Vv]alue [0-9]+')]
    )
    def test_match(self, data, key, pattern):
        """Test matching regex."""
        chk = Predicate.match(data, key=key, pattern=pattern)
        assert chk is True

    @pytest.mark.parametrize(
        "data,key,pattern",
        [(dict(key1='Value 1'), 'key1', '[Vv]alue [a-z]+')]
    )
    def test_match(self, data, key, pattern):
        """Test matching regex."""
        chk = Predicate.notmatch(data, key=key, pattern=pattern)
        assert chk is True


class TestPredicateOperator:
    """Test class for validating Operator."""
    @pytest.mark.parametrize(
        "data,key,op,other",
        [
            # greater than
            (dict(key1=5), 'key1', '>', 3),              # compare number a > b
            (dict(key1=5), 'key1', 'gt', 3),             # compare number a > b
            (dict(key1='5.0'), 'key1', 'gt', 3.5),       # compare number a > b
            (dict(key1='5'), 'key1', 'gt', '-3.3'),      # compare number a > b
            (dict(key1=True), 'key1', 'gt', False),      # compare number a > b
            (dict(key1=True), 'key1', 'gt', 'false'),    # compare number a > b
            (dict(key1='True'), 'key1', 'gt', -1),       # compare number a > b

            # greater or equal
            (dict(key1=5), 'key1', '>=', 3),             # compare number a >= b
            (dict(key1=5), 'key1', 'ge', 3),             # compare number a >= b
            (dict(key1='5.0'), 'key1', 'ge', 5),         # compare number a >= b
            (dict(key1='5'), 'key1', 'ge', '5.0'),       # compare number a >= b
            (dict(key1=True), 'key1', 'ge', True),       # compare number a >= b
            (dict(key1=True), 'key1', 'ge', '1'),        # compare number a >= b

            # less than
            (dict(key1=2), 'key1', '<', 3),              # compare number a < b
            (dict(key1=2), 'key1', 'lt', 3),             # compare number a < b
            (dict(key1='2.0'), 'key1', 'lt', 3.5),       # compare number a < b
            (dict(key1='2'), 'key1', 'lt', '3.3'),       # compare number a < b
            (dict(key1=False), 'key1', 'lt', True),      # compare number a < b
            (dict(key1='false'), 'key1', 'lt', True),    # compare number a < b
            (dict(key1='false'), 'key1', 'lt', 2),       # compare number a < b

            # less than or equal
            (dict(key1=2), 'key1', '<=', 3),             # compare number a <= b
            (dict(key1=2), 'key1', 'le', 3),             # compare number a <= b
            (dict(key1=2), 'key1', 'le', '2.0'),         # compare number a <= b
            (dict(key1='2'), 'key1', 'le', '2.0'),       # compare number a <= b
            (dict(key1=True), 'key1', 'le', '1'),        # compare number a <= b
            (dict(key1=0), 'key1', 'le', 'false'),       # compare number a <= b

            # equal
            (dict(key1=2), 'key1', '==', 2.0),           # compare number a == b
            (dict(key1=2), 'key1', 'eq', 2.0),           # compare number a == b
            (dict(key1=2.0), 'key1', 'eq', '2'),         # compare number a == b
            (dict(key1='2'), 'key1', 'eq', '2.0'),       # compare number a == b
            (dict(key1='true'), 'key1', 'eq', 'True'),   # compare number a == b
            (dict(key1=True), 'key1', 'eq', 1),          # compare number a == b

            # not equal
            (dict(key1=2), 'key1', '!=', 2.5),           # compare number a != b
            (dict(key1=2), 'key1', 'ne', 2.5),           # compare number a != b
            (dict(key1=2.5), 'key1', 'ne', '2'),         # compare number a != b
            (dict(key1='2'), 'key1', 'ne', '2.5'),       # compare number a != b
            (dict(key1='true'), 'key1', 'ne', 'false'),  # compare number a != b
            (dict(key1='false'), 'key1', 'ne', '1'),     # compare number a != b
        ]
    )
    def test_compare_number(self, data, key, op, other):
        """Test comparing number a vs number b."""
        chk = Predicate.compare_number(data, key=key, op=op, other=other)
        assert chk is True

    @pytest.mark.parametrize(
        "data,key,op,other",
        [
            # equal
            (dict(key1='abc'), 'key1', '==', 'abc'),     # compare string a == string b
            (dict(key1='abc'), 'key1', 'eq', 'abc'),     # compare string a == string b
            (dict(key1='1.0'), 'key1', 'eq', '1.0'),     # compare string a == string b
            (dict(key1='True'), 'key1', 'eq', 'True'),   # compare string a == string b

            # not equal
            (dict(key1='abc'), 'key1', '!=', 'xyz'),     # compare string a != string b
            (dict(key1='abc'), 'key1', 'ne', 'xyz'),     # compare string a != string b
            (dict(key1='1.0'), 'key1', 'ne', '1'),       # compare string a != string b
            (dict(key1='True'), 'key1', 'ne', 'true'),   # compare string a != string b
        ]
    )
    def test_compare(self, data, key, op, other):
        """Test comparing string a vs string b."""
        chk = Predicate.compare(data, key=key, op=op, other=other)
        assert chk is True


class TestPredicateVersion:
    """Test class for validating Version Comparison."""
    @pytest.mark.parametrize(
        "data,key,op,other",
        [
            (dict(key='b'), 'key', '>', 'a'),               # version a > version b
            (dict(key='b'), 'key', 'gt', 'a'),              # version a > version b
            (dict(key='b'), 'key', 'gt', 'a.b.c.d'),        # version a > version b
            (dict(key='3'), 'key', 'gt', '2'),              # version a > version b
            (dict(key='6.4'), 'key', 'gt', '6.3.9-a'),      # version a > version b
            (dict(key='3.1'), 'key', '>=', '2.9'),          # version a >= version b
            (dict(key='3.1'), 'key', 'ge', '2.9'),          # version a >= version b
            (dict(key='6.3.9'), 'key', '<', '6.4'),         # version a < version b
            (dict(key='6.3.9'), 'key', 'lt', '6.4'),        # version a < version b
            (dict(key='6.3.9'), 'key', '<=', '6.4'),        # version a <= version b
            (dict(key='6.3.9'), 'key', 'le', '6.4'),        # version a <= version b
            (dict(key='5.3.5'), 'key', '==', '5.3.5'),      # version a == version b
            (dict(key='5.3.5'), 'key', 'eq', '5.3.5'),      # version a == version b
            (dict(key='1.0.1.a'), 'key', 'eq', '1.0.1.a'),  # version a == version b
            (dict(key='6.3.9'), 'key', '!=', '6.4.1'),      # version a != version b
            (dict(key='6.3.9'), 'key', 'ne', '6.4.1'),      # version a != version b
        ]
    )
    def test_compare_version(self, data, key, op, other):
        """Test comparing version a vs version b."""
        chk = Predicate.compare_version(data, key=key, op=op, other=other)
        assert chk is True

    @pytest.mark.parametrize(
        "data,key,op,other",
        [
            (dict(key='6.4.0'), 'key', '>', '6.3.9-a'),     # semantic version a > semantic version b
            (dict(key='6.4.0'), 'key', 'gt', '6.3.9-a'),    # semantic version a > semantic version b
            (dict(key='3.1.0'), 'key', '>=', '2.9.9'),      # semantic version a >= semantic version b
            (dict(key='3.1.0'), 'key', 'ge', '2.9.9'),      # semantic version a >= semantic version b
            (dict(key='6.3.9'), 'key', '<', '6.4.0'),       # semantic version a < semantic version b
            (dict(key='6.3.9'), 'key', 'lt', '6.4.0'),      # semantic version a < semantic version b
            (dict(key='6.3.9'), 'key', '<=', '6.4.0'),      # semantic version a <= semantic version b
            (dict(key='6.3.9'), 'key', 'le', '6.4.0'),      # semantic version a <= semantic version b
            (dict(key='1.0.1-a'), 'key', '==', '1.0.1-a'),  # semantic version a == semantic version b
            (dict(key='1.0.1-a'), 'key', 'eq', '1.0.1-a'),  # semantic version a == semantic version b
            (dict(key='6.3.9'), 'key', '!=', '6.4.1'),      # semantic version a != semantic version b
            (dict(key='6.3.9'), 'key', 'ne', '6.4.1'),      # semantic version a != semantic version b
        ]
    )
    def test_compare_semantic_version(self, data, key, op, other):
        """Test comparing semantic version a vs semantic version b."""
        chk = Predicate.compare_version(data, key=key, op=op, other=other)
        assert chk is True


class TestPredicateDate:
    """Test class for validating Date Comparison."""
    @pytest.mark.parametrize(
        "data,key,op,other",
        [
            ####################### DATETIME COMPARISON ########################
            #################################################
            # compare regular DATETIME                      #
            #################################################
            (dict(key='06/06/2021 13:30:10'), 'key', '>', '01/01/2021 11:20:10'),
            (dict(key='06/06/2021 13:30:10.111222'), 'key', 'gt', '01/01/2021 11:20:10.111222'),
            (dict(key='06/06/2021 11:30:10 PM'), 'key', 'gt', '06/06/2021 11:30:10 AM'),
            (dict(key='06/06/2021 11:30:10.111222 PM'), 'key', 'gt', '06/06/2021 11:30:10.111222 AM'),
            (dict(key='06-06-2021 11:30:10.111222 PM'), 'key', 'gt', '06-06-2021 11:30:10.111222 AM'),
            (dict(key='Jun 6 11:30:10.111222 PM 2021'), 'key', 'gt', 'Jun 6 2021 11:30:10.111222 AM'),
            (dict(key='Sun Jun  6 11:30:10.111222 PM 2021'), 'key', 'gt', 'Jun 6 2021 11:30:10.111222 AM'),
            (dict(key='Sun Jun  6 11:30 PM 2021'), 'key', 'gt', 'Jun 6 2021 11:30:10.111222 AM'),
            (dict(key='Jun 14 11:30 PM 2021'), 'key', '==', '06/14/2021 23:30:00'),
            (dict(key='Jun 14 2021'), 'key', '==', '06/14/2021'),
            (dict(key='11:30 PM'), 'key', '==', '23:30:00'),
            #################################################
            # compare ISO DATETIME                          #
            #################################################
            (dict(key='2021-06-14T08:30:00+00:00'), 'key', 'gt', '2021-06-14T07:30:00+00:00 iso=True'),

            #################################################
            # compare DATETIME with timezone option         #
            #################################################
            (
                dict(key='Sun Mar 14 01:30:30 AM 2021'), 'key',
                '<',    # less than
                'Sunday March 2021 02:10:30 AM PDT timezone=PST: -28800, PDT: -25200'
            ),
            (
                dict(key='Sun Mar 14 01:30:30 AM PST 2021'), 'key',
                '>',    # greater than
                'Sunday March 2021 02:10:30 AM PDT timezone=PST: -28800, PDT: -25200'
            ),
            (
                dict(key='Sun Mar 14 01:30:30 AM PST 2021'), 'key',
                '>',    # greater than
                'Sunday March 2021 02:10:30 AM PDT timezone=PST: -28800, PDT: America/Los_Angeles'
            ),
            #################################################
            # compare DATETIME with dayfirst option         #
            #################################################
            (
                dict(key='14/03/21 01:30:30 AM PST'), 'key',
                '>',    # greater than
                '14/03/21 02:10:30 AM PDT timezone=PST: -28800, PDT: -25200 dayfirst=True'
            ),
            (
                dict(key='21/03/14 01:30:30 AM PST'), 'key',
                '>',    # greater than
                '21/03/14 02:10:30 AM PDT timezone=PST: -28800, PDT: -25200 dayfirst=False'
            ),
            #################################################
            # compare DATETIME with fuzzy option            #
            #################################################
            (
                dict(key='today is Mon Jun 14 03:00:00 PM 2021'), 'key',
                '==',  # equal
                'today is 2021-06-14 15:00:00 fuzzy=True'
            ),
        ]
    )
    def test_compare_datetime(self, data, key, op, other):
        """Test comparing a datetime vs other datetime."""
        chk = Predicate.compare_datetime(data, key=key, op=op, other=other)
        assert chk is True
