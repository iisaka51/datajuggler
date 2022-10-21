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
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.setdefault("fmt", plistlib.FMT_XML)
        if options:
            kwargs.update(options)
        if isinstance(s, str):
            s = s.encode(encoding)
        return plistlib.loads(s, **kwargs)

    def dumps(self, d, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        if options:
            kwargs.update(options)
        return plistlib.dumps(d, **kwargs).decode(encoding)

register_serializer(PListSerializer)
