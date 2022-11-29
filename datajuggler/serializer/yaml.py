# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.serializer.core import encode, decode

try:
    import yaml
    from yaml.constructor import MappingNode
    yaml_enable = True
except ImportError:  # pragma: no cover
    yaml_enable = False

    class YAML_Pretender(AbstractSerializer):
        """
        This class pretender of yaml module
        """
        class constructor(object):
            MappingNode = object

        class Dumper(object):
            def represent_mapping(self):
                raise NotImplementedError
            def add_representer(self):
                raise NotImplementedError

        class Loader(object):
            def construct_mapping(self):
                raise NotImplementedError

    yaml = YAML_Pretender()
    MappingNode = yaml.constructor.MappingNode


SERIALIZED_TAG = "tag:github.com/iisaka51/datajuggler,2022:python/datajuggler"

class Dumper(yaml.Dumper):
    def ignore_aliases(self, data):
        """See Also:
        https://github.com/yaml/pyyaml/issues/103
        https://github.com/yaml/pyyaml/issues/104
        """
        return True

    def represent_serialized(self, data, **kwargs):
        return self.represent_mapping(SERIALIZED_TAG, encode(data, **kwargs))

class Loader(yaml.Loader):
    def construct_serialized(self, node, **kwargs):
        assert node.tag == SERIALIZED_TAG
        assert isinstance(node, MappingNode)
        dct = self.construct_mapping(node, deep=True)
        return decode(dct)

class YAMLSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='yaml:custom', extension=['yaml', 'yml'],
                          package='PyYAML', enable=yaml_enable,
                          overwrite=True)
        Loader.add_constructor(SERIALIZED_TAG, Loader.construct_serialized)
        yaml.Dumper.ignore_aliases = lambda *args : True

    def loads(self, s, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        if encoding and isinstance(s, bytes):
            s = s.decode(encoding)
        return yaml.load(s, Loader=Loader, **kwargs)

    def dumps(self, d, **kwargs):
        kwargs, _, _, encoding, options = self.parse_kwargs(**kwargs)
        kwargs.update(options)
        if encoding:
            kwargs.setdefault('encoding', encoding)
        return yaml.dump(d, Dumper=Dumper, **kwargs)

    def register_class(self, cls):
        Dumper.add_representer(cls, Dumper.represent_serialized)
        Loader.add_constructor(SERIALIZED_TAG, Loader.construct_serialized)

register_serializer(YAMLSerializer)
