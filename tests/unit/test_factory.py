from dlapp import create_from_yaml_file
from dlapp import create_from_yaml_data
from dlapp import create_from_json_file
from dlapp import create_from_json_data
from dlapp import create_from_csv_file
from dlapp import create_from_csv_data
from os import path

test_path = path.dirname(__file__)


class TestDynamicDict:
    def test_creating_dlquery_from_yaml_file(self):
        """Test creating a dlapp instance from YAML file."""
        filename = path.join(test_path, 'data/sample.yaml')
        query_obj = create_from_yaml_file(filename)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_yaml_data(self):
        """Test creating a dlapp instance from YAML data."""
        data = '''{"a": "Apricot", "b": "Banana"}'''
        query_obj = create_from_yaml_data(data)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_json_file(self):
        """Test creating a dlapp instance from JSON file."""
        filename = path.join(test_path, 'data/sample.json')
        # filename = self.json_filename
        query_obj = create_from_json_file(filename)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_json_data(self):
        """Test creating a dlapp instance from JSON data."""
        data = '''{"a": "Apricot", "b": "Banana"}'''
        query_obj = create_from_json_data(data)
        assert query_obj.get('a') == 'Apricot'

    def test_creating_dlquery_from_csv_file(self):
        """Test creating a dlapp instance from CSV file."""
        filename = path.join(test_path, 'data/sample.csv')
        query_obj = create_from_csv_file(filename)
        result = query_obj.find(lookup='a=_iwildcard(Ap*)')
        assert result == ['Apple', 'Apricot']

        query_obj.find(lookup='a=_regex(Ap\\w+)', select='')
        assert result == ['Apple', 'Apricot']

        query_obj.find(lookup='a', select='where a match Ap\\w+')
        assert result == ['Apple', 'Apricot']

    def test_creating_dlquery_from_csv_data(self):
        """Test creating a dlapp instance from CSV data."""
        data = '''
            a,b,c
            Apple,Banana,Cherry
            Apricot,Boysenberry,Cantaloupe
            Avocado,Blueberry,Clementine
        '''
        data = '\n'.join(line.strip() for line in data.strip().splitlines())
        query_obj = create_from_csv_data(data)
        result = query_obj.find(lookup='b=_iregex(.+n.+)')
        assert result == ['Banana', 'Boysenberry']
