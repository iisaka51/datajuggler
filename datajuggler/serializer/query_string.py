# -*- coding: utf-8 -*-

import re
from urllib.parse import urlencode
from urllib.parse import parse_qs

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)

class QueryStringSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format=['querystring', 'qs'])

    def loads(self, s, **kwargs):
        if isinstance(s, bytes):
            s = s.decode('utf-8')
        flat = kwargs.pop("flat", True)
        qs_re = r"(?:([\w\-\%\+\.\|]+\=[\w\-\%\+\.\|]*)+(?:[\&]{1})?)+"
        qs_pattern = re.compile(qs_re)
        if qs_pattern.match(s):
            data = parse_qs(s)
            if flat:
                data = {key: value[0] for key, value in data.items()}
            return data
        raise ValueError(f"Invalid query string: {s}")

    def dumps(self, d, **kwargs):
        data = urlencode(d, **kwargs)
        return data


register_serializer(QueryStringSerializer)
