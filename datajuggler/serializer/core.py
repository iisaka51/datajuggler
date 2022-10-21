# -*- coding: utf-8 -*-

import re
import pathlib
from io import BytesIO
from typing import Union, Any, Optional
from collections import namedtuple

import serialize
from serialize.all import (
    FORMATS, UNAVAILABLE_FORMATS, FORMAT_BY_EXTENSION,
    Format, UnavailableFormat,
    CLASSES, CLASSES_BY_NAME, register_class
)

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


FormatParse = namedtuple("FormatParse", "format subformat extension")
_SERIALIZERS_SCHEMES = [ "sqlite", "mysql", "postgresql" ]
Serializers = {}
MISSING = object()

def encode_by_format(s, format, encoding='utf-8'):
    # for compatibility of Serialize module
    required_encoding_format = [
        'bson', 'pickle', 'dill', 'json', 'msgpack',
        'phpserialize', 'serpent', 'yaml',
        'base64', 'b64', 'plist', 'querystring', 'qs',
        'ini', 'toml', 'xml', 'yml',
     ]

    fmtargs = parse_format(format)
    if fmtargs.extension in required_encoding_format:
        if isinstance(s, str):
            s = s.encode(encoding)
    else:
        if isinstance(s, bytes):
            s = s.decode(encoding)
    return s


def parse_format(format, extension=None) -> FormatParse:
    """Parse fomart and return tuple of (format, option, subformat, extension).
    i.e.:
    if set 'json:prety' to 'format', will be return as followings.
        format - json:prety
        subformat - ''
        extension - json
    if set 'base64,pickle,b64' to 'format', will be return as followings.
        format - base64
        subformat - pickle
        extension - b64

    """
    format_key = (format or "").lower().strip()
    if format_key.find(',') >=0:
        fmtargs = format_key.split(',')
        nargs = len(fmtargs)
        format = fmtargs[0]
        try:
            extension = fmtargs[2]
        except IndexError:
            extension = extension or fmtargs[0]

        if nargs == 1:
            return FormatParse(format, '', extension)
        elif nargs == 2:
            return FormatParse(format, fmtargs[1], extension)
        else:
            return FormatParse(format, fmtargs[1], extension)
    else:
        extension = extension or format_key.split(':')[0]
        return FormatParse(format_key, '', extension)

def get_class_serializer(item):
    def class_serializer(obj):
        return ( CLASSES[item].from_builtin,
                 (CLASSES[item].to_builtin(obj),),
                  None,
                  None,
                  None,
                )
    if item in CLASSES:
        return class_serializer
    else:
        return None

def _get_format(format) ->Format:
    """Convenience function to get the format information.
    Raises a nice error if the format is unavailable or unknown.
    """

    if isinstance(format, Format):
        format = Format[format].extension
    format = parse_format(format).format
    if format in FORMATS:
        return FORMATS[format]

    if format in UNAVAILABLE_FORMATS:
        raise ValueError( ( f"'{format}' is an unavailable format. "
                            f"{UNAVAILABLE_FORMATS[format].msg}" ))

    raise ValueError( f"'{format}' is an unknown format. "
                      f"Valid options are {', '.join(FORMATS.keys())}" )


def _get_format_from_ext(extension) ->str:
    """Convenience function to get the format information from a file extension.

    Raises a nice error if the extension is unknown.
    """

    extension = extension.lower()
    for fmt in FORMATS.keys():
        if extension == FORMATS[fmt].extension:
            # return FORMATS[fmt]
            return fmt

    valid = ", ".join(get_serializers_extensions())

    raise ValueError(
        f"'{extension}' is an unknown extension. "
        f"Valid options are: \n{valid}"
    )

def get_format_by_path(path) ->Format:
    path = path.lower()
    for scheme in _SERIALIZERS_SCHEMES:
        if isinstance(path, str) and path.startswith(f'{scheme}://'):
            return scheme

    path = pathlib.Path(path)
    format = _get_format_from_ext(path.suffix.lstrip("."))
    return format

