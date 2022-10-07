from pathlib import Path

import pytest
from datajuggler import serializer as io

URL = ( 'https://raw.githubusercontent.com/iisaka51/datajuggler'
        '/main/requirements.txt' )
filepath = 'tests/serializer/data/valid-content.csv'

expect_csv = ( 'id,name,age,height,weight\n'
           '1,Alice,20,62,120.6\n'
           '2,Freddie,21,74,190.6\n'
           '3,Bob,17,68,120.0\n'
           '4,François,32,75,110.05' )

expect_txt = 'multimethod>=1.8\n'

class TestClass:
    def test_read_file_case01(self):
        data = io.read_file(filepath)
        assert data == expect_csv

    def test_read_file_case02(self):
        data = io.read_file(Path(filepath))
        assert data == expect_csv

    def test_read_url_case01(self):
        data = io.read_url(URL)
        assert data == expect_txt

    def test_read_contents_case01(self):
        data = io.read_contents(filepath)
        assert data == expect_csv

    def test_read_contents_case02(self):
        data = io.read_contents(URL)
        assert data == expect_txt
