from dlquery import create_from_yaml_file
from dlquery import create_from_yaml_data
from dlquery import create_from_json_file
from dlquery import create_from_json_data
from os import path

test_path = path.dirname(__file__)


class TestDynamicDict:
    def test_creating_dlquery_from_yaml_file(self):
        """Test creating a dlquery instance from YAML file."""
        filename = path.join(test_path, 'data/sample.yaml')
        query_obj = create_from_yaml_file(filename)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_yaml_data(self):
        """Test creating a dlquery instance from YAML data."""
        data = '''{"a": "Apricot", "b": "Banana"}'''
        query_obj = create_from_yaml_data(data)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_json_file(self):
        """Test creating a dlquery instance from JSON file."""
        filename = path.join(test_path, 'data/sample.json')
        # filename = self.json_filename
        query_obj = create_from_json_file(filename)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_json_data(self):
        """Test creating a dlquery instance from JSON data."""
        data = '''{"a": "Apricot", "b": "Banana"}'''
        query_obj = create_from_json_data(data)
        assert query_obj.get('a') == 'Apricot'
