# -*- coding: utf-8 -*-

from importlib import import_module

from .abstract import (
    AbstractSerializer, AbstractClassSerializer, register_serializer,
)
from .core import (
    get_class_serializer, encode_by_format,
    get_format_by_path, get_serializer_by_format,
    get_serializers_extensions, autodetect_format,
    is_database, is_data, validate_file, is_url, is_dsn,
    encode, decode, dumps, dump, loads, load,
    read_contents, read_url, read_database, read_file, write_file,
)

__modules__ = [
    "class_serializer",
    "base64",
    "csv",
    "ini",
    "plist",
    "query_string",
    "toml",
    "xml",
    "yaml",
    "json",
    "msgpack",
    "cloudpickle",
]

for mod in __modules__:
    import_module("." + mod, "datajuggler.serializer")


__all__ = [
    "AbstractSerializer",
    "AbstractClassSerializer",
    "register_serializer",
    "encode_by_format",
    "get_format_by_path",
    "get_format_and_subformat",
    "get_serializers_extensions",
    "get_serializer_by_format",
    "get_class_serializer",
    "autodetect_format",
    "validate_file",
    "is_url",
    "is_dsn",
    "is_database",
    "read_contents",
    "read_database",
    "read_url",
    "read_file",
    "write_file",
    "loads",
    "load",
    "dumps",
    "dump",
    "encode",
    "decode",
]

