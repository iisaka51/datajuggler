import sys
import base64
import pytest

from datajuggler import uDict, aDict
from datajuggler import serializer as io

list_of_dict = [
 {'age':'20', 'height':'62', 'id':'1', 'name':'Alice', 'weight':'120.6'},
 {'age':'21', 'height':'74', 'id':'2', 'name':'Freddie', 'weight':'190.6'},
 {'age':'17', 'height':'68', 'id':'3', 'name':'Bob', 'weight':'120.0'},
 {'age':'32', 'height':'75', 'id':'4', 'name':'François', 'weight':'110.05'}
]

csv_str = ( 'age,height,id,name,weight\n'
            '20,62,1,Alice,120.6\n'
            '21,74,2,Freddie,190.6\n'
            '17,68,3,Bob,120.0\n'
           '32,75,4,François,110.05\n' )

class TestClass:
    def test_csv_decode(self):
        s = io.CSVSerializer()
        result = s.decode(csv_str)
        assert result == list_of_dict

    def test_csv_encode(self):
        s = io.CSVSerializer()
        result = s.encode(list_of_dict)
        assert result == csv_str

    def test_csv_decode_adict_case01(self):
        expect  = {'value': [
 {'age':'20', 'height':'62', 'id':'1', 'name':'Alice', 'weight':'120.6'},
 {'age':'21', 'height':'74', 'id':'2', 'name':'Freddie', 'weight':'190.6'},
 {'age':'17', 'height':'68', 'id':'3', 'name':'Bob', 'weight':'120.0'},
 {'age':'32', 'height':'75', 'id':'4', 'name':'François', 'weight':'110.05'}
        ] }
        d = aDict(csv_str, format='csv' )
        expect = aDict({'values': list_of_dict })
        assert d == expect

