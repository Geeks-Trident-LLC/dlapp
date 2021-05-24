"""Module containing the logic for the collection of data structure."""

import yaml
import json
# import re
from dlquery.argumenthelper import validate_argument_type


class ListError(Exception):
    """Use to capture error for List instance"""


class ListIndexError(ListError):
    """Use to capture error for List instance"""


class List(list):
    """This is a class for List Collection.

    Properties:
        is_empty (boolean): a check point to tell an empty list or not.
        first (anything): return a first element of a list
        last (anything): return a last element of a list
        total (int): total element in list

    Exception:
        ListError
    """
    @property
    def is_empty(self):
        """Check an empty list."""
        return self.total == 0

    @property
    def first(self):
        """Get a first element of list if list is not empty"""
        if not self.is_empty:
            return self[0]

        raise ListIndexError('Can not get a first element of an empty list.')

    @property
    def last(self):
        """Get a last element of list if list is not empty"""
        if not self.is_empty:
            return self[-1]
        raise ListIndexError('Can not get last element of an empty list.')

    @property
    def total(self):
        """Get a size of list"""
        return len(self)


class ResultError(Exception):
    """Use to capture error for Result instance."""


class Result:
    """The Result Class to store data.

    Attributes:
        data (anything): the data.
        parent (Result): keyword arguments.

    Properties:
        has_parent -> boolean

    Methods:
        update_parent(parent: Result) -> None

    Exception:
        ResultError
    """
    def __init__(self, data, parent=None):
        self.data = data
        self.update_parent(parent)

    def update_parent(self, parent):
        """Update parent to Result

            Parameters:
                parent (Result): a Result instance.

            Return:
                None
        """
        if parent is None or isinstance(parent, self.__class__):
            self.parent = parent
        else:
            msg = 'parent argument must be Result instance or None.'
            raise ResultError(msg)

    @property
    def has_parent(self):
        """Return True if Result has parent."""
        return isinstance(self.parent, Result)


class Element(Result):
    def __init__(self, data, index='', parent=None):
        super().__init__(data, parent=parent)
        self.index = index
        self._build(data)

    def __iter__(self):
        if self.type == 'dict':
            return iter(self.data.keys())
        elif self.type == 'list':
            return iter(range(len(self.data)))
        else:
            fmt = '{!r} object is not iterable.'
            msg = fmt.format(type(self).__name__)
            raise TypeError(msg)

    def __getitem__(self, index):
        if self.type not in ['dict', 'list']:
            fmt = '{!r} object is not subscriptable.'
            msg = fmt.format(type(self).__name__)
            raise TypeError(msg)
        result = self.data[index]
        return result

    def _build(self, data):
        self.children = None
        self.value = None
        if isinstance(data, dict):
            self.type = 'dict'
            lst = List()
            for index, val in data.items():
                elm = Element(val, index=index, parent=self)
                lst.append(elm)
            self.children = lst or None
        elif isinstance(data, (list, tuple, set)):
            self.type = 'list'
            lst = List()
            for i, item in enumerate(data):
                index = '__index__{}'.format(i)
                elm = Element(item, index=index, parent=self)
                lst.append(elm)
            self.children = lst or None
        elif isinstance(data, (int, float, bool, str)) or data is None:
            self.type = type(data).__name__
            self.value = data
        else:
            self.type = 'object'
            self.value = data

    @property
    def has_children(self):
        """Return True if an element has children."""
        return bool(self.children)

    @property
    def is_element(self):
        """Return True if an element has children."""
        return self.has_children

    @property
    def is_leaf(self):
        """Return True if an element doesnt have children."""
        return not self.has_children

    @property
    def is_scalar(self):
        """Return True if an element is a scalar type."""
        return isinstance(self.data, (int, float, bool, str, None))

    def find(self, lookup, i=False):
        """recursively search a lookup."""
        # lookup = re.sub(r'([*?])', r'.\1', lookup)
        # lookup = lookup.replace('[!', '[^')
        # lookup+= r'\s*$'
        # items = re.split(' +', lookup.strip())
        raise NotImplementedError('TODO - Need to implement Element.find')


