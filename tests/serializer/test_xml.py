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
    def test_xml_decode_case01(self):
        expect = {'root': {
                     'April:int': 4,
                     'February:int': 2,
                     'January:int': 1,
                     'March:int': 3}  }

        s = io.XMLSerializer()
        result = s.decode(xml_str)
        assert result == expect

    def test_xml_decode_case01(self):
        expect = {'root':
                  {'April:int': 4,
                   'February:int': 2,
                   'January:int': 1,
                   'March:int': 3}}

        s = io.XMLSerializer()
        result = s.decode(xml_str, postprocessor=postprocessor)
        assert result == expect

    def test_xml_encode(self):
        s = io.XMLSerializer()
        result = s.encode(data)
        assert result == xml_str


