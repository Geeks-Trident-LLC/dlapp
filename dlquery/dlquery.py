"""Module containing the logic for querying dictionary or list object."""
import re
from dlquery.argumenthelper import validate_argument_type
from dlquery.argumenthelper import validate_argument_choice


class DLQueryError(Exception):
    """Use to capture error for DLQuery instance"""


class DLQueryDataTypeError(DLQueryError):
    """Use to capture error of unsupported query data type."""


class DLQuery:
    """This is a class for querying dictionary or list object.

    Attributes:
        data (list or dict): list or dictionary instance.
       dtype (str): list|dict.  Default is an empty string.

    Methods:
        TBA

    Exception:
        TBA
    """

    def __init__(self, data, dtype=''):
        validate_argument_type(list, dict, data=data)
        validate_argument_choice(dtype=[dtype, ('list', 'dict')])
        self.data = data
        self.dtype = dtype

    ############################################################################
    # properties
    ############################################################################
    @property
    def is_dict(self):
        """Check if data of DLQuery is a dictionary data."""
        return isinstance(self.data, dict)

    @property
    def is_list(self):
        """Check if data of DLQuery is a list or tuple data."""
        return isinstance(self.data, (list, tuple))

    ############################################################################
    # public methods
    ############################################################################
    def get(self, lookup, is_regex=False, default=None):
        try:
            if self.dtype == 'list':
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
