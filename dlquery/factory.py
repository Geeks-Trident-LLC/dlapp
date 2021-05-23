"""Module containing the logic for creating dlquery."""

import yaml
import json
from dlquery import DLQuery
from dlquery.utils import get_reference_dtype


def create_from_json_file(filename, **kwargs):
    """Create a dlquery instance from JSON filename.
    Parameters:
        filename (string): JSON filename.
        kwargs (dict): keyword arguments which would use for JSON instantiation.
    """
    from io import IOBase
    if isinstance(filename, IOBase):
        obj = json.load(filename, **kwargs)
    else:
        with open(filename) as stream:
            obj = json.load(stream, **kwargs)

    dtype = get_reference_dtype(obj)
    query_obj = DLQuery(obj, dtype=dtype)
    return query_obj


def create_from_json_data(data, **kwargs):
    """Create a dlquery instance from JSON data.
    Parameters:
        data (string): JSON data in string format.
        kwargs (dict): keyword arguments which would use for JSON instantiation.
    Return:
        DLQuery: a DLQuery instance.
    """
    obj = json.loads(data, **kwargs)
    dtype = get_reference_dtype(obj)
    query_obj = DLQuery(obj, dtype=dtype)
    return query_obj


def create_from_yaml_file(filename, loader=yaml.SafeLoader):
    """Create a dlquery instance from YAML file.
    Parameters:
        filename (string): a YAML file.
        loader (yaml.loader.Loader): a YAML loader.
    Return:
        DLQuery: a DLQuery instance.
    """
    with open(filename) as stream:
        obj = yaml.load(stream, Loader=loader)
        dtype = get_reference_dtype(obj)
        query_obj = DLQuery(obj, dtype=dtype)
        return query_obj


def create_from_yaml_data(data, loader=yaml.SafeLoader):
    """Create a dlquery instance from YAML data.
    Parameters:
        data (string): a YAML data in string format.
        loader (yaml.loader.Loader): a YAML loader.
    Return:
        DLQuery: a DLQuery instance.
    """
    obj = yaml.load(data, Loader=loader)
    dtype = get_reference_dtype(obj)
    query_obj = DLQuery(obj, dtype=dtype)
    return query_obj
