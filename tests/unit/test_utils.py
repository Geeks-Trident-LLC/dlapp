from dlquery import utils
import pytest
import re

################################################################################
# utils.convert_data_to_regex
################################################################################
#     Wildcard support:
#         ? (question mark): this can represent any single character.
#         * (asterisk): this can represent any number of characters
#             (including zero, in other words, zero or more characters).
#         [] (square brackets): specifies a range.
#         [!] : match any that not specifies in a range.
################################################################################


@pytest.mark.parametrize(
    "wildcard,expected_regex_pattern",
    [
        ('name?', r'^name.$'),
        ('name*', r'^name.*$'),
        ('m[aeu]n', r'^m[aeu]n$'),
        ('*.doc', r'^.*\.doc$'),
        ('[Ll]ogin', r'^[Ll]ogin$'),
        ('test [a-c]', r'^test [a-c]$'),
        ('test [!a-c]', r'^test [^a-c]$'),
        ('192.168.0.1', r'^192\.168\.0\.1$'),
        ('a.b.c', r'^a\.b\.c$'),
        ('a+b+c', r'^a\+b\+c$'),
    ]
)
def test_utility_regex_conversion(wildcard, expected_regex_pattern):
    """Test matching regex."""
    converted_regex_pattern = utils.convert_wildcard_to_regex(wildcard, closed=True)
    assert converted_regex_pattern == expected_regex_pattern


@pytest.mark.parametrize(
    "wildcard,matched_output",
    [
        (
            'name?',                                    # wildcard pattern
            ['names', 'name1', 'name_', 'name+'],       # matched output
         ),
        (
            'name*',                                    # wildcard pattern
            ['name', 'names', 'names abc xyz'],         # matched output
         ),
        (
            '*.doc',                                    # wildcard pattern
            ['file1.doc', 'a.b.doc'],                   # matched output
        ),
        (
            'm[aeu]n',                                  # wildcard pattern
            ['man', 'men', 'mun'],                      # matched output
        ),
        (
            'test [a-c]',                               # wildcard pattern
            ['test a', 'test b', 'test c'],             # matched output
        ),
        (
            'test [!a-c]',                              # wildcard pattern
            ['test 0', 'test 1', 'test d'],             # matched output
        ),
        (
            '192.168.0.1',                              # wildcard pattern
            ['192.168.0.1'],                            # matched output
        ),

    ]
)
def test_matching_regex_conversion(wildcard, matched_output):
    """Test matching regex."""
    regex_pattern = utils.convert_wildcard_to_regex(wildcard, closed=True)

    for data in matched_output:
        result = re.search(regex_pattern, data)
        is_matched = bool(result)
        assert is_matched is True


@pytest.mark.parametrize(
    "wildcard,unmatched_output",
    [
        (
            'name?',                                    # wildcard pattern
            ['name', 'name12', 'name_.', 'name abc']    # unmatched output
         ),
        (
            'name*',                                    # wildcard pattern
            ['nam', 'naming', 'a name', 'the names']    # unmatched output
         ),
        (
            '*.doc',                                    # wildcard pattern
            ['file1.docx']                              # unmatched output
        ),
        (
            'm[aeu]n',                                  # wildcard pattern
            ['min', 'myn', 'mpn', 'm-n', 'a man', 'human']       # unmatched output
        ),
        (
            '192.168.0.1',                              # wildcard pattern
            [
                '192.168.0.12',                 # unmatched output
                'addr 192.68.0.1',              # unmatched output
                '192.168.0.1 IPv4 address'      # unmatched output
            ]
        ),
    ]
)
def test_unmatched_regex_conversion(wildcard, unmatched_output):
    """Test unmatched regex."""
    regex_pattern = utils.convert_wildcard_to_regex(wildcard, closed=True)

    for data in unmatched_output:
        result = re.search(regex_pattern, data)
        is_matched = bool(result)
        assert is_matched is False


@pytest.mark.parametrize(
    "data,choice,expected_result",
    [
        # data is dict
        ({'a': 1}, 'keys', ['a']),
        ({'a': 1}, 'values', [1]),
        ({'a': 1}, 'items', [('a', 1)]),
        # data is list
        (['a', 'b'], 'keys', [0, 1]),
        (['a', 'b'], 'values', ['a', 'b']),
        (['a', 'b'], 'items', [(0, 'a'), (1, 'b')]),
        # data is tuple
        (('a', 'b'), 'keys', [0, 1]),
        (('a', 'b'), 'values', ['a', 'b']),
        (('a', 'b'), 'items', [(0, 'a'), (1, 'b')]),
    ]
)
def test_foreach_function(data, choice, expected_result):
    obj = utils.foreach(data, choice=choice)
    result = list(obj)
    assert result == expected_result

@pytest.mark.parametrize(
    "data,expected_result",
    [
        (1.1, True),
        (.1, True),
        (5, True),
        ('1.1', True),
        (' .1', True),
        (' 5 ', True),
        ('1.1.1', False),
        ('ab', False)
    ]
)
def test_is_number_function(data, expected_result):
    result = utils.is_number(data)
    assert result == expected_result