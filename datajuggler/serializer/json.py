# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer
from datajuggler.validator import TypeValidator as _type

import json


class JSONSerializer(AbstractSerializer):
    """
    This class describes a json serializer.
    """

    def __init__(self):
        super().__init__()

    def decode(self, s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        kwargs.setdefault("default", self._encode_default)
        data = json.dumps(d, **kwargs)
        return data

    def _encode_default(self, obj):
        if _type.is_set(obj):
            return list(obj)
        elif _type.is_datetime(obj):
            return obj.isoformat()
        elif _type.is_decimal(obj):
            return str(obj)
        return str(obj)