def get_serializer_by_format(format):
    if format:
        format = parse_format(format).format
        serializer = _get_format(format)
        return serializer
    else:
        return None


def get_serializers_extensions():
    return list(FORMAT_BY_EXTENSION.keys() )


def autodetect_format(s):
    if isinstance(s, str) and (is_url(s) or is_dsn(s) or validate_file(s)):
        return get_format_by_path(s)

    return None

def register_format(
    fmt,
    dumpser=None,
    loadser=None,
    dumper=None,
    loader=None,
    extension=MISSING,
    register_class=None,
    overwrite=False,
):
    """Register an available serialization format.

    `fmt` is a unique string identifying the format, such as `json`. Use a colon (`:`) to
    separate between subformats.

    `dumpser` and `dumper` should be callables with the same purpose and arguments
    that `json.dumps` and `json.dump`. If one of those is missing, it will be
    generated automatically from the other.

    `loadser` and `loader` should be callables with the same purpose and arguments
    that `json.loads` and `json.load`. If one of those is missing, it will be
    generated automatically from the other.

    `extension` is the file extension used to guess the desired serialization format when loading
    from or dumping to a file. If not given, the part before the colon of `fmt` will be used.

    `register_class` is a callback made when a class is registered with
    `serialize.register_class`. When a new format is registered,
    previously registered classes are called. It takes on argument, the
    class to register. See `serialize.yaml.py` for an example.
    if `overwrite`` is True, register overwrite old entry..
    """

    if not overwrite and fmt in FORMATS:
        raise ValueError("%s is already defined." % fmt)

    # Here we generate register_class if it is not present
    if not register_class:

        def register_class(klass):
            pass

    # Here we generate dumper/dumpser if they are not present.
    if dumper and not dumpser:

        def dumpser(obj, **kwargs):
            buf = BytesIO()
            dumper(obj, buf, **kwargs)
            return buf.getvalue()

    elif not dumper and dumpser:

        def dumper(obj, fp, **kwargs):
            fp.write(dumpser(obj, **kwargs))

    elif not dumper and not dumpser:

        def raiser(*args, **kwargs):
            raise ValueError("dump/dumps is not defined for %s" % fmt)

        dumper = dumpser = raiser

    # Here we generate loader/loadser if they are not present.
    if loader and not loadser:

        def loadser(serialized, **kwargs):
            return loader(BytesIO(serialized), **kwargs)

    elif not loader and loadser:

        def loader(fp, **kwargs):
            return loadser(fp.read(), **kwargs)

    elif not loader and not loadser:

        def raiser(*args, **kwargs):
            raise ValueError("load/loads is not defined for %s" % fmt)

        loader = loadser = raiser

    extension = extension.lower() if isinstance(extension, str) else MISSING
    format, subformat, extension = tuple(parse_format(fmt, extension))
    if extension is MISSING:
        extension = fmt.split(":", 1)[0]

    FORMATS[fmt] = Format(extension, dumper, dumpser, loader, loadser, register_class)

    if extension and overwrite:
        FORMAT_BY_EXTENSION[extension] = fmt
    elif extension and extension not in FORMAT_BY_EXTENSION:
        FORMAT_BY_EXTENSION[extension] = fmt

    # register previously registered classes with the new format
    for klass in CLASSES:
        FORMATS[fmt].register_class(klass)

def register_unavailable(fmt, msg="", pkg="", extension=MISSING):
    """Register an unavailable serialization format.

    Unavailable formats are those known by Serialize but that cannot be used
    due to a missing requirement (e.g. the package that does the work).

    """
    if pkg:
        msg = "This serialization format requires the %s package." % pkg

    extension = extension.lower() if isinstance(extension, str) else MISSING
    if extension is MISSING:
        extension = fmt.split(":", 1)[0]

    UNAVAILABLE_FORMATS[fmt] = UnavailableFormat(extension, msg)

    if extension and extension not in FORMAT_BY_EXTENSION:
        FORMAT_BY_EXTENSION[extension] = fmt


