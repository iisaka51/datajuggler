import base64
import pytest

from datajuggler import aDict, uDict
from datajuggler import serializer as io

msg = 'Python-benedict is greate job.'
base64_msg = base64.b64encode(msg.encode('ascii'))

class TestClass:
    def test_base64_decode(self):
        s = io.Base64Serializer()
        result = s.decode(base64_msg)
        assert result == msg

    def test_base64_encode(self):
        s = io.Base64Serializer()
        result = s.encode(msg)
        assert result == base64_msg.decode()

    def test_base64_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = aDict({'a': 1, 'b': 2, 'c': 3})
        d = aDict(filepath, format='base64')
        assert d == expect

    def test_base64_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = aDict({'a': 1, 'b': 2, 'c': 3})
        d = aDict(filepath)
        assert d == expect

    def test_base64_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = uDict({'a': 1, 'b': 2, 'c': 3})
        d = uDict(filepath, format='base64')
        assert d == expect

    def test_base64_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = uDict({'a': 1, 'b': 2, 'c': 3})
        d = uDict(filepath)
        assert d == expect


