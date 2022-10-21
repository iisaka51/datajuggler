# -*- coding: utf-8 -*-

import base64
from urllib.parse import unquote
from typing import Any

import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from datajuggler.serializer.abstract import (
    AbstractSerializer, register_serializer
)
from datajuggler.serializer.core import encode_by_format
from datajuggler.validator import TypeValidator as _type

_SALT_SIZE = 12

class Base64Serializer(AbstractSerializer):
    def __init__(self):
        super().__init__(format=['base64', 'b64'])

    def derive_key(self,
            password: str,
            salt: bytes
        ) -> bytes:
        encoded_password = password.encode('ASCII')
        kdf = PBKDF2HMAC( algorithm=hashes.SHA256(),
                          length=32,
                          salt=salt,
                          iterations=100_000,
                          backend=default_backend() )
        return base64.urlsafe_b64encode(kdf.derive(encoded_password))

    def decrypt(self,
            input_data: bytes,
            password: str,
        ) -> Any:
        salt = input_data[:_SALT_SIZE]
        encrypted_data = input_data[_SALT_SIZE:]
        key = self.derive_key(password, salt)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data

    def encrypt(self,
            raw_data: Any,
            password: str,
        ) -> bytes:
            salt = secrets.token_bytes(_SALT_SIZE)
            key = self.derive_key(password, salt)
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(raw_data)
            return salt + encrypted_data

    def loads(self, s, **kwargs):
        """base64 encoder
        if not set 'password', no decrypt..
        if set 'encoding', encoding as string.
        if set 'subformat', first decoding base64 then decoding subformat
        """
        def _decode(s, password):
            def _fix_url_encoding_and_padding(s):
                s = unquote(s)     # fix urlencoded chars
                m = len(s) % 4     # fix padding
                if m != 0:
                    s += "=" * (4 - m)
                return s

            value = _fix_url_encoding_and_padding(s)
            value = base64.b64decode(value)
            if password:
                value = self.decrypt(value, password)
            return value


        kwargs, serializer, subformat, encoding, options = self.parse_kwargs(**kwargs)
        if _type.is_bytes(s):
                s = s.decode('utf-8')
        password = kwargs.pop('password', None)
        value = _decode(s, password)
        if serializer:
            kwargs.update(options)
            value = serializer.loads(value, **kwargs)
        return value


    def dumps(self, obj, **kwargs): # encrypt
        """encripyted base64 encoder
        if not set 'password', no encrypt.
        if set 'encoding', encoding as string.
        if set 'subformat', first encoding subformat then encrypt
        """
        def _b64encode(data, password, encoding):
            if encoding and _type.is_str(data):
                data = data.encode(encoding)
            if password:
                data = self.encrypt(data, password)
            data = base64.b64encode(data)
            if encoding and _type.is_str(data):
                data = data.encode(encoding)
            return data

        kwargs, serializer, subformat, encoding, options = self.parse_kwargs(**kwargs)
        password = kwargs.pop('password', None)
        if serializer:
            objata = encode_by_format(obj, subformat)
            kwargs.update(options)
            serialized_data = serializer.dumps(obj, **kwargs)
        else:
            serialized_data = obj

        encrypted_data = _b64encode(serialized_data, password, encoding)
        return encrypted_data


register_serializer(Base64Serializer)