def encode(obj, defaultfunc=None, **kwargs):
    """Encode registered types using the corresponding functions.
    For other types, the defaultfunc will be used
    """

    def encode_helper(obj, to_builtin):
        """Encode an object into a two element dict using a function
        that can convert it to a builtin data type.
        """

        return dict(__class_name__=str(obj.__class__), __dumped_obj__=to_builtin(obj, **kwargs))


    for klass, (to_builtin, _) in CLASSES.items():
        if isinstance(obj, klass):
            return encode_helper(obj, to_builtin)

    if defaultfunc is None:
        return obj

    return defaultfunc(obj, **kwargs)


def decode(dct, classes_by_name=None, **kwargs):
    """If the dict contains a __class__ and __serialized__ field tries to
    decode it using the registered classes within the encoder/decoder
    instance.
    """
    if not isinstance(dct, dict):
        return dct

    s = dct.get("__class_name__", None)
    if s is None:
        return dct

    classes_by_name = classes_by_name or CLASSES_BY_NAME
    try:
        _, from_builtin = classes_by_name[s]
        c = dct["__dumped_obj__"]
    except KeyError:
        return dct

    return from_builtin(c, **kwargs)

def dumps(obj, format, **kwargs):
    """Serialize `obj` to bytes using the format specified by `format`"""

    format, subformat, _ = tuple(parse_format(format))
    if subformat:
        kwargs.setdefault('subformat', subformat)
    encoding = kwargs.pop("encoding", None)
    if encoding and isinstance(obj, str):
        obj = obj.encode(encoding)
    options = kwargs.pop("options", dict())
    if options:
        kwargs.update(options)

    data = _get_format(format).dumps(obj, **kwargs)

    if encoding and isinstance(data, bytes):
        data = data.decode(encoding)

    return data


def dump(obj, file, format=None, **kwargs):
    """Serialize `obj` to a file using the format specified by `format`

    The file can be specified by a file-like object or filename.
    In the latter case the format is not need if it can be guessed from the extension.
    """
    if str and isinstance(file, str):
        file = pathlib.Path(file)

    options = kwargs.pop("options", dict())
    if options:
        kwargs.update(options)
    if isinstance(file, pathlib.Path):
        if format is None:
            format = _get_format_from_ext(file.suffix.lstrip("."))
        with file.open(mode="wb") as fp:
            dump(obj, fp, format, **kwargs)
    else:
        _get_format(format).dump(obj, file, **kwargs)


def loads(serialized, format, **kwargs):
    """Deserialize bytes using the format specified by `format`
    if pass `encoding` parameters and `serialized` is str,
    encoding str performed first before processing.
    note: `encoding` parameter will be dropped.
    """

    format, subformat, _ = tuple(parse_format(format))
    if subformat:
        kwargs.setdefault('subformat', subformat)
    encoding = kwargs.pop("encoding", None)
    if encoding:
        serialized = encode_by_format(serialized, format, encoding=encoding)
    options = kwargs.pop("options", dict())
    if options:
        kwargs.update(options)

    data = _get_format(format).loads(serialized, **kwargs)

    if encoding and isinstance(data, bytes):
        data = data.decode(encoding)

    return data


def load(file, format=None, **kwargs):
    """Deserialize from a file using the format specified by `format`

    The file can be specified by a file-like object or filename.
    In the latter case the format is not need if it can be guessed from the extension.
    """
    if isinstance(file, str):
        file = pathlib.Path(file)

    options = kwargs.pop("options", dict())
    if options:
        kwargs.update(options)

    if isinstance(file, pathlib.Path):
        if format is None:
            format = _get_format_from_ext(file.suffix.lstrip("."))
        with file.open(mode="rb") as fp:
            return load(fp, format, **kwargs)

    return _get_format(format).load(file)


