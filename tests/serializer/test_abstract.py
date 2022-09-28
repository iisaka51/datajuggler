import sys
import pytest

from datajuggler import serializer as io

class TestClass:
    def test_abstract_decode(self):
        s = io.AbstractSerializer()
        with pytest.raises(NotImplementedError) as e:
            s.decode("")
        assert str(e.value) == ""

    def test_abstract_encode(self):
        s = io.AbstractSerializer()
        with pytest.raises(NotImplementedError) as e:
            s.encode("")
        assert str(e.value) == ""

    def test_abstract_inheritance(self):
        class ConcreateSerializer(io.AbstractSerializer):
            @classmethod
            def encode(d):
                return ""

        s = ConcreateSerializer()
        with pytest.raises(NotImplementedError) as e:
            s.decode("")
        assert str(e.value) == ""
