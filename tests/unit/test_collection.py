import pytest

from dlquery.collection import Element
from dlquery.collection import LookupCls


class TestElement:
    def test_case1(self):
        data = dict(
            level1a=dict(
                level2a=dict(
                    level3a='level1a-level2a-level3a',
                    level3b='level1a-level2a-level3b'
                ),
                level2b=dict(
                    level3a='level1a-level2b-level3a',
                    level3b='level1a-level2b-level3b'
                ),
                level2c='level1a-level2c',
            ),
            level1b=dict(
                level2a='level1b-level2a',
                level2b='level1b-level2b'
            ),
            level1c='level1c',
        )
        # import pdb; pdb.set_trace()
        obj = Element(data)
        print(obj.has_children)


class TestLookupCls:
    @pytest.mark.parametrize(
        "lookup,expected_left,expected_right",
        [
            (
                'full_name',                # lookup only has left expression
                '^full_name$',              # expected left pattern
                None,                       # expected right pattern
            ),
            (
                'full++name',               # lookup only has left expression
                '^full\\+\\+name$',         # expected left pattern
                None,                       # expected right pattern
            ),
            (
                'full**name',               # lookup only has left expression
                '^full\\*\\*name$',         # expected left pattern
                None,                       # expected right pattern
            ),
            (
                '_text(full_name)',         # lookup only has left expression
                '^full_name$',              # expected left pattern
                None,                       # expected right pattern
            ),
            (
                'full_name=David M. James',     # lookup has left and right expr
                '^full_name$',                  # expected left pattern
                '^David\\ M\\.\\ James$',       # expected right pattern
            ),
            (
                '_itext(full_name)=David M. James',     # lookup has left and right expr
                '(?i)^full_name$',                      # expected left pattern
                '^David\\ M\\.\\ James$',               # expected right pattern
            ),
            (
                '_itext(full_name)=_itext(David M. James)',     # lookup has left and right expr
                '(?i)^full_name$',                              # expected left pattern
                '(?i)^David\\ M\\.\\ James$',                   # expected right pattern
            ),
            (
                'full_itext(+name)=_itext(David M. James)',     # lookup has left and right expr
                '(?i)^full\\+name$',                            # expected left pattern
                '(?i)^David\\ M\\.\\ James$',                   # expected right pattern
            ),
        ]
    )
    def test_lookup_text(self, lookup, expected_left, expected_right):
        obj = LookupCls(lookup)
        assert obj.left == expected_left
        assert obj.right == expected_right

    @pytest.mark.parametrize(
        "lookup,left_data,right_data",
        [
            (
                'full_name',                # lookup
                [                           # left data
                    ['full_name'],          # matched
                    [                       # unmatched
                        'the full_name',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [None],                 # matched
                    [None]                  # unmatched
                ]
            ),
            (
                '_itext(full_name)=_itext(David M. James)',     # lookup
                [                           # left data
                    [                       # matched
                        'full_name',
                        'Full_Name',
                        'FULL_NAME'
                    ],
                    [  # unmatched
                        'the full_name',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [                       # matched
                        'David M. James',
                        'DAVID M. JAMES'
                    ],
                    [                       # unmatched
                        'David M. Jameson',
                        'my friend name is David M. James'
                    ]
                ]
            ),
            (
                '_itext(full_name)=David _itext(M. James)',  # lookup
                [                           # left data
                    [                       # matched
                        'full_name',
                        'Full_Name',
                        'FULL_NAME'
                    ],
                    [                       # unmatched
                        'the full_name',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [                       # matched
                        'David M. James',
                        'DAVID M. JAMES'
                    ],
                    [                       # unmatched
                        'David M. Jameson',
                        'is David M. James'
                    ]
                ]
            ),
        ]
    )
    def test_lookup_text_and_verify(self, lookup, left_data, right_data):
        obj = LookupCls(lookup)
        left_matched_data, left_unmatched_data = left_data

        for data in left_matched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is True

        for data in left_unmatched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is False

        right_matched_data, right_unmatched_data = right_data
        for data in right_matched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is True

        for data in right_unmatched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is False

    @pytest.mark.parametrize(
        "lookup,expected_left,expected_right",
        [
            (
                '_wildcard(full?name)',     # lookup only has left expression
                '^full.name$',              # expected left pattern
                None,                       # expected right pattern
            ),
            (
                '_iwildcard(full?name)',    # lookup only has left expression
                '(?i)^full.name$',          # expected left pattern
                None,                       # expected right pattern
            ),
            (
                'ful_iwildcard(l?n)ame',  # lookup only has left expression
                '(?i)^full.name$',          # expected left pattern
                None,                       # expected right pattern
            ),
            (
                '_iwildcard(*name)=_iwildcard(David *James)',     # lookup has left and right expr
                '(?i)^.*name$',               # expected left pattern
                '(?i)^David .*James$',       # expected right pattern
            ),
            (
                'full_name=David_wildcard( [MTW]. )James',     # lookup has left and right expr
                '^full_name$',                          # expected left pattern
                '^David [MTW]\\. James$',               # expected right pattern
            ),
            (
                'full_name=David_wildcard( [!MTW]. )James',     # lookup has left and right expr
                '^full_name$',                            # expected left pattern
                '^David [^MTW]\\. James$',               # expected right pattern
            ),
        ]
    )
    def test_lookup_wildcard(self, lookup, expected_left, expected_right):
        obj = LookupCls(lookup)
        assert obj.left == expected_left
        assert obj.right == expected_right

    @pytest.mark.parametrize(
        "lookup,left_data,right_data",
        [
            (
                '_wildcard(full?name)',     # lookup
                [                           # left data
                    [                       # matched
                        'full?name',
                        'full_name',
                        'full name',
                        'full-name',
                        'full.name',
                        'fullaname'
                    ],
                    [                       # unmatched
                        'the full_name',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [None],                 # matched
                    [None]                  # unmatched
                ]
            ),
            (
                '_iwildcard(*name)=_wildcard(David *James)',     # lookup
                [                           # left data
                    [                       # matched
                        'first name',
                        'last NAME',
                        'anything BLABLABLA name'
                    ],
                    [                       # unmatched
                        'the full name is',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [                       # matched
                        'David James',
                        'David M. James',
                        'David BlablaBla James'
                    ],
                    [                       # unmatched
                        'David M. Jameson',
                        'my friend name is David M. James'
                    ]
                ]
            ),
            (
                'full_name=David _wildcard([WTM].) James',  # lookup
                [                           # left data
                    [                       # matched
                        'full_name',
                    ],
                    [                       # unmatched
                        'the full_name',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [                       # matched
                        'David M. James',
                        'David T. James',
                        'David W. James'
                    ],
                    [                       # unmatched
                        'David M. Jameson',
                        'is David M. James'
                    ]
                ]
            ),
            (
                    'full_name=David _wildcard([!WTM].) James',  # lookup
                    [                           # left data
                        [                       # matched
                            'full_name',
                        ],
                        [                       # unmatched
                            'the full_name',
                            'full_names'
                        ]
                    ],
                    [                           # right data
                        [                       # matched
                            'David C. James',
                            'David D. James',
                            'David J. James'
                        ],
                        [  # unmatched
                            'David M. James',
                            'David T. James',
                            'David W. James'
                        ]
                    ]
            ),
        ]
    )
    def test_lookup_wildcard_and_verify(self, lookup, left_data, right_data):
        obj = LookupCls(lookup)
        left_matched_data, left_unmatched_data = left_data

        for data in left_matched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is True

        for data in left_unmatched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is False

        right_matched_data, right_unmatched_data = right_data
        for data in right_matched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is True

        for data in right_unmatched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is False

    @pytest.mark.parametrize(
        "lookup,expected_left,expected_right",
        [
            (
                '_regex([Ff]ull[- _]?[Nn]ame)',         # lookup only has left expression
                '^[Ff]ull[- _]?[Nn]ame$',               # expected left pattern
                None,                                   # expected right pattern
            ),
            (
                '_iregex([Ff]ull[- _]?[Nn]ame)',        # lookup only has left expression
                '(?i)^[Ff]ull[- _]?[Nn]ame$',           # expected left pattern
                None,                                   # expected right pattern
            ),
            (
                    'Full_iregex([- _]?)Name',  # lookup
                    '(?i)^Full[- _]?Name$',  # expected left pattern
                    None,  # expected right pattern
            ),
            (
                '_iregex(full[- _]?name)=_iregex(David ([MTW][.] )?James)',  # lookup
                '(?i)^full[- _]?name$',  # expected left pattern
                '(?i)^David ([MTW][.] )?James$',  # expected right pattern
            ),
        ]
    )
    def test_lookup_regex(self, lookup, expected_left, expected_right):
        obj = LookupCls(lookup)
        assert obj.left == expected_left
        assert obj.right == expected_right

    @pytest.mark.parametrize(
        "lookup,left_data,right_data",
        [
            (
                '_regex(full[ ._-]name)',     # lookup
                [                           # left data
                    [                       # matched
                        'full name',
                        'full.name',
                        'full_name',
                        'full-name',
                    ],
                    [                       # unmatched
                        'full?name',
                        'Full name'
                    ]
                ],
                [                           # right data
                    [None],                 # matched
                    [None]                  # unmatched
                ]
            ),
            (
                '_iregex(\\w+ name)=_regex(David ([MTW][.] )?James)',     # lookup
                [                           # left data
                    [                       # matched
                        'first name',
                        'last NAME',
                        'any_letter name'
                    ],
                    [                       # unmatched
                        'the full name is',
                        'full_names'
                    ]
                ],
                [                           # right data
                    [                       # matched
                        'David James',
                        'David M. James',
                        'David T. James',
                        'David W. James'
                    ],
                    [                       # unmatched
                        'DAVID M. James',
                        'David M. Jameson'
                    ]
                ]
            ),
        ]
    )
    def test_lookup_regex_and_verify(self, lookup, left_data, right_data):
        obj = LookupCls(lookup)
        left_matched_data, left_unmatched_data = left_data

        for data in left_matched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is True

        for data in left_unmatched_data:
            is_match = obj.is_left_matched(data)
            assert is_match is False

        right_matched_data, right_unmatched_data = right_data
        for data in right_matched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is True

        for data in right_unmatched_data:
            if obj.is_right:
                is_match = obj.is_right_matched(data)
                assert is_match is False


    @pytest.mark.parametrize(
        "data,lookup,expected_result",
        [
            # data is empty
            ('', 'key=is_empty()', True),

            # data is not empty
            ('abc', 'key=is_not_empty()', True),

            # data is IPv4 address
            ('192.168.1.1', 'key=is_ipv4_address()', True),

            # data is not IPv4 address
            ('192.168.1.256', 'key=is_not_ipv4_address()', True),

            # data is IPv6 address
            ('2001:8a3::1', 'key=is_ipv6_address()', True),

            # data is not IPv6 address
            ('2001:8a3::1/130', 'key=is_not_ipv6_address()', True),

            # data is IP address
            ('192.168.1.1', 'key=is_ip_address()', True),
            ('2001:8a3::1', 'key=is_ip_address()', True),

            # data is not IP address
            ('192.168.1.256', 'key=is_not_ip_address()', True),
            ('2001:8a3::1/130', 'key=is_not_ip_address()', True),

            # data is MAC address
            ('aa:bb:cc:dd:ee:ff', 'key=is_mac_address()', True),
            ('aa-bb-cc-dd-ee-ff', 'key=is_mac_address()', True),
            ('aa bb cc dd ee ff', 'key=is_mac_address()', True),

            # data is not MAC address
            ('11:30:20 11:59:55', 'key=is_not_mac_address()', True),
            ('12-10-21 12-20:21', 'key=is_not_mac_address()', True),

            # data is greater than 3.0
            ('3.2', 'key=gt(3.0)', True),

            # data is greater than or equal 3.0
            ('3.2', 'key=ge(3.0)', True),
            ('3.0', 'key=ge(3)', True),

            # data is less than 4.0
            ('3.2', 'key=lt(4.0)', True),

            # data is less than or equal 4.0
            ('3.2', 'key=le(4.0)', True),
            ('4.0', 'key=le(4)', True),

            # data is equal to 4.0
            ('4', 'key=eq(4.0)', True),

            # data is not equal to 4.0
            ('3', 'key=ne(4.0)', True),

            # string comparison: data is equal to "abc"
            ('abc', 'key=eq(abc)', True),

            # string comparison: data is not equal to "abc"
            ('xyz', 'key=ne(abc)', True),
        ]
    )
    def test_validating_right_expression_for_custom_method(self, data, lookup, expected_result):
        lkup_obj = LookupCls(lookup)
        result = lkup_obj.is_right_matched(data)
        assert result == expected_result