def validate_file(s, thrown_error: bool=False):
    try:
        filepath = pathlib.Path(s)
    except TypeError:
        return False

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
    if isinstance(s, str):
        return any([ s.startswith(protocol)
                 for protocol in ["http://", "https://"] ])
    else:
        return False

def is_database(f):
    return f in _SERIALIZERS_SCHEMES

def is_dsn(s):
    if s and isinstance(s, str):
        return any([ s.startswith(protocol)
                 for protocol in ["sqlite://", "mysql://", "postgresql://"] ])
    else:
        return False

def is_data(s):
    if isinstance(s, dict):
        return True
    else:
        return len(s.splitlines()) > 1

def read_contents(s,
        *args: Any,
        serialize: bool=False,
        thrown_error: bool=False,
        **kwargs: Any,
    ) ->Union[str, list]:
    # s -> filepath or url or data
    if is_data(s): # data
        return s
    elif is_url(s): # url
        return read_url(s, serialize=serialize)
    elif is_dsn(s): # databse
        return list(read_database(s, **kwargs))
    elif validate_file(s, thrown_error=thrown_error):
        return read_file(s, serialize=serialize, thrown_error=thrown_error)
    # one-line data?!
    return s


def read_url(
        url: str,
        encoding: str='utf-8',
        serialize: bool=False,
        **options: Any
    ):
    if not requests_installed:
        raise NotImplementedError("'requests' module is not installed.")

    response = requests.get(url, **options)
    response.raise_for_status()
    contents = response.text
    if serialize:
        try:
            format = pathlib.Path(url).suffix.lstrip('.')
            if isinstance(contents, str):
                contents = contents.encode(encoding)
            contents = loads(contents, format)
        except:
            contents = response.text
    return contents

def read_database(
        dsn: str,
        as_str: bool=False,
        row_type=None,
        **kwargs: Any
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
    row_type = row_type or dict
    db = dataset.connect(dsn, row_type=row_type)
    contents = []
    if table in db:
        tbl = db[table]
        if len(kwargs)>0:
            data = tbl.find(**kwargs)
        else:
            data = tbl.all()
        for x in data:
            if as_str:
                yield str(dict(x))
            else:
                yield x

    db.executable.invalidate()
    db.executable.engine.dispose()
    db.close()

def read_file(
        filepath: Union[str, pathlib.Path],
        encoding: Optional[str]=None,
        serialize: bool=False,
        thrown_error: bool=False,
        **options: Any
    ):
    ops = dict(encoding=encoding)
    ops.update(options)

    if serialize:
        contents = load(filepath, encoding=encoding)
    else:
        if validate_file(filepath, thrown_error=thrown_error):
            with open(filepath, 'rb', **options) as file:
                contents = file.read()
        else:
            contents = None
    if encoding and isinstance(contents, bytes):
        try:
            contents = contents.decode(encoding)
        except:
            pass
    return contents


def write_file(
        filepath: Union[str, pathlib.Path],
        content: str,
        append: bool=False,
        encording: str="utf-8",
        serialize: bool=False,
        **options: Any
    ):
    filepath = pathlib.Path(filepath).absolute()
    this_dir = filepath.parent
    filepath.mkdir(parents=True, exists_ok=True)
    if serialize:
        dump(content, filepath, **options)
    else:
        mode = 'a' if append else 'w'
        ops = dict(encording=encording)
        ops.update(options)
        with open(str(filepath), mode, **options) as file:
            file.write(content)

__all__ = [
    "register_class",
    "register_format",
    "register_unavailable",
    "get_format_by_path",
    "parse_format",
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
    "decode",
    "encode",
    "FORMATS",
    "FORMAT_BY_EXTENSION",
]

