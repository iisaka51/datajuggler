# -*- coding: utf-8 -*-

import re

from pathlib import Path
from typing import Union, Any

try:
    import requests
    requests_installed = True
except ImportError:
    requests_installed = False

try:
    import dataset
    dataset_installed = True
except ImportError:
    dataset_installed = False


from datajuggler.serializer.abstract import AbstractSerializer
from datajuggler.serializer.base64 import Base64Serializer
from datajuggler.serializer.csv import CSVSerializer
from datajuggler.serializer.ini import INISerializer
from datajuggler.serializer.json import JSONSerializer
from datajuggler.serializer.pickle import PickleSerializer
from datajuggler.serializer.plist import PListSerializer
from datajuggler.serializer.query_string import QueryStringSerializer
from datajuggler.serializer.toml import TOMLSerializer
from datajuggler.serializer.xml import XMLSerializer
from datajuggler.serializer.yaml import YAMLSerializer, yaml_initializer


__all__ = [
    "AbstractSerializer",
    "Base64Serializer",
    "CSVSerializer",
    "INISerializer",
    "JSONSerializer",
    "PickleSerializer",
    "PListSerializer",
    "QueryStringSerializer",
    "TOMLSerializer",
    "XMLSerializer",
    "YAMLSerializer",
    "yaml_initializer",
    "get_format_by_path",
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
]

_BASE64_SERIALIZER = Base64Serializer()
_CSV_SERIALIZER = CSVSerializer()
_INI_SERIALIZER = INISerializer()
_JSON_SERIALIZER = JSONSerializer()
_PICKLE_SERIALIZER = PickleSerializer()
_PLIST_SERIALIZER = PListSerializer()
_QUERY_STRING_SERIALIZER = QueryStringSerializer()
_TOML_SERIALIZER = TOMLSerializer()
_YAML_SERIALIZER = YAMLSerializer()
_XML_SERIALIZER = XMLSerializer()

_SERIALIZERS = {
    "b64": _BASE64_SERIALIZER,
    "base64": _BASE64_SERIALIZER,
    "csv": _CSV_SERIALIZER,
    "ini": _INI_SERIALIZER,
    "json": _JSON_SERIALIZER,
    "pickle": _PICKLE_SERIALIZER,
    "plist": _PLIST_SERIALIZER,
    "qs": _QUERY_STRING_SERIALIZER,
    "querystring": _QUERY_STRING_SERIALIZER,
    "toml": _TOML_SERIALIZER,
    "yaml": _YAML_SERIALIZER,
    "yml": _YAML_SERIALIZER,
    "xml": _XML_SERIALIZER,
}

_SERIALIZERS_EXTENSIONS = [f".{extension}" for extension in _SERIALIZERS.keys()]
_SERIALIZERS_SCHEMES = [ "sqlite", "mysql", "postgresql" ]


def get_format_by_path(path):
    path = path.lower()
    for scheme in _SERIALIZERS_SCHEMES:
        if path.startswith(f'{scheme}://'):
            return scheme
    for extension in _SERIALIZERS_EXTENSIONS:
        if path.endswith(extension):
            return extension[1:]
    return None


def get_serializer_by_format(format):
    format_key = (format or "").lower().strip()
    format_key = re.sub(r"[\s\-\_]*", "", format_key)
    return _SERIALIZERS.get(format_key)


def get_serializers_extensions():
    return list(_SERIALIZERS_EXTENSIONS)


def autodetect_format(s):
    if isinstance(s, str) and (is_url(s) or is_dsn(s) or validate_file(s)):
        return get_format_by_path(s)
    return None

def is_database(f):
    return f in _SERIALIZERS_SCHEMES

def decode(
        s: str,
        format: str,
        **kwargs: Any
    ):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    decode_opts = kwargs.copy()
    data = s.strip() if isinstance(s, str) else s
    data = serializer.decode(s, **decode_opts)
    return data


def encode(
        d: dict,
        format: str,
        **kwargs: Any
    ):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    s = serializer.encode(d, **kwargs)
    return s


def is_data(s):
    if isinstance(s, dict):
        return True
    else:
        return len(s.splitlines()) > 1


def validate_file(s, thrown_error: bool=False):
    filepath = Path(s)
    if filepath.exists():
        if filepath.is_file():
            file = str(s)
            if any([file.endswith(ext)
                    for ext in get_serializers_extensions()]):
                return True
            elif thrown_error:
                raise RuntimeError(f'Unsupported file extension: {filepath}')
        else:
            raise RuntimeError(f'filepath is not file: {filepath}')
    elif thrown_error:
        raise FileNotFoundError(f'No such file or directory: {filepath}')

    return False


def is_url(s):
    return any([ s.startswith(protocol)
                 for protocol in ["http://", "https://"] ])

def is_dsn(s):
    return any([ s.startswith(protocol)
                 for protocol in ["sqlite://", "mysql://", "postgresql://"] ])

def read_contents(s, thrown_error: bool=False) ->Union[str, list]:
    # s -> filepath or url or data
    if is_data(s): # data
        return s
    elif is_url(s): # url
        return read_url(s)
    elif is_dsn(s): # databse
        return list(read_database(s))
    elif validate_file(s, thrown_error=thrown_error):
        return read_file(s, thrown_error=thrown_error)
    # one-line data?!
    return s


def read_url(
        url: str,
        **options: Any
    ):
    if not requests_installed:
        raise NotImplementedError("'requests' module is not installed.")

    response = requests.get(url, **options)
    response.raise_for_status()
    contents = response.text
    return contents

def read_database(
        dsn: str,
        find: dict={},
        *,
        as_str: bool=False,
        **options: Any
    ):
    """Read database and return list of dictionary.
    default table name is 'default'.
    table name pass to after '#' in dsn.
    i.e.:  'sqlite:///users.sqlite#users'
    supported database are 'sqlite', 'mysql', 'postgresql'.
    """
    if not dataset_installed:
        raise NotImplementedError("'dataset' module is not installed.")

    if dsn.find('#')>0:
        dsn, table = dsn.split('#')
    else:
        table = 'default'
    db = dataset.connect(dsn, **options)
    contents = []
    if table in db:
        tbl = db[table]
        if find:
            data = tbl.find(**find)
        else:
            data = tbl.all()
        for x in data:
            if as_str:
                yield str(dict(x))
            else:
                yield dict(x)

def read_file(
        filepath: Union[str, Path],
        encording: str="utf-8",
        thrown_error: bool=False,
        **options: Any
    ):
    contents = ""
    if validate_file(filepath, thrown_error=thrown_error):
        ops = dict(encording=encording)
        ops.update(options)
        with open(filepath, 'r', **options) as file:
            contents = file.read()
    return contents


def write_file(
        filepath: Union[str, Path],
        content: str,
        append: bool=False,
        encording: str="utf-8",
        **options: Any
    ):
    filepath = Path(filepath).absolute()
    this_dir = filepath.parent
    filepath.mdir(parents=True, exists_ok=True)
    mode = 'a' if append else 'w'
    ops = dict(encording=encording)
    ops.update(options)
    with open(str(filepath), mode, **options) as file:
        file.write(content)
