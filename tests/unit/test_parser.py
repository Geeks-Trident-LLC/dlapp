import pytest
# from dlquery import DLQuery
from dlquery.parser import SelectParser


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
            (   # case: select * where a != 1 or_ c eq 3
                {'a': 1, 'b': 2, 'c': 3},               # data
                'select a, c where a ne 1 or_ c eq 3',  # select statement
                ['a', 'c'],                             # expected_columns
                True                                    # predicate_result
            ),
            (   # case: select * where a = 1 and_ c eq 3
                {'a': 1, 'b': 2, 'c': 3},                   # data
                'select a, c where a eq 1 and_ c eq 3',     # select statement
                ['a', 'c'],                                 # expected_columns
                True                                        # predicate_result
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
                'select b where a ge 20.0',     # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a lt 10',       # select statement
            ),
            (
                {'a': 5.0, 'b': 2},             # data
                'select b where a le 5',        # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a eq 5.0',      # select statement
            ),
            (
                {'a': 5, 'b': 2},               # data
                'select b where a ne 3',        # select statement
            ),
            (
                {'a': 'abc', 'b': 2},           # data
                'select b where a eq abc',      # select statement
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
                'select a where a gt version(6.3.0)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a lt version(7.0.1)',   # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a le version(7.0.1-a)',     # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},  # data
                'select a where a eq version(6.3.4)',  # select statement
            ),
            (
                {'a': '6.3.4', 'b': '2'},               # data
                'select a where a ne version(6.3.5)',   # select statement
            ),
        ]
    )
    def test_parse_statement_validating_operator(self, data, statement):
        obj = SelectParser(statement)
        obj.parse_statement()
        result = obj.predicate(data, on_exception=False)
        assert result is True
