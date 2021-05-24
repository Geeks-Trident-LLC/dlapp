"""Module containing the logic for querying dictionary or list object."""
import re
from dlquery.argumenthelper import validate_argument_type


class DLQueryError(Exception):
    """Use to capture error for DLQuery instance"""


class DLQueryDataTypeError(DLQueryError):
    """Use to capture error of unsupported query data type."""


class DLQuery:
    """This is a class for querying dictionary or list object.

    Attributes:
        data (list, tuple, or dict): list or dictionary instance.

    Methods:
        TBA

    Exception:
        TypeError
    """

    def __init__(self, data):
        validate_argument_type(list, tuple, dict, data=data)
        self.data = data
        self._is_dict = None
        self._is_list = None

    ############################################################################
    # Special methods
    ############################################################################
    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        if self.is_dict:
            return iter(self.data.keys())
        elif self.is_list:
            return iter(range(len(self.data)))
        else:
            fmt = '{!r} object is not iterable.'
            msg = fmt.format(type(self).__name__)
            raise TypeError(msg)

    ############################################################################
    # properties
    ############################################################################
    @property
    def is_dict(self):
        """Check if data of DLQuery is a dictionary data."""
        if self._is_dict is None:
            self._is_dict = isinstance(self.data, dict)
        return self._is_dict

    @property
    def is_list(self):
        """Check if data of DLQuery is a list or tuple data."""
        if self._is_list is None:
            self._is_list = isinstance(self.data, (list, tuple))
        return self._is_list

    ############################################################################
    # public methods
    ############################################################################
    def get(self, lookup, is_regex=False, default=None):
        try:
            if self.is_list:
                if isinstance(lookup, int):
                    return self.data[lookup]
                elif isinstance(lookup, str):
                    if lookup.isdigit():
                        return self.data[int(lookup)]
                    else:
                        count = lookup.count(':')
                        if count == 1:
                            i, j = [k.strip() for k in lookup.split(':')]
                            if i.isdigit() and j.isdigit():
                                return self.data[int(i):int(j)]
                            else:
                                # display warning
                                return default
                        elif count == 2:
                            i, j, k = [k.strip() for k in lookup.split(':')]
                            if i.isdigit() and j.isdigit() and k.isdigit():
                                return self.data[int(i):int(j):int(k)]
                            else:
                                # display warning
                                return default
                        else:
                            # print warning
                            return default
                else:
                    # print warning
                    return True
            else:
                if is_regex:
                    result = []
                    for key, value in self.data.items():
                        if re.match(lookup, key):
                            result.append(self.data[key])
                    return result
                else:
                    return self.data[lookup]
        except Exception as ex:     # noqa
            return default
