# DLQuery
DLQuery is the query utility for dictionary or list.

## Installation
```python
pip install dlquery
```

## Features
- support a simple wildcard characters ?, *, [], [!]
- support regex
- support custom keywords
- support SQL-like select statement
- support GUI application

## Usage

### Development
```python
>>> # test data
>>> lst_of_dict = [
...     { "title": "ABC Widget", "name": "abc", "width": 500},
...     { "title": "DEF Widget", "name": "def", "width": 300},
...     { "title": "MNP Widget", "name": "mnp", "width": 455},
...     { "title": "XYZ Widget", "name": "xyz", "width": 600}
... ]
>>>
>>> from dlquery import DLQuery
>>>
>>> query_obj = DLQuery(lst_of_dict)
>>>
>>> # find any value of title starting with A or X
>>> query_obj.find(lookup="title=_wildcard([AX]*)")
['ABC Widget', 'XYZ Widget']
>>>
>>> # find any data of title starting with A or X 
>>> # and select title, width where width lt 550
>>> query_obj.find(lookup="title=_wildcard([AX]*)", select="SELECT title, width WHERE width lt 550")
[{'title': 'ABC Widget', 'width': 500}]
>>>
>>>
>>>
>>> # assuming /path/sample.json file has the same structure data as lst_of_dict
>>> from dlquery import create_from_json_file
>>>
>>> query_obj = create_from_json_file('/path/sample.json')
>>>
>>> query_obj.find(lookup="title=_wildcard([AX]*)")
['ABC Widget', 'XYZ Widget']
>>>
>>> # to query json string data, use
>>> from dlquery import create_from_json_data
>>>
>>>
>>>
>>> # to query yaml file, use
>>> from dlquery import create_from_yaml_file
>>>
>>> # to query yaml string data, use
>>> from dlquery import create_from_yaml_data
>>>
>>>
>>>
>>> # to query csv file, use
>>> from dlquery import create_from_csv_file
>>>
>>> # to query csv string data, use
>>> from dlquery import create_from_yaml_file
```

### Console command line

Open DLQuery application
```bash
$ dlquery-gui                   # using python entry point
$ dlquery --gui                 # using console command line
$ python -m dlquery --gui       # using python module invocation
```

Search json, yaml, or csv file
```bash
$ # assuming that /path/sample.json has the same structure data as lst_of_dict
$ dlquery --filename=/path/sample.json --lookup="title=_wildcard([AX]*)"
['ABC Widget', 'XYZ Widget']
$
$ dlquery --filename=/path/sample.json --lookup="title=_wildcard([AX]*)" --select="SELECT title, width WHERE width lt 550"
[{'title': 'ABC Widget', 'width': 500}]
$
$ # the same syntax can apply for yaml, yml, or csv file. 
```

## Bugs/Requests
Please use the [GitHub issue tracker](https://github.com/Geeks-Trident-LLC/dlquery/issues) to submit bugs or request features.

## License
Copyright @ 2021 [Geeks Trident LLC](http://www.geekstrident.com).  All rights reserved.

