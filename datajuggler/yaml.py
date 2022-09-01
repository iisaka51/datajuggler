try:
    import yaml
    from yaml.representer import Representer, SafeRepresenter

    def yaml_initializer(cls, factory=None):
        from pathlib import Path

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
        module_name = Path(__file__).parent.name

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

    def to_yaml(self, **options):
        """instance method for convert to YAML"""
        opts = dict(indent=4, default_flow_style=False, allow_unicode=True)
        opts.update(options)
        if 'Dumper' not in opts:
            return yaml.safe_dump(self, **opts)
        else:
            return yaml.dump(self, **opts)

    def from_yaml(self, stream, *args, inplace: bool=False, **kwargs):
        """instance method for convert from YAML"""
        factory = lambda d: type(self)(*(args + (d,)), **kwargs)
        loader_class = kwargs.pop('Loader', yaml.FullLoader)
        return self.from_dict(yaml.load(stream, Loader=loader_class),
                              factory=factory, inplace=inplace)

except ImportError:
    def to_yaml(self, **options):
        raise NotImplementedError('You should install PyYAML.')

    def from_yaml(cls, stream, *args, **kwargs):
        raise NotImplementedError('You should install PyYAML.')

    def yaml_initializer(cls):
        pass
