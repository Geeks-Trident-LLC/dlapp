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
            ########################################
            # compare default DATETIME format      #
            #    where default datetime format is  #
            #       %m/%d/%Y %H:%M:%S              #
            #       %m/%d/%Y %H:%M:%S.%f           #
            #       %m/%d/%Y %I:%M:%S %p           #
            #       %m/%d/%Y %I:%M:%S.%f %p        #
            #       -----                          #
            #       %m-%d-%Y %H:%M:%S              #
            #       %m-%d-%Y %H:%M:%S.%f           #
            #       %m-%d-%Y %I:%M:%S %p           #
            #       %m-%d-%Y %I:%M:%S.%f %p        #
            ########################################
            (dict(key='06/06/2021 13:30:10'), 'key', '>', '01/01/2021 11:20:10'),
            (dict(key='06/06/2021 13:30:10'), 'key', 'gt', '01/01/2021 11:20:10'),
            (dict(key='06/06/2021 13:30:10.111222'), 'key', 'gt', '01/01/2021 11:20:10.111222'),
            (dict(key='06/06/2021 11:30:10 PM'), 'key', 'gt', '06/06/2021 11:30:10 AM'),
            (dict(key='06/06/2021 11:30:10.111222 PM'), 'key', 'gt', '06/06/2021 11:30:10.111222 AM'),
            # -----
            (dict(key='06-06-2021 13:30:10'), 'key', 'gt', '01-01-2021 11:20:10'),
            (dict(key='06-06-2021 13:30:10.111222'), 'key', 'gt', '01-01-2021 11:20:10.111222'),
            (dict(key='06-06-2021 11:30:10 PM'), 'key', 'gt', '06-06-2021 11:30:10 AM'),
            (dict(key='06-06-2021 11:30:10.111222 PM'), 'key', 'gt', '06-06-2021 11:30:10.111222 AM'),

            ###############################################
            # compare custom DATETIME format              #
            #    which end-user needs to provide a format #
            ###############################################
            (
                # end-user needs to provide "%Y%b%d %I:%M:%S.%f %p" format
                # to parse "2021Jun6 10:30:20.111222 PM" or "2021Jan1 10:30:20.111222 AM"
                dict(key='2021Jun6 10:30:20.111222 PM'),
                'key',
                'gt',
                '2021Jan1 10:30:20.111222 AM format=%Y%b%d %I:%M:%S.%f %p'
            ),
            (
                # end-user needs to provide "%a %b %d, %Y" to parse
                #   "Mon Jun  1 11 2021" or "Tue Jan 29, 2021"
                dict(key='Mon Jun  1 14:11:50 2021'),
                'key',
                'gt',
                'Tue Jan 29 14:11:50 2021 format=%a %b %d %H:%M:%S %Y'
            ),
            #####################################################
            # compare custom DATETIME format which has timezone #
            # Timezone will support in a next release.          #
            # Use skips to ignore timezone during parsing       #
            #####################################################
            (
                # end-user needs to provide "%a %b %d %H:%M:%S %Y" to parse
                #   "Mon Jun  1 14:11:50 PDT 2021" or "Tue Jan 29 14:11:50 PST 2021"
                dict(key='Mon Jun  1 14:11:50 PDT 2021'),
                'key',
                'gt',
                'Tue Jan 29 14:11:50 PST 2021 format=%a %b %d %H:%M:%S %Y skips= PDT, PST'
            ),

            #####################################################
            # compare custom DATETIME format which a datetime   #
            # has a datetime while an other datetime has        #
            # a different datetime format                       #
            #####################################################
            (
                # end-user needs to provide
                #   "%m/%d/%Y %I:%M:%S %p" to parse "06/06/2021 05:30:10 PM"
                #    "%m/%d/%Y %H:%M:%S" to parse "06/06/2021 14:30:10"
                # Note: a separator is comma symbol which use to separator
                # two formats.
                dict(key='06/06/2021 05:30:10 PM'),
                'key',
                'gt',
                '06/06/2021 14:30:10 format,=%m/%d/%Y %I:%M:%S %p, %m/%d/%Y %H:%M:%S'
            ),

            ######################### DATE COMPARISON ##########################
            ####################################
            # compare default DATE format      #
            #    where default date format is  #
            #       %m/%d/%Y                   #
            #       %m-%d-%Y                   #
            ####################################
            (dict(key='06/06/2021'), 'key', 'gt', '01/01/2021'),
            (dict(key='06-06-2021'), 'key', 'gt', '01-01-2021'),
            (dict(key='6/6/2021'), 'key', 'gt', '01/01/2021'),
            (dict(key='6/6/2021'), 'key', 'gt', '1/1/2021'),
            ###############################################
            # compare custom DATE format                  #
            #    which end-user needs to provide a format #
            ###############################################
            (
                # end-user needs to provide "%Y%b%d" format
                # to parse "2021Jun6" or "2021Jan1"
                dict(key='2021Jun6'),
                'key',
                'gt',
                '2021Jan1 format=%Y%b%d'
            ),
            (
                # end-user needs to provide "%a %b %d, %Y" to parse
                #   "Mon Jun 1, 2021" or "Tue Jan 29, 2021"
                dict(key='Mon Jun 1, 2021'),
                'key',
                'gt',
                'Tue Jan 29, 2021 format=%a %b %d, %Y'
            ),
            #################################################
            # compare custom DATE format which has timezone #
            # Timezone will support in a next release.      #
            # Use skips to ignore timezone during parsing   #
            #################################################
            (
                # end-user needs to provide "%a %b %d, %Y" to parse
                #   "Mon Jun 1, 2021" or "Tue Jan 29, 2021"
                dict(key='Mon Jun 1, 2021 PDT'),
                'key',
                'gt',
                'Tue Jan 29, 2021 PST format=%a %b %d, %Y skips= PDT, PST'
            ),

            ######################### TIME COMPARISON ##########################
            ####################################
            # compare default TIME format      #
            #    where default time format is  #
            #       %H:%M:%S                   #
            #       %H:%M:%S.%f                #
            #       %I:%M:%S %p                #
            #       %I:%M:%S.%f %p             #
            ####################################
            (dict(key='11:50:30'), 'key', 'gt', '09:20:10'),
            (dict(key='11:50:30.333222'), 'key', 'gt', '11:50:30.222111'),
            (dict(key='11:50:30 pm'), 'key', 'gt', '11:50:30 am'),
            ###############################################
            # compare custom time format                  #
            #    which end-user needs to provide a format #
            ###############################################
            (
                # end-user needs to provide "%H:%M" format
                # to parse "13:30" or "11:10"
                dict(key='13:30'),
                'key',
                'gt',
                '11:10 format=%H:%M'
            ),
            (
                # end-user needs to provide "%H:%M %p" to parse
                #   "11:30 PM" or "11:30 AM"
                dict(key='11:30 PM'),
                'key',
                'gt',
                '11:30 AM format=%I:%M %p'
            ),
        ]
    )
    def test_compare_datetime(self, data, key, op, other):
        """Test comparing a datetime vs other datetime."""
        chk = Predicate.compare_datetime(data, key=key, op=op, other=other)
        assert chk is True
