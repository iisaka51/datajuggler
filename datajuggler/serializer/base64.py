# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer
from datajuggler.validator import TypeValidator as _type

from urllib.parse import unquote

import base64

class Base64CoreSerializer(AbstractSerializer):
    """
    This class describes a base64 core serializer.
    """

    def __init__(self):
        super().__init__()

    def _fix_url_encoding_and_padding(self, s):
        # fix urlencoded chars
        s = unquote(s)
        # fix padding
        m = len(s) % 4
        if m != 0:
            s += "=" * (4 - m)
        return s

    def decode(self, s, **kwargs):
        value = self._fix_url_encoding_and_padding(s)
        encoding = kwargs.pop("encoding", "utf-8")
        if encoding:
            value = value.encode(encoding)
        value = base64.b64decode(value)
        if encoding:
            return value.decode(encoding)
        return value

    def encode(self, d, **kwargs):
        value = d
        encoding = kwargs.pop("encoding", "utf-8")
        if encoding and _type.is_str(value):
            value = value.encode(encoding)
        value = base64.b64encode(value)
        if encoding:
            value = value.decode(encoding)
        return value


class Base64Serializer(Base64CoreSerializer):
    def __init__(self):
        super().__init__()

    def _pop_options(self, options):
        encoding = options.pop("encoding", "utf-8")
        subformat = options.pop("subformat", None)
        from datajuggler.serializer import get_serializer_by_format

        serializer = get_serializer_by_format(subformat)
        return (serializer, encoding)

    def decode(self, s, **kwargs):
        serializer, encoding = self._pop_options(kwargs)
        value = super().decode(s, encoding=encoding)
        if serializer:
            value = serializer.decode(value, **kwargs)
        return value

    def encode(self, d, **kwargs):
        serializer, encoding = self._pop_options(kwargs)
        value = d
        if serializer:
            value = serializer.encode(value, **kwargs)
        value = super().encode(value, encoding=encoding)
        return value
