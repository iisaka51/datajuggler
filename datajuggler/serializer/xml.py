# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)

try:
    import xmltodict
    xml_enable = True
except ImportError:  # pragma: no cover
    xml_enable = False
    xmltodict = AbstractSerializer()

class XMLSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='xml', package='xmltodict', enable=xml_enable)

    def loads(self, s, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        kwargs.setdefault("dict_constructor", dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def dumps(self, d, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        if len(list(d.keys())) != 1:
            raise ValueError('dict must have exactly one root.')
        data = xmltodict.unparse(d, **kwargs)
        return data

register_serializer(XMLSerializer)
