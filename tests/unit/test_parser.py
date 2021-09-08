import pytest
# from dlapp import DLQuery
from dlapp.parser import SelectParser


@pytest.fixture
def data():
    obj = {'a': 1.2, 'b': 3, 'c': 'abc xyz'}
    yield obj


class TestSelectParser:
    @pytest.mark.parametrize(
        "data,statement,expected_columns, predicate_result",
        [
            (   # case: select None
                {'a': 1, 'b': 2},           # data
                '',                         # select statement
                [None],                     # expected_columns
                None                        # predicate_result
            ),
            (   # case: select ALL
                {'a': 1, 'b': 2},           # data
                'SELECT *',                 # select statement
                [],                         # expected_columns
                None                        # predicate_result
            ),
            (   # case: select ALL
                {'a': 1, 'b': 2},           # data
                '__ALL__',                  # select statement
                [],                         # expected_columns
                None                        # predicate_result
            ),
            (   # case: select b where a = 1
                {'a': 1, 'b': 2},           # data
                'SELECT b where a eq 1',    # select statement
                ['b'],                      # expected_columns
                True                        # predicate_result
            ),
            (   # case: a, b where a = 1 (short format)
                {'a': 1, 'b': 2},           # data
                'a, b where a eq 1',        # select statement
                ['a', 'b'],                 # expected_columns
                True                        # predicate_result
            ),
            (   # case: select a, c where a != 1 or_ c eq 3
                {'a': 1, 'b': 2, 'c': 3},               # data
                'select a, c where a ne 1 or_ c eq 3',  # select statement
                ['a', 'c'],                             # expected_columns
                True                                    # predicate_result
            ),
            (  # case: select a, c where a != 1 || c eq 3
                {'a': 1, 'b': 2, 'c': 3},               # data
                'select a, c where a ne 1 || c eq 3',   # select statement
                ['a', 'c'],                             # expected_columns
                True                                    # predicate_result
            ),
            (   # case: select a, c where a = 1 and_ c eq 3
                {'a': 1, 'b': 2, 'c': 3},                   # data
                'select a, c where a eq 1 and_ c eq 3',     # select statement
                ['a', 'c'],                                 # expected_columns
                True                                        # predicate_result
            ),
            (  # case: select a, c where a = 1 and_ c eq 3
                {'a': 1, 'b': 2, 'c': 3},                   # data
                'select a, c where a eq 1 && c eq 3',       # select statement
                ['a', 'c'],                                 # expected_columns
                True                                        # predicate_result
            ),
            (  # case: a, select key name having space where "key having space" == 2
                {'a': 1, 'key name having space': 2},                                       # data
                '''select a, key name having space where "key name having space" == 2''',   # select statement
                ['a', 'key name having space'],                                             # expected_columns
                True                                                                        # predicate_result
            ),
            (  # case: select a, key name having space where 'key having space' == 2
                {'a': 1, 'key name having space': 2},                                       # data
                '''select a, key name having space where 'key name having space' == 2''',   # select statement
                ['a', 'key name having space'],                                             # expected_columns
                True                                                                        # predicate_result
            ),
        ]
    )
    def test_parse_statement(self, data, statement,
                             expected_columns, predicate_result):
        obj = SelectParser(statement)
        obj.parse_statement()
        assert obj.columns == expected_columns
        if obj.predicate is not None:
            result = obj.predicate(data)
            assert result == predicate_result

    @pytest.mark.parametrize(
        "data,statement",
        [
            (
                {'a': True, 'b': 2},            # data
                'select b where a is true',     # select statement
            ),
            (
                {'a': 'True', 'b': 2},          # data
                'select b where a is true',     # select statement
            ),
            (
                    {'a': False, 'b': 2},               # data
                    'select b where a is_not true',     # select statement
            ),
            (
                    {'a': False, 'b': 2},               # data
                    'select b where a is false',        # select statement
            ),
            (
                    {'a': 'False', 'b': 2},             # data
                    'select b where a is false',        # select statement
            ),
            (
                    {'a': True, 'b': 2},  # data
                    'select b where a is_not false',    # select statement
            ),
            (
                {'a': '', 'b': 2},                  # data
                'select b where a is empty',        # select statement
            ),
            (
                {'a': 'abc', 'b': 2},               # data
                'select b where a is_not empty',    # select statement
            ),
            (
                {'a': 'abc', 'b': 2},  # data
                'select b where a isnot empty',  # select statement
            ),
            (
                {'a': ' \t\n', 'b': 2},                 # data
                'select b where a is optional_empty',   # select statement
            ),
            (
                {'a': '', 'b': 2},                          # data
                'select b where a is_not optional_empty',   # select statement
            ),
            (
                {'a': '192.168.1.1', 'b': 2},               # data
                'select b where a is ipv4_address',         # select statement
            ),
            (
                {'a': '192.168.1.300', 'b': 2},             # data
                'select b where a is_not ipv4_address',     # select statement
            ),
            (
                {'a': '2001::1', 'b': 2},                   # data
                'select b where a is ipv6_address',         # select statement
            ),
            (
                {'a': '2001::1/150', 'b': 2},               # data
                'select b where a is_not ipv6_address',     # select statement
            ),
            (
                {'a': '192.168.1.1', 'b': 2},               # data
                'select b where a is ip_address',           # select statement
            ),
            (
                {'a': '2001::1', 'b': 2},                   # data
                'select b where a is ip_address',           # select statement
            ),
            (
                {'a': '192.168.1.300', 'b': 2},             # data
                'select b where a is_not ip_address',       # select statement
            ),
            (
                {'a': '2001::1/150', 'b': 2},               # data
                'select b where a is_not ip_address',       # select statement
            ),
            (
                {'a': '11:22:33:aa:bb:cc', 'b': 2},         # data
                'select b where a is mac_address',          # select statement
            ),
            (
                {'a': '11-22-33-aa-bb-cc', 'b': 2},         # data
                'select b where a is mac_address',          # select statement
            ),
            (
                {'a': '11 22 33 aa bb cc', 'b': 2},         # data
                'select b where a is mac_address',          # select statement
            ),
            (
                {'a': '11-22-21 12-30-21', 'b': 2},         # data
                'select b where a is_not mac_address',      # select statement
            ),
            (
                {'a': '11:22:33 12:59:55', 'b': 2},         # data
                'select b where a is_not mac_address',      # select statement
            ),
            (
                {'a': 'Loopback0', 'b': 2},                 # data
                'select b where a is loopback_interface',   # select statement
            ),
            (
                {'a': 'lo0', 'b': 2},                       # data
                'select b where a is loopback_interface',   # select statement
            ),
            (
                {'a': 'Bundle-Ether 1', 'b': 2},            # data
                'select b where a is bundle_ethernet',      # select statement
            ),
            (
                {'a': 'Bundle-Ether1.1', 'b': 2},           # data
                'select b where a is bundle_ethernet',      # select statement
            ),
            (
                {'a': 'BE1', 'b': 2},                       # data
                'select b where a is bundle_ethernet',      # select statement
            ),
            (
                {'a': 'be 1.1', 'b': 2},  # data
                'select b where a is bundle_ethernet',      # select statement
            ),
            (
                {'a': 'Port-Channel 1', 'b': 2},            # data
                'select b where a is port_channel',         # select statement
            ),
            (
                {'a': 'po 1.1', 'b': 2},                    # data
                'select b where a is port_channel',         # select statement
            ),
            (
                {'a': 'HundredGigE 0/0/0/0/1', 'b': 2},             # data
                'select b where a is hundred_gigabit_ethernet',     # select statement
            ),
            (
                {'a': 'Hu0/0/0/0/1.1', 'b': 2},                     # data
                'select b where a is hundred_gigabit_ethernet',     # select statement
            ),
            (
                {'a': 'TenGigE 0/0/0/0/1', 'b': 2},             # data
                'select b where a is ten_gigabit_ethernet',     # select statement
            ),
            (
                {'a': 'Te0/0/0/0/1.1', 'b': 2},                 # data
                'select b where a is ten_gigabit_ethernet',     # select statement
            ),
            (
                {'a': 'GigabitEthernet0/0/0/1', 'b': 2},        # data
                'select b where a is gigabit_ethernet',         # select statement
            ),
            (
                {'a': 'Gi0/0/0/1.1', 'b': 2},                   # data
                'select b where a is gigabit_ethernet',         # select statement
            ),
            (
                {'a': 'FastEthernet0/13', 'b': 2},      # data
                'select b where a is fast_ethernet',    # select statement
            ),
            (
                {'a': 'Fa0/13.1', 'b': 2},              # data
                'select b where a is fast_ethernet',    # select statement
            ),
        ]
    )
    def test_parse_statement_validating_custom_keyword(self, data, statement):
        obj = SelectParser(statement)
        obj.parse_statement()
        result = obj.predicate(data, on_exception=False)
        assert result is True

    @pytest.mark.parametrize(
        "data,statement",
        [
            (
                {'a': 'abc', 'b': 2},               # data
                'select b where a match [a-z]+',    # select statement
            ),
            (
                {'a': 'abc', 'b': 2},               # data
                'select b where a match \\w+',      # select statement
            ),
            (
                {'a': '+ - * ?', 'b': 2},               # data
                'select b where a not_match [a-z]+',    # select statement
            ),
            (
                {'a': '+ - * ?', 'b': 2},               # data
                'select b where a not_match \\w+',      # select statement
            ),
        ]
    )
    def test_parse_statement_validating_regular_expression(self, data, statement):
        obj = SelectParser(statement)
        obj.parse_statement()
        result = obj.predicate(data, on_exception=False)
        assert result is True

    @pytest.mark.parametrize(
        "data,statement",
        [
            #####################
            # number comparison #
            #####################
            (
                {'a': 20, 'b': 2},              # data
                'select b where a > 10',        # select statement
            ),
            (
                {'a': 20, 'b': 2},              # data
                'select b where a gt 10',       # select statement
            ),
            (
                {'a': '20', 'b': 2},            # data
                'select b where a gt 10',       # select statement
            ),
            (
                {'a': 20, 'b': 2},              # data
                'select b where a >= 20.0',     # select statement
            ),
            (
                {'a': 20, 'b': 2},              # data
                'select b where a ge 20.0',     # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a < 10',        # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a lt 10',       # select statement
            ),
            (
                {'a': 5.0, 'b': 2},             # data
                'select b where a <= 5',        # select statement
            ),
            (
                {'a': 5.0, 'b': 2},             # data
                'select b where a le 5',        # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a == 5.0',      # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a eq 5.0',      # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a != 3',        # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a ne 3',        # select statement
            ),
            #####################
            # string comparison #
            #####################
            (
                {'a': 'abc', 'b': 2},           # data
                'select b where a == abc',      # select statement
            ),
            (
                {'a': 'abc', 'b': 2},           # data
                'select b where a eq abc',      # select statement
            ),
            (
                {'a': 'abc', 'b': 2},           # data
                'select b where a != xyz',      # select statement
            ),
            (
                {'a': 'abc', 'b': 2},           # data
                'select b where a ne xyz',      # select statement
            ),
            (
                {'a': 'first, last', 'b': 2},       # data
                'select b where a contains first',  # select statement
            ),
            (
                {'a': 'first, last', 'b': 2},       # data
                'select b where a contain first',   # select statement
            ),
            (
                {'a': 'first, last', 'b': 2},               # data
                'select b where a not_contain middle',     # select statement
            ),
            (
                {'a': 'first', 'b': 2},                     # data
                'select b where a belongs first, last',     # select statement
            ),
            (
                {'a': 'first', 'b': 2},                 # data
                'select b where a belong first, last',  # select statement
            ),
            (
                {'a': 'middle', 'b': 2},                    # data
                'select b where a not_belong first, last',  # select statement
            ),
            ######################
            # version comparison #
            ######################
            (
                {'a': 'b', 'b': '2'},                   # data
                'select a where a > version(a)',        # select statement
            ),
            (
                {'a': 'b', 'b': '2'},                   # data
                'select a where a gt version(a)',       # select statement
            ),
            (
                {'a': 'b', 'b': '2'},                   # data
                'select a where a gt version(a.b.c.d)',  # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a >= version(6.3.0)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a ge version(6.3.0)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a < version(7.0.1)',    # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a lt version(7.0.1)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a <= version(7.0.1-a)',  # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a le version(7.0.1-a)',     # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a == version(6.3.4)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a eq version(6.3.4)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a != version(6.3.5)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a ne version(6.3.5)',   # select statement
            ),
            ###############################
            # semantic version comparison #
            ###############################
            (
                {'a': '6.4.0', 'b': '2'},                           # data
                'select a where a gt semantic_version(6.3.9-a)',    # select statement
            ),
            (
                {'a': '3.1.0', 'b': '2'},                           # data
                'select a where a ge semantic_version(2.9.9)',      # select statement
            ),
            (
                {'a': '6.3.9', 'b': '2'},                           # data
                'select a where a lt semantic_version(6.4.0)',      # select statement
            ),
            (
                {'a': '6.3.9', 'b': '2'},                           # data
                'select a where a le semantic_version(6.4.0)',      # select statement
            ),
            (
                {'a': '1.0.1-a', 'b': '2'},                         # data
                'select a where a eq semantic_version(1.0.1-a)',    # select statement
            ),
            (
                {'a': '6.3.9', 'b': '2'},                           # data
                'select a where a ne semantic_version(6.4.1)',      # select statement
            ),
            ###############################
            # datetime comparison         #
            ###############################
            (
                {'a': '2021-06-05'},                                    # data
                'select a where a == date(06/05/2021)',                 # select statement
            ),
            (
                {'a': '2021Jun05'},                                     # data
                'select a where a == date(Jun  5, 2021)',               # select statement
            ),
            (
                {'a': '03:30:50.000001 PM'},                           # data
                'select a where a > time(15:30:50)',                   # select statement
            ),
            (
                {'a': '03:30:50pm'},                                    # data
                'select a where a == time(15:30:50)',                   # select statement
            ),
            (
                {'a': '06/06/2021'},                                    # data
                'select a where a gt datetime(01/01/2021)',             # select statement
            ),
            (
                {'a': '6-6-2021'},                                          # data
                'select a where a gt datetime(Jan  1, 2021)',               # select statement
            ),
            (
                {'a': '2021-06-14T08:30:00+00:00'},                                 # data
                'select a where a > datetime(2021-06-14T07:30:00+00:00 iso=True)',  # select statement
            ),
            (
                {'a': '2021Jun06 02:30:00 PM PDT'},                                                             # data
                'select a where a > datetime(Jan  1 10:30:00 AM PST 2021 timezone=PST: -28800, PDT: -25200)',   # select statement
            ),
            (
                {'a': '2021Jun06 02:30:00 PM PDT'},                                                             # data
                'select a where a == datetime(Jun  6 14:30:00 AM PDT 2021 timezone=PST: -28800, PDT: -25200)',  # select statement
            ),
        ]
    )
    def test_parse_statement_validating_operator(self, data, statement):
        obj = SelectParser(statement)
        obj.parse_statement()
        result = obj.predicate(data, on_exception=False)
        assert result is True
