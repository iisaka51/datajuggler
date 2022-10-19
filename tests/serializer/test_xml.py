import sys
import pytest

from datajuggler import serializer as io

data = { 'root': {
              'January': 1,
              'February': 2,
              'March': 3,
              'April': 4 } }

xml_str_pretty = """<?xml version="1.0" encoding="utf-8"?>
<root>
	<January>1</January>
	<February>2</February>
	<March>3</March>
	<April>4</April>
</data>
"""

xml_str = ( '<?xml version="1.0" encoding="utf-8"?>\n'
              '<root><January>1</January>'
              '<February>2</February>'
              '<March>3</March>'
              '<April>4</April>'
            '</root>' )

def postprocessor(path, key, value):
    try:
        return key + ':int', int(value)
    except (ValueError, TypeError):
        return key, value

class TestClass:
    def test_xml_loads_case01(self):
        expect = {'root': {
                     'April': '4',
                     'February': '2',
                     'January': '1',
                     'March': '3'} }

        result = io.loads(xml_str, format='xml')
        assert result == expect

    def test_xml_loads_case02(self):
        expect = {'root':
                  {'April:int': 4,
                   'February:int': 2,
                   'January:int': 1,
                   'March:int': 3}}

        result = io.loads(xml_str, postprocessor=postprocessor, format='xml')
        assert result == expect

    def test_xml_dumps(self):
        result = io.dumps(data, format='xml')
        assert result == xml_str


