# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer

try:
    try:
        import tomllib as toml   # python 3.11 or later.
    except ImportError:
        import toml


    class TOMLSerializer(AbstractSerializer):
        """
        This class describes a toml serializer.
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            return toml.loads(s, **kwargs)

        def encode(self, d, **kwargs):
            return toml.dumps(dict(d), **kwargs)


except ImportError:

    class TOMLSerializer(AbstractSerializer):
        """
        This class describes a toml serializer.
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            raise NotImplementedError('You should install toml.')

        def encode(self, d, **kwargs):
            raise NotImplementedError('You should install toml.')
