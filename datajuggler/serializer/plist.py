# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer

try:
    import plistlib

    class PListSerializer(AbstractSerializer):
        """
        This class describes a p list serializer.
        https://docs.python.org/3/library/plistlib.html
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            kwargs.setdefault("fmt", plistlib.FMT_XML)
            encoding = kwargs.pop("encoding", "utf-8")
            return plistlib.loads(s.encode(encoding), **kwargs)

        def encode(self, d, **kwargs):
            encoding = kwargs.pop("encoding", "utf-8")
            return plistlib.dumps(d, **kwargs).decode(encoding)

except ImportError:

    class PListSerializer(AbstractSerializer):
        """
        This class describes a p list serializer.
        https://docs.python.org/3/library/plistlib.html
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            raise NotImplementedError('You should install plistlib.')

        def encode(self, d, **kwargs):
            raise NotImplementedError('You should install plistlib.')
