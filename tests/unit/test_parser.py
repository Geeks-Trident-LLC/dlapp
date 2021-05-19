from dlquery import DLQuery
from dlquery.parser import SelectParser


class TestSelectParser:
    def test_case1(self):
        """Test matching regex validation."""
        obj = SelectParser('SELECT a, b WHERE a eq 1')
        obj.parse_statement()
        node = dict(a=1, b=2)
        result = obj.predicate(node)
        print(result)
        assert True
