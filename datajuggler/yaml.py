import snoop
from pathlib import Path

try:
    import yaml
    from yaml.representer import Representer, SafeRepresenter

    def yaml_initializer(cls, factory=None):
        """class method to initialize for YAML"""

        def _from_yaml(loader, node):
            nonlocal factory
            data = factory()
            yield data
            value = loader.construct_mapping(node)
            data.update(value)

        def _to_yaml_safe(dumper, data):
            return dumper.represent_dict(data)

        def _to_yaml(dumper, data):
            nonlocal factory_name
            return dumper.represent_mapping(
                           '!{}'.format(factory_name), data)

        factory = factory or cls
        factory_name=cls.__name__

        for loader_name in ( "BaseLoader", "FullLoader", "SafeLoader",
                             "Loader", "UnsafeLoader", "DangerLoader" ):
            LoaderCls = getattr(yaml, loader_name, None)
            if LoaderCls is None:
                # This code supports both PyYAML 4.x and 5.x versions
                continue
            package_name = Path(__file__).parent
            yaml.add_constructor('!{}'.format( package_name ),
                                  _from_yaml, Loader=LoaderCls)
            yaml.add_constructor('!{}.{}'.format( package_name, factory_name),
                                  _from_yaml, Loader=LoaderCls)

        SafeRepresenter.add_representer(cls, _to_yaml_safe)
        SafeRepresenter.add_multi_representer(cls, _to_yaml_safe)

        Representer.add_representer(cls, _to_yaml)
        Representer.add_multi_representer(cls, _to_yaml)

    def to_yaml(self, **options):
        """instance method for convert to YAML"""
        opts = dict(indent=4, default_flow_style=False)
        opts.update(options)
        if 'Dumper' not in opts:
            return yaml.safe_dump(self, **opts)
        else:
            return yaml.dump(self, **opts)

    @snoop
    def from_yaml(self, stream, *args, **kwargs):
        """instance method for convert from YAML"""
        factory = lambda d: cls(*(args + (d,)), **kwargs)
        loader_class = kwargs.pop('Loader', yaml.FullLoader)
        return self.from_dict(yaml.load(stream, Loader=loader_class),
                              factory=type(self))


except ImportError:
    def to_yaml(self, **options):
        raise NotImplementedError('You should install PyYAML.')

    def from_yaml(cls, stream, *args, **kwargs):
        raise NotImplementedError('You should install PyYAML.')

    def yaml_initializer(cls):
        pass
