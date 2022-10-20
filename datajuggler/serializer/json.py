# -*- coding: utf-8 -*-

import json
from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.serializer.core import encode, decode
from datajuggler.validator import TypeValidator as _type

pretty = dict( sort_keys=True, indent=4, separators=(",", ": ") )

class Encoder(json.JSONEncoder):
    def default(self, obj):
        return encode(obj, super().default)

class JSONSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='json:custom', overwrite=True)


    def dumps(self, obj, **kwargs):
        encoding = kwargs.pop('encoding', None)
        options = kwargs.pop('options', None)
        if options:
            kwargs.update(options)
        data  =  json.dumps(obj, cls=Encoder, **kwargs)
        if not encoding and isinstance(data, str):
            data = data.encode("utf-8")

        return data

    def loads(self, content, **kwargs):
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return json.loads(content, object_hook=decode, **kwargs)

register_serializer(JSONSerializer)
