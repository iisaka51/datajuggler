# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import AbstractSerializer
from datajuggler.serializer.json import JSONSerializer
from pathlib import Path
from typing import Optional, Type, Union

try:
    import yaml
    from yaml.representer import Representer, SafeRepresenter

    def yaml_initializer(cls, factory: Optional[Type[dict]]=None):
        """class method to initialize for YAML"""

        def _from_yaml(loader, node):
            nonlocal factory
            value = loader.construct_mapping(node)
            data = factory(value)
            yield data

        def _to_yaml_safe(dumper, data):
            return dumper.represent_dict(data)

        def _to_yaml(dumper, data):
            nonlocal module_name, factory_name
            return dumper.represent_mapping(u'!{}.{}'.format(module_name, factory_name), data)

        factory = factory or cls
        factory_name=factory.__name__
        module_name = Path(__file__).parent.parent.name

        for loader_name in ( "BaseLoader", "FullLoader", "SafeLoader",
                             "Loader", "UnsafeLoader", "DangerLoader" ):
            LoaderCls = getattr(yaml, loader_name, None)
            if LoaderCls is None:
                # This code supports both PyYAML 4.x and 5.x versions
                continue
            yaml.add_constructor(u'!{}'.format( module_name ),
                                  _from_yaml, Loader=LoaderCls)
            yaml.add_constructor(u'!{}.{}'.format( module_name, factory_name ),
                                  _from_yaml, Loader=LoaderCls)
            yaml.add_constructor(u'!python/object:{}.{}'.format(
                                           module_name, factory_name),
                                  _from_yaml, Loader=LoaderCls)
            yaml.add_constructor(u'!python/object/new:{}.{}'.format(
                                           module_name, factory_name),
                                  _from_yaml, Loader=LoaderCls)

        SafeRepresenter.add_representer(cls, _to_yaml_safe)
        SafeRepresenter.add_multi_representer(cls, _to_yaml_safe)

        Representer.add_representer(cls, _to_yaml)
        Representer.add_multi_representer(cls, _to_yaml)


    class YAMLSerializer(AbstractSerializer):
        """
        This class describes an yaml serializer.
        """

        def __init__(self, factory: Optional[Type[dict]]=None):
            super().__init__()
            self._json_serializer = JSONSerializer()

        def decode(self, s, **kwargs):
            factory = lambda d: dict(*(args + (d,)), **kwargs)
            loader_class = kwargs.pop('Loader', yaml.FullLoader)
            return yaml.load(s, Loader=loader_class)

        def encode(self, d, **options):
            d = self._json_serializer.decode(self._json_serializer.encode(d))
            opts = dict(indent=4, default_flow_style=False, allow_unicode=True)
            opts.update(options)
            if 'Dumper' not in opts:
                return yaml.safe_dump(d, **opts)
            else:
                return yaml.dump(d, **opts)
            return data

except ImportError:
    def yaml_initializer(cls, factory: Optional[Type[dict]]=None):
        pass

    class YAMLSerializer(AbstractSerializer):
        """
        This class describes an yaml serializer.
        """

        def __init__(self):
            super().__init__()

        def decode(self, s, **kwargs):
            raise NotImplementedError('You should install PyYAML.')

        def encode(self, d, **kwargs):
            raise NotImplementedError('You should install PyYAML.')

