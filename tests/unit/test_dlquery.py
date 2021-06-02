from dlquery import DLQuery
import pytest


class ExpectedResult:
    def __init__(self):
        self.dict_result = dict(a='Apricot', b='Banana')
        self.list_result = [2021, 'Hello dlquery', dict(self.dict_result)]
        self.dict_other_result = dict(a='Apricot', c='Cherry')
        self.list_other_result = [
            2021, 'Hello python', dict(self.dict_other_result)
        ]
        # dict result
        self.key1 = 'a'
        self.key2 = 'b'
        self.value1 = 'Apricot'
        self.value2 = 'Banana'

        # list result
        self.index0 = 2021
        self.index1 = 'Hello dlquery'
        self.index2 = dict(self.dict_result)

        # number
        self.zero = 0
        self.one = 1
        self.two = 2
        self.three = 3

        # bool
        self.true = True
        self.false = False

        # constant
        self.not_found = 'NOT_FOUND'


@pytest.fixture
def expected_result():
    yield ExpectedResult()


@pytest.fixture
def dict_data():
    obj = {'a': 'Apricot', 'b': 'Banana'}
    yield obj


@pytest.fixture
def list_data(dict_data):
    obj = [2021, 'Hello dlquery', dict(dict_data)]
    yield obj


@pytest.fixture
def dict_other_data():
    obj = {'a': 'Apricot', 'c': 'Cherry'}
    yield obj


@pytest.fixture
def list_other_data(dict_other_data):
    obj = [2021, 'Hello python', dict(dict_other_data)]
    yield obj


@pytest.fixture
def empty_dldata():
    empty_dict, empty_list = dict(), list()
    obj1, obj2 = DLQuery(empty_dict), DLQuery(empty_list)
    yield obj1, obj2


@pytest.fixture
def dldata(dict_data, list_data):
    obj1, obj2 = DLQuery(dict_data), DLQuery(list_data)
    yield obj1, obj2


@pytest.fixture
def other_dldata(dict_other_data, list_other_data):
    obj1, obj2 = DLQuery(dict_other_data), DLQuery(list_other_data)
    yield obj1, obj2


