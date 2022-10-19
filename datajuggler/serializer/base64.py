# -*- coding: utf-8 -*-

import base64
from urllib.parse import unquote

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.validator import TypeValidator as _type

_Encodable_SUBFORMAT = [ 'yaml_custom' ]
_NotAllowBytesObject_SUBFORMAT = ['json']

class Base64Serializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format=['base64', 'b64'])

    def loads(self, s, **kwargs):
        """base64 encoder
        if set 'encoding', encoding as string.
        if set 'subformat', first decoding base64 then decoding subformat
        """
        def _decode(s, **kwargs):
            def _fix_url_encoding_and_padding(s):
                s = unquote(s)     # fix urlencoded chars
                m = len(s) % 4     # fix padding
                if m != 0:
                    s += "=" * (4 - m)
                return s

            value = _fix_url_encoding_and_padding(s)
            value = base64.b64decode(value)
            return value


        serializer, subformat, encoding = self.parse_kwargs(**kwargs)
        del kwargs['subformat']
        value = _decode(s)
        if serializer:
            if subformat in _Encodable_SUBFORMAT:
                kwargs.setdefault('encoding', encoding)
            value = serializer.loads(value, **kwargs)
        return value

    def dumps(self, d, **kwargs):
        """base64 encoder
        if set 'encoding', encoding as string.
        if set 'subformat', first encoding subformat then encoding base64
        """
        def _encode(d, encoding, **kwargs):
            value = d
            encoding = kwargs.pop("encoding", "utf-8")
            if encoding and _type.is_str(value):
                value = value.encode(encoding)
            value = base64.b64encode(value)
            if _type.is_str(value) and encoding:
                value = value.encode(encoding)
            return value

        serializer, subformat, encoding = self.parse_kwargs(**kwargs)
        del kwargs['subformat']
        if serializer:
            if subformat in _NotAllowBytesObject_SUBFORMAT:
                if encoding and _type.is_bytes(d):
                    d = d.decode(encoding)
            if subformat in _Encodable_SUBFORMAT:
                kwargs.setdefault('encoding', encoding)
            value = serializer.dumps(d, **kwargs)
        else:
            value = d
        # value = base64.b64encode(value)
        value = _encode(value, encoding)
        return value


register_serializer(Base64Serializer)

