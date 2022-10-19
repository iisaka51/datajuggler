# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)

try:
    import plistlib
    plist_enable = True
except ImportError:  # pragma: no cover
    plist_enable = False
    plistlib = AbstractSerializer()

class PListSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='plist',
                         package='plistlib', enable=plist_enable)

    def loads(self, s, **kwargs):
        kwargs.setdefault("fmt", plistlib.FMT_XML)
        encoding = kwargs.pop("encoding", "utf-8")
        if isinstance(s, str):
            s = s.encode(encoding)
        return plistlib.loads(s, **kwargs)

    def dumps(self, d, **kwargs):
        encoding = kwargs.pop("encoding", "utf-8")
        return plistlib.dumps(d, **kwargs).decode(encoding)

register_serializer(PListSerializer)