class TestDLQuery:
    def test_len_function(self, dldata, empty_dldata, expected_result):

        dict_obj, list_obj = dldata

        dict_obj_len = len(dict_obj)
        assert dict_obj_len == expected_result.two

        list_obj_len = len(list_obj)
        assert list_obj_len == expected_result.three

        empty_dict, empty_list = empty_dldata

        empty_dict_len = len(empty_dict)
        assert empty_dict_len == expected_result.zero

        empty_list_len = len(empty_list)
        assert empty_list_len == expected_result.zero

    def test_bool_function(self, dldata, empty_dldata, expected_result):

        dict_obj, list_obj = dldata
        assert bool(dict_obj)
        assert bool(list_obj)
        assert dict_obj
        assert list_obj

        empty_dict, empty_list = empty_dldata
        assert bool(empty_dict) == expected_result.false
        assert bool(empty_list) == expected_result.false
        assert not empty_dict
        assert not empty_list

    def test_eq(self, dldata, dict_data, list_data, expected_result):
        data_dict_obj, data_list_obj = dldata
        assert data_dict_obj == dict_data
        assert data_dict_obj == expected_result.dict_result

        assert data_list_obj == list_data
        assert data_list_obj == expected_result.list_result

    def test_ne(self, dldata, other_dldata, dict_other_data,
                list_other_data, expected_result):
        data_dict_obj, data_list_obj = dldata
        data_dict_other_obj, data_list_other_obj = other_dldata

        assert data_dict_obj != data_dict_other_obj
        assert data_dict_obj != dict_other_data
        assert data_dict_obj != expected_result.dict_other_result

        assert data_list_obj != data_list_other_obj
        assert data_list_obj != list_other_data
        assert data_list_obj != expected_result.list_other_result

    def test_getitem(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        key1, key2 = 'a', 'b'
        index0, index1, index2 = 0, 1, 2

        assert data_dict_obj[key1] == expected_result.value1
        assert data_dict_obj[key2] == expected_result.value2

        assert data_list_obj[index0] == expected_result.index0
        assert data_list_obj[index1] == expected_result.index1
        assert data_list_obj[index2] == expected_result.index2
        assert data_list_obj[index2][key1] == expected_result.value1
        assert data_list_obj[index2][key2] == expected_result.value2

    def test_is_dict_property(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        assert data_dict_obj.is_dict == expected_result.true
        assert data_list_obj.is_dict == expected_result.false

        with pytest.raises(AssertionError):
            assert data_list_obj.is_dict == expected_result.true

    def test_is_list_property(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        assert data_list_obj.is_list == expected_result.true
        assert data_dict_obj.is_list == expected_result.false

        with pytest.raises(AssertionError):
            assert data_dict_obj.is_list == expected_result.true

    def test_get_method(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        default = 'NOT_FOUND'

        # case 1: DLQuery is holding a dictionary
        assert data_dict_obj.get('a', default=default) == expected_result.value1
        assert data_dict_obj.get('b', default=default) == expected_result.value2
        assert data_dict_obj.get('c', default=default) == expected_result.not_found

        # case 2: DLQuery is holding a list
        assert data_list_obj.get(0, default=default) == expected_result.index0
        assert data_list_obj.get('0', default=default) == expected_result.index0

        assert data_list_obj.get(1, default=default) == expected_result.index1
        assert data_list_obj.get('1', default=default) == expected_result.index1

        assert data_list_obj.get(2, default=default) == expected_result.index2
        assert data_list_obj.get('2', default=default) == expected_result.index2

        assert data_list_obj.get(3, default=default) == expected_result.not_found
        assert data_list_obj.get('3', default=default) == expected_result.not_found

        assert data_list_obj.get(-4, default=default) == expected_result.not_found
        assert data_list_obj.get('-4', default=default) == expected_result.not_found

        assert data_list_obj.get(-3, default=default) == expected_result.index0
        assert data_list_obj.get('-3', default=default) == expected_result.index0

        assert data_list_obj.get(-2, default=default) == expected_result.index1
        assert data_list_obj.get('-2', default=default) == expected_result.index1

        assert data_list_obj.get(-1, default=default) == expected_result.index2
        assert data_list_obj.get('-1', default=default) == expected_result.index2

        with pytest.raises(TypeError):
            data_list_obj.get('abc', default=default, on_exception=True)

        with pytest.raises(IndexError):
            data_list_obj.get(3, default=default, on_exception=True)

        with pytest.raises(IndexError):
            data_list_obj.get('3', default=default, on_exception=True)

        with pytest.raises(IndexError):
            data_list_obj.get(-4, default=default, on_exception=True)

        with pytest.raises(IndexError):
            data_list_obj.get('-4', default=default, on_exception=True)

        # case 3: slicing
        eresult = [
            expected_result.index0,
            expected_result.index1,
            expected_result.index2
        ]
        assert data_list_obj.get(':', default=default) == eresult
        assert data_list_obj.get(':3', default=default) == eresult
        assert data_list_obj.get('0:3', default=default) == eresult
        assert data_list_obj.get('-3:', default=default) == eresult

        assert data_list_obj.get('::', default=default) == eresult
        assert data_list_obj.get('::1', default=default) == eresult
        assert data_list_obj.get('0:3:1', default=default) == eresult
        assert data_list_obj.get('0:3:', default=default) == eresult
        assert data_list_obj.get('-3::', default=default) == eresult
        assert data_list_obj.get('-3::1', default=default) == eresult

        eresult1 = [
            expected_result.index0,
            expected_result.index2
        ]
        assert data_list_obj.get('0:3:2', default=default) == eresult1
        assert data_list_obj.get('0::2', default=default) == eresult1

        eresult2 = [
            expected_result.index0
        ]
        assert data_list_obj.get('0:3:3', default=default) == eresult2
        assert data_list_obj.get('0::3', default=default) == eresult2

        with pytest.raises(TypeError):
            data_list_obj.get(':::', default=default, on_exception=True)

        with pytest.raises(TypeError):
            data_list_obj.get('0:3:1:', default=default, on_exception=True)


@pytest.fixture
def another_dict_data():
    obj = {
        "widget": {
            "debug": "on",
            "window": {
                "title": "ABC Widget",
                "name": "window abc",
                "width": 500,
                "height": 500
            },
            "image": {
                "src": "Images/abc.png",
                "name": "image abc",
                "width": 100,
                "height": 100,
                "alignment": "center"
            },
            "text": {
                "data": "Click ABC",
                "size": 36,
                "style": "bold",
                "name": "text abc",
                "width": 300,
                "height": 20,
                "alignment": "center",
            }
        }
    }
    yield obj


@pytest.fixture
def another_list_data():
    obj = [
        {
            "widget": {
                "debug": "on",
                "window": {
                    "title": "ABC Widget",
                    "name": "window abc",
                    "width": 500,
                    "height": 500
                },
                "image": {
                    "src": "Images/abc.png",
                    "name": "image abc",
                    "width": 100,
                    "height": 100,
                    "alignment": "center"
                },
                "text": {
                    "data": "Click ABC",
                    "size": 36,
                    "style": "bold",
                    "name": "text abc",
                    "width": 300,
                    "height": 20,
                    "alignment": "center",
                }
            }
        },
        {
            "widget": {
                "debug": "off",
                "window": {
                    "title": "XYZ Widget",
                    "name": "window xyz",
                    "width": 599,
                    "height": 599
                },
                "image": {
                    "src": "Images/xyz.png",
                    "name": "image xyz",
                    "width": 199,
                    "height": 199,
                    "alignment": "right"
                },
                "text": {
                    "data": "Click XYZ",
                    "size": 96,
                    "style": "normal",
                    "name": "text abc",
                    "width": 399,
                    "height": 29,
                    "alignment": "left",
                }
            }
        }
    ]
    yield obj


class TestQueryingDLQuery:
    @pytest.mark.parametrize(
        "lookup,select_statement,expected_result",
        [
            ('name=_iwildcard(*abc*)', 'src', [{'src': 'Images/abc.png'}]),
            ('alignment=center', 'name where width eq 300', [{'name': 'text abc'}]),
            ('alignment', 'name where width eq 300 and_ data match (?i).+ abc', [{'name': 'text abc'}])
        ]
    )
    def test_find_a_lookup_and_validate_dict_obj(
        self, another_dict_data, lookup, select_statement, expected_result
    ):
        dl_obj = DLQuery(another_dict_data)
        result = dl_obj.find(lookup=lookup, select=select_statement)
        assert result == expected_result

    @pytest.mark.parametrize(
        "lookup,select_statement,expected_result",
        [
            (
                'debug=off',            # lookup
                'window',               # select statement
                [                       # expected_result
                    {
                        "window": {
                            "title": "XYZ Widget",
                            "name": "window xyz",
                            "width": 599,
                            "height": 599
                        }
                    }

                ]
            )
        ]
    )
    def test_find_a_lookup_and_validate_list_obj(
        self, another_list_data, lookup, select_statement, expected_result
    ):
        dl_obj = DLQuery(another_list_data)
        result = dl_obj.find(lookup=lookup, select=select_statement)
        assert result == expected_result

    @pytest.mark.parametrize(
        "lookup_a,select_a,lookup_b,select_b,expected_result",
        [
            (
                'name',                                             # lookup1
                'select name, width, height where height le 500',   # select1
                'name=_iwildcard(*xyz)',                            # lookup2
                '',                                                 # select2
                ["image xyz"]               # expected_result
            )
        ]
    )
    def test_find_double_querying(
        self, another_list_data, lookup_a, select_a,
        lookup_b, select_b, expected_result
    ):
        dl_obj = DLQuery(another_list_data)
        result_a = dl_obj.find(lookup=lookup_a, select=select_a)
        result_b = dl_obj.find(node=result_a, lookup=lookup_b, select=select_b)
        assert result_b == expected_result
