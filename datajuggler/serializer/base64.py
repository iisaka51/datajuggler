# -*- coding: utf-8 -*-

import base64
from urllib.parse import unquote

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.serializer.core import encode_by_format
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
        _ = kwargs.pop('subformat', None)
        value = _decode(s)
        if serializer:
            value = serializer.loads(value, **kwargs)
        return value

    def dumps(self, d, **kwargs):
        """base64 encoder
        if set 'encoding', encoding as string.
        if set 'subformat', first encoding subformat then encoding base64
        """
        def _b64encode(s, encoding):
            if encoding and _type.is_str(s):
                s = s.encode(encoding)
            s = base64.b64encode(s)
            if _type.is_str(s) and encoding:
                s = s.encode(encoding)
            return s

        serializer, subformat, encoding = self.parse_kwargs(**kwargs)
        _ = kwargs.pop('subformat', None)
        if serializer:
            d = encode_by_format(d, subformat)
            value = serializer.dumps(d, **kwargs)
        else:
            value = d

        value = _b64encode(value, encoding)
        return value


register_serializer(Base64Serializer)

