# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)

try:
    try:
        import tomllib as toml   # python 3.11 or later.
    except ImportError:
        import toml
    toml_enable = True
except ImportError:  # pragma: no cover
    toml_enable = False
    toml = AbstractSerializer()

class TOMLSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='toml', package='toml', enable=toml_enable)

    def loads(self, s, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        if isinstance(s, bytes):
            s = s.decode('utf-8')
        return toml.loads(s, **kwargs)

    def dumps(self, d, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        return toml.dumps(d, **kwargs)

register_serializer(TOMLSerializer)
