import sys
import base64
import pytest

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

