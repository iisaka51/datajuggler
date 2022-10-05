import datetime
import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io

data = {'date': datetime.datetime(1985, 4, 3, 0, 0)}
pickled = ( 'gAJ9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZ'
            'QpxAmNfY29kZWNzCmVuY29kZQpxA1gLAAAAB8OBBAMAAA'
            'AAAABxBFgGAAAAbGF0aW4xcQWGcQZScQeFcQhScQlzLg==' )

class TestClass:
    def test_pickle_decode(self):
        s = io.PickleSerializer()
        result = s.decode(pickled)
        assert result == data

    def test_pickle_encode(self):
        s = io.PickleSerializer()
        result = s.encode(data)
        assert result == pickled


    def test_pickle_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = aDict(filepath, format='pickle')
        assert d == expect

    def test_pickle_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = aDict(filepath)
        assert d == expect

    def test_pickle_adict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.pickle'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.pickle\n"
                   "Incorrect padding" )
        with pytest.raises(ValueError) as e:
            d = aDict(filepath, format='pickle')
        assert str(e.value) == expect

    def test_pickle_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = uDict(filepath, format='pickle')
        assert d == expect

    def test_pickle_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.pickle'
        expect = aDict(data)
        d = uDict(filepath)
        assert d == expect

    def test_pickle_udict_decode_case03(self):
        filepath = 'tests/serializer/data/invalid-content.pickle'
        expect = ( "Invalid data or url or filepath argument: "
                   "tests/serializer/data/invalid-content.pickle\n"
                   "Incorrect padding" )
        with pytest.raises(ValueError) as e:
            d = uDict(filepath, format='pickle')
        assert str(e.value) == expect
