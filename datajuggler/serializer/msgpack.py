# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.serializer.core import encode, decode

try:
    import msgpack
    msgpack_enable = True
except ImportError:  # pragma: no cover
    msgpack_enable = False
    msgpack = AbstractSerializer()

class MsgpackSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='msgpack:custom',
                         package='msgpack', enable=msgpack_enable,
                         overwrite=True)

    def loads(self, content, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        raw = kwargs.pop('raw', False)
        kwargs.setdefault('raw', raw)
        return msgpack.unpackb(content, object_hook=decode, **kwargs)

    def dumps(self, obj, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        return msgpack.packb(obj, default=encode, **kwargs)

register_serializer(MsgpackSerializer)
