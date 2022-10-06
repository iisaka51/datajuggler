# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer

try:
    import xmltodict

    class XMLSerializer(AbstractSerializer):
        """
        This class describes a xml serializer.
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            kwargs.setdefault("dict_constructor", dict)
            data = xmltodict.parse(s, **kwargs)
            return data

        def encode(self, d, **kwargs):
            if len(list(d.keys())) != 1:
                raise ValueError('dict must have exactly one root.')
            data = xmltodict.unparse(d, **kwargs)
            return data

except ImportError:

    class XMLSerializer(AbstractSerializer):
        """
        This class describes a xml serializer.
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            raise NotImplementedError("You should install 'xmltodict'.")

        def encode(self, d, **kwargs):
            raise NotImplementedError("You should install 'xmltodict'.")
