from pathlib import Path

import pytest
from datajuggler import serializer as io

BASE_URL = 'https://raw.githubusercontent.com/iisaka51/datajuggler/data'
URL = f'{BASE_URL}/tests/serializer/data/preamble.txt'

filepath = 'tests/serializer/data/valid-content.csv'

expect_csv = (
  'id,name,age,height,weight\n'
  '1,Alice,20,62,120.6\n'
  '2,Freddie,21,74,190.6\n'
  '3,Bob,17,68,120.0\n'
  '4,François,32,75,110.05'
)

preamble_txt = (
 'We the People of the United States, in Order to form a more perfect Union, '
 'establish Justice, insure domestic Tranquility, provide for the common '
 'defense, promote the general Welfare, and secure the Blessings of Liberty to '
 'ourselves and our Posterity, do ordain and establish this Constitution for '
 'the United States of America.\n'
)

class TestClass:
    def test_read_file_case01(self):
        data = io.read_file(filepath)
        assert data == expect_csv

    def test_read_file_case02(self):
        data = io.read_file(Path(filepath))
        assert data == expect_csv

    def test_read_url_case01(self):
        data = io.read_url(URL)
        assert data == preamble_txt

    def test_read_contents_case01(self):
        data = io.read_contents(filepath)
        assert data == expect_csv

    def test_read_contents_case02(self):
        data = io.read_contents(URL)
        assert data == preamble_txt

