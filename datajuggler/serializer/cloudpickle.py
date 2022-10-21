# -*- coding: utf-8 -*-

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)

try:
    import cloudpickle
    cloudpickle_enable = True
except ImportError:  # pragma: no cover
    cloudpickle_enable = False
    cloudpickle = AbstractSerializer()

class CloudpickleSerializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format='cloudpickle',
                         extension=['pickle', 'cpickle'],
                         package='cloudpickle',
                         enable=cloudpickle_enable,
                         overwrite=True)

    def loads(self, s, **kwargs):
        data = cloudpickle.loads(s, **kwargs)
        return data

    def dumps(self, d, **kwargs):
        data = cloudpickle.dumps(d, **kwargs)
        return data

register_serializer(CloudpickleSerializer)
