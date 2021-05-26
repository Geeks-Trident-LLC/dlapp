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
    return ExpectedResult()


@pytest.fixture
def dict_data():
    obj = {'a': 'Apricot', 'b': 'Banana'}
    return obj


@pytest.fixture
def list_data(dict_data):
    obj = [2021, 'Hello dlquery', dict(dict_data)]
    return obj


@pytest.fixture
def dict_other_data():
    obj = {'a': 'Apricot', 'c': 'Cherry'}
    return obj


@pytest.fixture
def list_other_data(dict_other_data):
    obj = [2021, 'Hello python', dict(dict_other_data)]
    return obj


@pytest.fixture
def empty_dldata():
    empty_dict, empty_list = dict(), list()
    obj1, obj2 = DLQuery(empty_dict), DLQuery(empty_list)
    return obj1, obj2


@pytest.fixture
def dldata(dict_data, list_data):
    obj1, obj2 = DLQuery(dict_data), DLQuery(list_data)
    return obj1, obj2


@pytest.fixture
def other_dldata(dict_other_data, list_other_data):
    obj1, obj2 = DLQuery(dict_other_data), DLQuery(list_other_data)
    return obj1, obj2


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

    def test_iter(self, dldata, expected_result):

        data_dict_obj, data_list_obj = dldata

        for key in data_dict_obj:
            print(key)

        for item in data_list_obj:
            print(item)

        assert expected_result.key1 in data_dict_obj
        assert expected_result.key2 in data_dict_obj

        assert expected_result.index0 in data_list_obj
        assert expected_result.index1 in data_list_obj
        assert expected_result.index2 in data_list_obj

        iter_obj = iter(data_dict_obj)
        result = next(iter_obj)
        assert result == expected_result.key1
        result = next(iter_obj)
        assert result == expected_result.key2

        iter_obj = iter(data_list_obj)
        result = next(iter_obj)
        assert result == expected_result.index0
        result = next(iter_obj)
        assert result == expected_result.index1
        result = next(iter_obj)
        assert result == expected_result.index2

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

    def test_keys_method(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        dict_keys = data_dict_obj.keys()
        result = iter(dict_keys)

        assert next(result) == expected_result.key1
        assert next(result) == expected_result.key2

        list_indices = data_list_obj.keys()
        result = iter(list_indices)

        assert next(result) == expected_result.zero
        assert next(result) == expected_result.one
        assert next(result) == expected_result.two

    def test_values_method(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        dict_values = data_dict_obj.values()
        result = iter(dict_values)

        assert next(result) == expected_result.value1
        assert next(result) == expected_result.value2

        list_items = data_list_obj.values()
        result = iter(list_items)

        assert next(result) == expected_result.index0
        assert next(result) == expected_result.index1
        assert next(result) == expected_result.index2

    def test_items_method(self, dldata, expected_result):
        data_dict_obj, data_list_obj = dldata

        dict_items = data_dict_obj.items()
        result = iter(dict_items)

        assert next(result) == (expected_result.key1, expected_result.value1)
        assert next(result) == (expected_result.key2, expected_result.value2)

        list_items = data_list_obj.items()
        result = iter(list_items)

        assert next(result) == (expected_result.zero, expected_result.index0)
        assert next(result) == (expected_result.one, expected_result.index1)
        assert next(result) == (expected_result.two, expected_result.index2)

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
        assert data_list_obj.get('::', default=default) == eresult
        assert data_list_obj.get('::1', default=default) == eresult
        assert data_list_obj.get('0:3:1', default=default) == eresult
        assert data_list_obj.get('0:3:', default=default) == eresult

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
