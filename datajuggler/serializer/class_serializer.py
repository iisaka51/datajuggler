import datetime
import decimal
from datajuggler.serializer.abstract import (
    AbstractClassSerializer, register_serializer
)
from datajuggler.validator import TypeValidator as _type

class DatetimeClassSerializer(AbstractClassSerializer):
    def __init__(self, cls=datetime.datetime):
        super().__init__(cls)

    def encode(self, obj):
        if _type.is_datetime(obj):
            return {
                "__type__": "datetime",
                "value": [
                     obj.year,
                     obj.month,
                     obj.day,
                     obj.hour,
                     obj.minute,
                     obj.second,
                    ],
                }
        else:
            super().encode(obj)

    def decode(self, obj):
        v = obj.get("__type__")
        if v == "datetime":
            return datetime.datetime(*obj["value"])

        self.raise_error(obj)

class DateClassSerializer(AbstractClassSerializer):
    def __init__(self, cls=datetime.date):
        super().__init__(cls)

    def encode(self, obj):
        if _type.is_date(obj):
            return {
                "__type__": "date",
                "value": [
                     obj.year,
                     obj.month,
                     obj.day,
                    ],
                }
        else:
            super().encode(obj)

    def decode(self, obj):
        v = obj.get("__type__")
        if v == "date":
            return datetime.date(*obj["value"])

        self.raise_error(obj)

class TimeClassSerializer(AbstractClassSerializer):
    def __init__(self, cls=datetime.time):
        super().__init__(cls)

    def encode(self, obj):
        if _type.is_time(obj):
            return {
                "__type__": "time",
                "value": [
                     obj.hour,
                     obj.minute,
                     obj.second,
                    ],
                }
        else:
            super().encode(obj)

    def decode(self, obj):
        v = obj.get("__type__")
        if v == "time":
            return datetime.time(*obj["value"])

        self.raise_error(obj)

class DecimalClassSerializer(AbstractClassSerializer):
    def __init__(self, cls=decimal.Decimal):
        super().__init__(cls)

    def encode(self, obj):
        if _type.is_decimal(obj):
            return {
                "__type__": "Decimal",
                "value": str(obj),
                }
        else:
            return obj

    def decode(self, obj):
        v = obj.get("__type__")
        if v == "Decimal":
            return decimal.Decimal(obj["value"])

        self.raise_error(obj)


register_serializer(DatetimeClassSerializer)
register_serializer(DateClassSerializer)
register_serializer(TimeClassSerializer)
register_serializer(DecimalClassSerializer)
