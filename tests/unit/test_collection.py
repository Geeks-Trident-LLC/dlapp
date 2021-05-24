from dlquery.collection import Element


class TestElement:
    def test_case1(self):
        data = dict(
            level1a=dict(
                level2a=dict(
                    level3a='level1a-level2a-level3a',
                    level3b='level1a-level2a-level3b'
                ),
                level2b=dict(
                    level3a='level1a-level2b-level3a',
                    level3b='level1a-level2b-level3b'
                ),
                level2c='level1a-level2c',
            ),
            level1b=dict(
                level2a='level1b-level2a',
                level2b='level1b-level2b'
            ),
            level1c='level1c',
        )
        # import pdb; pdb.set_trace()
        obj = Element(data)
        print(obj.has_children)
