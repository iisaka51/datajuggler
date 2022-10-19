from .core import (
    register_format, register_unavailable, register_class,
    get_serializer_by_format,
)

MISSING = object()
__Serializers = {}

def register_serializer(cls):
    __Serializers[cls.__class__.__name__] = cls()

class AbstractClassSerializer(object):
    def __init__(self, cls):
        register_class(cls, self.encode, self.decode)
        super().__init__()

    def encode(self, obj):
        pass

    def decode(self, obj):
        pass

    def raise_error(self, obj):
        raise TypeError(f"Unserializable object {obj} of type {type(obj)}")


class AbstractSerializer(object):
    """
    This class describes an abstract serializer.
    """

    def __init__(self, format=None, extension=MISSING,
                       package=None, enable:bool=True,
                       overwrite=False):
        if not format:
            super().__init__()
            return

        format = [format] if isinstance(format, str) else format


        if extension is MISSING:
            extension = [extension]
        elif isinstance(extension, str):
            extension = [extension.lower()]

        try:
            dumps = self.dumps
        except NotImplementedError:
            dumps = None
        try:
            loads = self.loads
        except NotImplementedError:
            loads = None
        try:
            dumper = self.dumper
        except NotImplementedError:
            dumper = None
        try:
            loader = self.loader
        except NotImplementedError:
            loader = None
        try:
            regist_cls = self.register_class
        except NotImplementedError:
            regist_cls = None

        for fmt in format:
            if not enable:
                register_unavailable(fmt, pkg=package)

            try:
                for ext in extension:
                    register_format(fmt,
                            dumpser=dumps, loadser=loads,
                            dumper=dumper, loader=loader,
                            extension=ext,
                            register_class=regist_cls,
                            overwrite=overwrite,
                            )
            except ValueError:
                pass   # already registered

        super().__init__()

    def parse_kwargs(self, subformat='', **kwargs):
        encoding = kwargs.pop("encoding", "utf-8")
        subformat = kwargs.pop("subformat", subformat)

        serializer = get_serializer_by_format(subformat)
        return (serializer, subformat, encoding)

    def __getattr__(self, k):
        if k not in dir(self):
            raise NotImplementedError


__init__ = [
    "AbstractSerializer",
    "AbstractClassSerializer",
]