class ObjectDict(dict):
    """The ObjectDict can retrieve value of key as attribute style."""
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    ############################################################################
    # Special methods
    ############################################################################
    def __getattribute__(self, attr):
        try:
            value = super().__getattribute__(attr)
            return value
        except Exception as ex:
            if attr in self:
                return self[attr]
            else:
                raise ex

    def __setitem__(self, key, value):
        new_value = self._build(value)
        super().__setitem__(key, new_value)

    def __setattr__(self, attr, value):
        new_value = self._build(value)
        if attr in self:
            self[attr] = new_value
        else:
            super().__setattr__(attr, new_value)

    ############################################################################
    # Private methods
    ############################################################################
    def _build(self, value, forward=True):
        """The function to recursively build a ObjectDict instance
        when the value is the dict instance.

        Parameters:
            value (anything): The value to recursively build a ObjectDict
                    instance when value is the dict instance.
            forward (boolean): set flag to convert dict instance to ObjectDict
                    instance or vice versa.  Default is True.
        Returns:
            anything: the value or a new value.
        """
        if isinstance(value, (dict, list, set, tuple)):
            if isinstance(value, ObjectDict):
                if forward:
                    return value
                else:
                    result = dict([i, self._build(j, forward=forward)] for i, j in value.items())
                    return result
            elif isinstance(value, dict):
                lst = [[i, self._build(j, forward=forward)] for i, j in value.items()]
                if forward:
                    result = self.__class__(lst)
                    return result
                else:
                    result = dict(lst)
                    return result
            elif isinstance(value, list):
                lst = [self._build(item, forward=forward) for item in value]
                return lst
            elif isinstance(value, set):
                lst = [self._build(item, forward=forward) for item in value]
                return set(lst)
            else:
                tuple_obj = (self._build(item, forward=forward) for item in value)
                return tuple_obj
        else:
            return value

    ############################################################################
    # class methods
    ############################################################################
    @classmethod
    def create_from_json_file(cls, filename, **kwargs):
        """Create a ObjectDict instance from JSON file.
        Parameters:
            filename (string): YAML file.
            kwargs (dict): the keyword arguments.
        """
        from io import IOBase
        if isinstance(filename, IOBase):
            obj = json.load(filename, **kwargs)
        else:
            with open(filename) as stream:
                obj = json.load(stream, **kwargs)

        obj_dict = ObjectDict(obj)
        return obj_dict

    @classmethod
    def create_from_json_data(cls, data, **kwargs):
        obj = json.loads(data, **kwargs)
        obj_dict = ObjectDict(obj)
        return obj_dict

    @classmethod
    def create_from_yaml_file(cls, filename, loader=yaml.SafeLoader):
        """Create a ObjectDict instance from YAML file.
        Parameters:
            filename (string): YAML file.
            loader (yaml.loader.Loader): YAML loader.
        """
        from io import IOBase
        if isinstance(filename, IOBase):
            obj = yaml.load(filename, Loader=loader)
        else:
            with open(filename) as stream:
                obj = yaml.load(stream, Loader=loader)

        obj_dict = ObjectDict(obj)
        return obj_dict

    @classmethod
    def create_from_yaml_data(cls, data, loader=yaml.SafeLoader):
        """Create a ObjectDict instance from YAML data.
        Parameters:
            data (string): YAML data.
            loader (yaml.loader.Loader): YAML loader.
        """
        obj = yaml.load(data, Loader=loader)
        obj_dict = ObjectDict(obj)
        return obj_dict

    ############################################################################
    # public methods
    ############################################################################
    def update(self, *args, **kwargs):
        """Update data to ObjectDict."""
        obj = dict(*args, **kwargs)
        new_obj = dict()
        for key, value in obj.items():
            new_obj[key] = self._build(value)
        super().update(new_obj)

    def deep_apply_attributes(self, node=None, **kwargs):
        """Recursively apply attributes to ObjectDict instance.

        Parameters:
            node (ObjectDict): a ObjectDict instance
            kwargs (dict):
        """

        def assign(node_, **kwargs_):
            for key, val in kwargs_.items():
                setattr(node_, key, val)

        def apply(node_, **kwargs_):
            if isinstance(node_, (dict, list, set, tuple)):
                if isinstance(node_, dict):
                    if isinstance(node_, self.__class__):
                        assign(node_, **kwargs_)
                    for value in node_.values():
                        apply(value, **kwargs_)
                else:
                    for item in node_:
                        apply(item, **kwargs_)

        node = self if node is None else node
        validate_argument_type(self.__class__, node=node)
        apply(node, **kwargs)

    def to_dict(self, data=None):
        """Convert a given data to native dictionary

        Parameters:
            data (ObjectDict): a dynamic dictionary instance.
                if data is None, it will convert current instance to dict.

        Return:
            dict: dictionary
        """
        if data is None:
            data = dict(self)

        validate_argument_type(dict, data=data)
        result = self._build(data, forward=False)
        return result

    todict = to_dict
