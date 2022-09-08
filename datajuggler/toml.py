from typing import Any, Optional

try:
    try:
        import tomllib as toml   # python 3.11 or later.
    except ImportError:
        import toml

    def to_toml(self, obj: Optional[Any]=None, **options):
        """instance method for convert to YAML"""
        obj = obj or self
        return toml.dumps(self.to_dict(obj))

    def from_toml(self, stream, *args, inplace: bool=False, **kwargs):
        """instance method for convert from YAML"""
        factory = lambda d: dict(*(args + (d,)), **kwargs)
        return self.from_dict(toml.loads(stream),
                              factory=factory, inplace=inplace)

except ImportError:
    def to_toml(self, **options):
        raise NotImplementedError('You should install toml.')

    def from_toml(cls, stream, *args, **kwargs):
        raise NotImplementedError('You should install toml.')
