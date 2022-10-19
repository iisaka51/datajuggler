# -*- coding: utf-8 -*-

import csv
from io import StringIO
from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.validator import TypeValidator as _type

class CSVSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='csv')

    def loads(self, s, **kwargs):
        # kwargs.setdefault('delimiter', ',')
        if kwargs.pop("quote", False):
            # TODO: add tests coverage
            kwargs.setdefault("quoting", csv.QUOTE_ALL)
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        f = StringIO(s)
        r = csv.reader(f, **kwargs)
        ln = 0
        data = []
        for row in r:
            if ln == 0 and columns_row:
                if not columns:
                    columns = row
                ln += 1
                continue
            d = dict(zip(columns, row))
            data.append(d)
            ln += 1
        return data

    def dumps(self, d, **kwargs):
        ls = d
        # kwargs.setdefault('delimiter', ',')
        if kwargs.pop("quote", False):
            kwargs.setdefault("quoting", csv.QUOTE_ALL)
        kwargs.setdefault("lineterminator", "\n")
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        if not columns and len(ls) and _type.is_dict(ls[0]):
            keys = [str(key) for key in ls[0].keys()]
            columns = list(sorted(keys))
        f = StringIO()
        w = csv.writer(f, **kwargs)
        if columns_row and columns:
            w.writerow(columns)
        for item in ls:
            if _type.is_dict(item):
                row = [item.get(key, "") for key in columns]
            elif _type.is_collection(item):
                # TODO: add tests coverage
                row = item
            else:
                # TODO: add tests coverage
                row = [item]
            w.writerow(row)
        data = f.getvalue()
        return data

register_serializer(CSVSerializer)
