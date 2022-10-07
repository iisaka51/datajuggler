import datetime
import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io

plist_data = io.read_file('tests/serializer/data/valid-content.plist')
data = {
    'aDate': datetime.datetime(1985, 4, 3, 23, 55),
    'aDict': {'aFalseValue': False,
    'aThirdString': 'Mässig, Maß',
    'aTrueValue': True,
    'anotherString': '<hello & hi there!>'},
    'aFloat': 0.1,
    'aList': ['A', 'B', 12, 32.1, [1, 2, 3]],
    'aString': 'Doodah',
    'anInt': 728,
    'someData': b'<binary gunk>',
    'someMoreData': ( b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>'
                      b'<lots of binary gunk>' )
    }

plist_xml = (
  '<?xml version="1.0" encoding="UTF-8"?>\n'
  '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
  '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
  '<plist version="1.0">\n'
  '<dict>\n'
  '\t<key>aDate</key>\n'
  '\t<date>1985-04-03T23:55:00Z</date>\n'
  '\t<key>aDict</key>\n'
  '\t<dict>\n'
  '\t\t<key>aFalseValue</key>\n'
  '\t\t<false/>\n'
  '\t\t<key>aThirdString</key>\n'
  '\t\t<string>Mässig, Maß</string>\n'
  '\t\t<key>aTrueValue</key>\n'
  '\t\t<true/>\n\t\t<key>anotherString</key>\n'
  '\t\t<string>&lt;hello &amp; hi there!&gt;</string>\n'
  '\t</dict>\n'
  '\t<key>aFloat</key>\n'
  '\t<real>0.1</real>\n'
  '\t<key>aList</key>\n'
  '\t<array>\n'
  '\t\t<string>A</string>\n'
  '\t\t<string>B</string>\n'
  '\t\t<integer>12</integer>\n'
  '\t\t<real>32.1</real>\n'
  '\t\t<array>\n'
  '\t\t\t<integer>1</integer>\n'
  '\t\t\t<integer>2</integer>\n'
  '\t\t\t<integer>3</integer>\n'
  '\t\t</array>\n'
  '\t</array>\n'
  '\t<key>aString</key>\n'
  '\t<string>Doodah</string>\n'
  '\t<key>anInt</key>\n'
  '\t<integer>728</integer>\n'
  '\t<key>someData</key>\n'
  '\t<data>\n\tPGJpbmFyeSBndW5rPg==\n'
  '\t</data>\n\t<key>someMoreData</key>\n'
  '\t<data>\n'
  '\tPGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2Yg\n'
  '\tYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1\n'
  '\tbms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMg\n'
  '\tb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5\n'
  '\tIGd1bms+\n\t</data>\n</dict>\n</plist>\n' )

class TestClass:
    def test_plist_decode(self):
        s = io.PListSerializer()
        result = s.decode(plist_data)
        assert result == data

    def test_plist_encode(self):
        s = io.PListSerializer()
        result = s.encode(data)
        assert result == plist_xml


    def test_plist_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.plist'
        expect = aDict(data)
        d = aDict(filepath, format='plist')
        assert d == expect

    def test_plist_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.plist'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_plist_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.plist'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.plist\n"
                   "syntax error: line 1, column 0" )
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='plist')
        assert str(e.value) == expect

    def test_plist_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.plist'
        expect = aDict(data)
        d = uDict(filepath, format='plist')
        assert d == expect

    def test_plist_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.plist'
        expect = aDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_plist_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.plist'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.plist\n"
                   "syntax error: line 1, column 0" )
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='plist')
        assert str(e.value) == expect
