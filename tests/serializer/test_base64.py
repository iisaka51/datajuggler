import base64
import decimal
import datetime

import pytest

from datajuggler import serializer as io
from datajuggler import aDict, uDict

simple_data = { 'January': 1, 'February': 2, 'March': 3, 'April': 4 }
base64_simple = (
    'eydKYW51YXJ5JzogMSwgJ0ZlYnJ1YXJ5JzogMiw'
    'gJ01hcmNoJzogMywgJ0FwcmlsJzogNH0='
)
base64_simple_encode = (
    b'eydKYW51YXJ5JzogMSwgJ0ZlYnJ1YXJ5JzogMiw'
    b'gJ01hcmNoJzogMywgJ0FwcmlsJzogNH0='
)

nest_data = [None,
 {},
 [1, 2, 3, 4],
 {'a': 1,
  'b': decimal.Decimal('2'),
  'c': datetime.datetime(2020, 5, 24, 8, 20),
  'd': datetime.date(1962, 1, 13),
  'e': datetime.time(11, 12, 13),
  'f': [1, 2, 3, decimal.Decimal('4')]}]

nest_base64_json = (
    b'W251bGwsIHt9LCBbMSwgMiwgMywgNF0sIHsiYSI6IDEsICJiIjogeyJfX2Ns'
    b'YXNzX25hbWVfXyI6ICI8Y2xhc3MgJ2RlY2ltYWwuRGVjaW1hbCc+IiwgIl9f'
    b'ZHVtcGVkX29ial9fIjogeyJfX3R5cGVfXyI6ICJEZWNpbWFsIiwgInZhbHVl'
    b'IjogIjIifX0sICJjIjogeyJfX2NsYXNzX25hbWVfXyI6ICI8Y2xhc3MgJ2Rh'
    b'dGV0aW1lLmRhdGV0aW1lJz4iLCAiX19kdW1wZWRfb2JqX18iOiB7Il9fdHlw'
    b'ZV9fIjogImRhdGV0aW1lIiwgInZhbHVlIjogWzIwMjAsIDUsIDI0LCA4LCAy'
    b'MCwgMF19fSwgImQiOiB7Il9fY2xhc3NfbmFtZV9fIjogIjxjbGFzcyAnZGF0'
    b'ZXRpbWUuZGF0ZSc+IiwgIl9fZHVtcGVkX29ial9fIjogeyJfX3R5cGVfXyI6'
    b'ICJkYXRlIiwgInZhbHVlIjogWzE5NjIsIDEsIDEzXX19LCAiZSI6IHsiX19j'
    b'bGFzc19uYW1lX18iOiAiPGNsYXNzICdkYXRldGltZS50aW1lJz4iLCAiX19k'
    b'dW1wZWRfb2JqX18iOiB7Il9fdHlwZV9fIjogInRpbWUiLCAidmFsdWUiOiBb'
    b'MTEsIDEyLCAxM119fSwgImYiOiBbMSwgMiwgMywgeyJfX2NsYXNzX25hbWVf'
    b'XyI6ICI8Y2xhc3MgJ2RlY2ltYWwuRGVjaW1hbCc+IiwgIl9fZHVtcGVkX29i'
    b'al9fIjogeyJfX3R5cGVfXyI6ICJEZWNpbWFsIiwgInZhbHVlIjogIjQifX1dfV0='
)

nest_base64_pickle = (
 b'gASV/QEAAAAAAABdlChOfZRdlChLAUsCSwNLBGV9lCiMAWGUSwGMAWKUjAhidWlsdGluc5SMB2dl'
 b'dGF0dHKUk5SMJ2RhdGFqdWdnbGVyLnNlcmlhbGl6ZXIuY2xhc3Nfc2VyaWFsaXplcpSMFkRlY2lt'
 b'YWxDbGFzc1NlcmlhbGl6ZXKUk5QpgZR9lIwGZm9ybWF0lIwHRGVjaW1hbJRzYowGZGVjb2RllIaU'
 b'UpR9lCiMCF9fdHlwZV9flIwHRGVjaW1hbJSMBXZhbHVllIwBMpR1hZRSlIwBY5RoCGgJjBdEYXRl'
 b'dGltZUNsYXNzU2VyaWFsaXplcpSTlCmBlH2UaA6MCGRhdGV0aW1llHNiaBCGlFKUfZQoaBSMCGRh'
 b'dGV0aW1llGgWXZQoTeQHSwVLGEsISxRLAGV1hZRSlIwBZJRoCGgJjBNEYXRlQ2xhc3NTZXJpYWxp'
 b'emVylJOUKYGUfZRoDowEZGF0ZZRzYmgQhpRSlH2UKGgUjARkYXRllGgWXZQoTaoHSwFLDWV1hZRS'
 b'lIwBZZRoCGgJjBNUaW1lQ2xhc3NTZXJpYWxpemVylJOUKYGUfZRoDowEdGltZZRzYmgQhpRSlH2U'
 b'KGgUjAR0aW1llGgWXZQoSwtLDEsNZXWFlFKUjAFmlF2UKEsBSwJLA2gSfZQoaBRoFWgWjAE0lHWF'
 b'lFKUZXVlLg==')


nest_base64_yaml = (
    b'LSBudWxsCi0ge30KLSAtIDEKICAtIDIKICAtIDMKICAtIDQKLSBhOiAxCiAg'
    b'YjogISFweXRob24vb2JqZWN0L2FwcGx5OmRlY2ltYWwuRGVjaW1hbAogIC0g'
    b'JzInCiAgYzogMjAyMC0wNS0yNCAwODoyMDowMAogIGQ6IDE5NjItMDEtMTMK'
    b'ICBlOiAhIXB5dGhvbi9vYmplY3QvYXBwbHk6ZGF0ZXRpbWUudGltZQogIC0g'
    b'ISFiaW5hcnkgfAogICAgQ3d3TkFBQUEKICBmOgogIC0gMQogIC0gMgogIC0g'
    b'MwogIC0gISFweXRob24vb2JqZWN0L2FwcGx5OmRlY2ltYWwuRGVjaW1hbAog'
    b'ICAgLSAnNCcK'
)

nest_base64_yamlcustom = (
    b'LSBudWxsCi0ge30KLSAtIDEKICAtIDIKICAtIDMKICAtIDQKLSBhOiAxCiAg'
    b'YjogITx0YWc6Z2l0aHViLmNvbS9paXNha2E1MS9kYXRhanVnZ2xlciwyMDIy'
    b'OnB5dGhvbi9kYXRhanVnZ2xlcj4KICAgIF9fY2xhc3NfbmFtZV9fOiA8Y2xh'
    b'c3MgJ2RlY2ltYWwuRGVjaW1hbCc+CiAgICBfX2R1bXBlZF9vYmpfXzoKICAg'
    b'ICAgX190eXBlX186IERlY2ltYWwKICAgICAgdmFsdWU6ICcyJwogIGM6ICE8'
    b'dGFnOmdpdGh1Yi5jb20vaWlzYWthNTEvZGF0YWp1Z2dsZXIsMjAyMjpweXRo'
    b'b24vZGF0YWp1Z2dsZXI+CiAgICBfX2NsYXNzX25hbWVfXzogPGNsYXNzICdk'
    b'YXRldGltZS5kYXRldGltZSc+CiAgICBfX2R1bXBlZF9vYmpfXzoKICAgICAg'
    b'X190eXBlX186IGRhdGV0aW1lCiAgICAgIHZhbHVlOgogICAgICAtIDIwMjAK'
    b'ICAgICAgLSA1CiAgICAgIC0gMjQKICAgICAgLSA4CiAgICAgIC0gMjAKICAg'
    b'ICAgLSAwCiAgZDogITx0YWc6Z2l0aHViLmNvbS9paXNha2E1MS9kYXRhanVn'
    b'Z2xlciwyMDIyOnB5dGhvbi9kYXRhanVnZ2xlcj4KICAgIF9fY2xhc3NfbmFt'
    b'ZV9fOiA8Y2xhc3MgJ2RhdGV0aW1lLmRhdGUnPgogICAgX19kdW1wZWRfb2Jq'
    b'X186CiAgICAgIF9fdHlwZV9fOiBkYXRlCiAgICAgIHZhbHVlOgogICAgICAt'
    b'IDE5NjIKICAgICAgLSAxCiAgICAgIC0gMTMKICBlOiAhPHRhZzpnaXRodWIu'
    b'Y29tL2lpc2FrYTUxL2RhdGFqdWdnbGVyLDIwMjI6cHl0aG9uL2RhdGFqdWdn'
    b'bGVyPgogICAgX19jbGFzc19uYW1lX186IDxjbGFzcyAnZGF0ZXRpbWUudGlt'
    b'ZSc+CiAgICBfX2R1bXBlZF9vYmpfXzoKICAgICAgX190eXBlX186IHRpbWUK'
    b'ICAgICAgdmFsdWU6CiAgICAgIC0gMTEKICAgICAgLSAxMgogICAgICAtIDEz'
    b'CiAgZjoKICAtIDEKICAtIDIKICAtIDMKICAtICE8dGFnOmdpdGh1Yi5jb20v'
    b'aWlzYWthNTEvZGF0YWp1Z2dsZXIsMjAyMjpweXRob24vZGF0YWp1Z2dsZXI+'
    b'CiAgICBfX2NsYXNzX25hbWVfXzogPGNsYXNzICdkZWNpbWFsLkRlY2ltYWwn'
    b'PgogICAgX19kdW1wZWRfb2JqX186CiAgICAgIF9fdHlwZV9fOiBEZWNpbWFs'
    b'CiAgICAgIHZhbHVlOiAnNCcK'
)

nest_base64_msgpack = (
    b'lMCAlAECAwSGoWEBoWKCrl9fY2xhc3NfbmFtZV9fuTxjbGFzcyAnZGVjaW1h'
    b'bC5EZWNpbWFsJz6uX19kdW1wZWRfb2JqX1+CqF9fdHlwZV9fp0RlY2ltYWyl'
    b'dmFsdWWhMqFjgq5fX2NsYXNzX25hbWVfX7s8Y2xhc3MgJ2RhdGV0aW1lLmRh'
    b'dGV0aW1lJz6uX19kdW1wZWRfb2JqX1+CqF9fdHlwZV9fqGRhdGV0aW1lpXZh'
    b'bHVlls0H5AUYCBQAoWSCrl9fY2xhc3NfbmFtZV9ftzxjbGFzcyAnZGF0ZXRp'
    b'bWUuZGF0ZSc+rl9fZHVtcGVkX29ial9fgqhfX3R5cGVfX6RkYXRlpXZhbHVl'
    b'k80HqgENoWWCrl9fY2xhc3NfbmFtZV9ftzxjbGFzcyAnZGF0ZXRpbWUudGlt'
    b'ZSc+rl9fZHVtcGVkX29ial9fgqhfX3R5cGVfX6R0aW1lpXZhbHVlkwsMDaFm'
    b'lAECA4KuX19jbGFzc19uYW1lX1+5PGNsYXNzICdkZWNpbWFsLkRlY2ltYWwn'
    b'Pq5fX2R1bXBlZF9vYmpfX4KoX190eXBlX1+nRGVjaW1hbKV2YWx1ZaE0'
)

nest_base64_serpent = (
    b'IyBzZXJwZW50IHV0Zi04IHB5dGhvbjMuMgpbTm9uZSx7fSxbMSwyLDMsNF0s'
    b'eydhJzoxLCdiJzp7J19fY2xhc3NfbmFtZV9fJzoiPGNsYXNzICdkZWNpbWFs'
    b'LkRlY2ltYWwnPiIsJ19fZHVtcGVkX29ial9fJzp7J19fdHlwZV9fJzonRGVj'
    b'aW1hbCcsJ3ZhbHVlJzonMid9fSwnYyc6eydfX2NsYXNzX25hbWVfXyc6Ijxj'
    b'bGFzcyAnZGF0ZXRpbWUuZGF0ZXRpbWUnPiIsJ19fZHVtcGVkX29ial9fJzp7'
    b'J19fdHlwZV9fJzonZGF0ZXRpbWUnLCd2YWx1ZSc6WzIwMjAsNSwyNCw4LDIw'
    b'LDBdfX0sJ2QnOnsnX19jbGFzc19uYW1lX18nOiI8Y2xhc3MgJ2RhdGV0aW1l'
    b'LmRhdGUnPiIsJ19fZHVtcGVkX29ial9fJzp7J19fdHlwZV9fJzonZGF0ZScs'
    b'J3ZhbHVlJzpbMTk2MiwxLDEzXX19LCdlJzp7J19fY2xhc3NfbmFtZV9fJzoi'
    b'PGNsYXNzICdkYXRldGltZS50aW1lJz4iLCdfX2R1bXBlZF9vYmpfXyc6eydf'
    b'X3R5cGVfXyc6J3RpbWUnLCd2YWx1ZSc6WzExLDEyLDEzXX19LCdmJzpbMSwy'
    b'LDMseydfX2NsYXNzX25hbWVfXyc6IjxjbGFzcyAnZGVjaW1hbC5EZWNpbWFs'
    b'Jz4iLCdfX2R1bXBlZF9vYmpfXyc6eydfX3R5cGVfXyc6J0RlY2ltYWwnLCd2'
    b'YWx1ZSc6JzQnfX1dfV0='
)

nest_base64_dill = (
 b'gASV/QEAAAAAAABdlChOfZRdlChLAUsCSwNLBGV9lCiMAWGUSwGMAWKUjAhidWlsdGluc5SMB2dl'
 b'dGF0dHKUk5SMJ2RhdGFqdWdnbGVyLnNlcmlhbGl6ZXIuY2xhc3Nfc2VyaWFsaXplcpSMFkRlY2lt'
 b'YWxDbGFzc1NlcmlhbGl6ZXKUk5QpgZR9lIwGZm9ybWF0lIwHRGVjaW1hbJRzYowGZGVjb2RllIaU'
 b'UpR9lCiMCF9fdHlwZV9flIwHRGVjaW1hbJSMBXZhbHVllIwBMpR1hZRSlIwBY5RoCGgJjBdEYXRl'
 b'dGltZUNsYXNzU2VyaWFsaXplcpSTlCmBlH2UaA6MCGRhdGV0aW1llHNiaBCGlFKUfZQoaBSMCGRh'
 b'dGV0aW1llGgWXZQoTeQHSwVLGEsISxRLAGV1hZRSlIwBZJRoCGgJjBNEYXRlQ2xhc3NTZXJpYWxp'
 b'emVylJOUKYGUfZRoDowEZGF0ZZRzYmgQhpRSlH2UKGgUjARkYXRllGgWXZQoTaoHSwFLDWV1hZRS'
 b'lIwBZZRoCGgJjBNUaW1lQ2xhc3NTZXJpYWxpemVylJOUKYGUfZRoDowEdGltZZRzYmgQhpRSlH2U'
 b'KGgUjAR0aW1llGgWXZQoSwtLDEsNZXWFlFKUjAFmlF2UKEsBSwJLA2gSfZQoaBRoFWgWjAE0lHWF'
 b'lFKUZXVlLg==')

nest_base64_bson = (
    b'5gIAAARfX2Jzb25fZm9sbG93X18A0AIAAAowAAMxAAUAAAAABDIAIQAAABAw'
    b'AAEAAAAQMQACAAAAEDIAAwAAABAzAAQAAAAAAzMAmQIAABBhAAEAAAADYgBr'
    b'AAAAAl9fY2xhc3NfbmFtZV9fABoAAAA8Y2xhc3MgJ2RlY2ltYWwuRGVjaW1h'
    b'bCc+AANfX2R1bXBlZF9vYmpfXwAoAAAAAl9fdHlwZV9fAAgAAABEZWNpbWFs'
    b'AAJ2YWx1ZQACAAAAMgAAAANjAJcAAAACX19jbGFzc19uYW1lX18AHAAAADxj'
    b'bGFzcyAnZGF0ZXRpbWUuZGF0ZXRpbWUnPgADX19kdW1wZWRfb2JqX18AUgAA'
    b'AAJfX3R5cGVfXwAJAAAAZGF0ZXRpbWUABHZhbHVlAC8AAAAQMADkBwAAEDEA'
    b'BQAAABAyABgAAAAQMwAIAAAAEDQAFAAAABA1AAAAAAAAAAADZAB6AAAAAl9f'
    b'Y2xhc3NfbmFtZV9fABgAAAA8Y2xhc3MgJ2RhdGV0aW1lLmRhdGUnPgADX19k'
    b'dW1wZWRfb2JqX18AOQAAAAJfX3R5cGVfXwAFAAAAZGF0ZQAEdmFsdWUAGgAA'
    b'ABAwAKoHAAAQMQABAAAAEDIADQAAAAAAAANlAHoAAAACX19jbGFzc19uYW1l'
    b'X18AGAAAADxjbGFzcyAnZGF0ZXRpbWUudGltZSc+AANfX2R1bXBlZF9vYmpf'
    b'XwA5AAAAAl9fdHlwZV9fAAUAAAB0aW1lAAR2YWx1ZQAaAAAAEDAACwAAABAx'
    b'AAwAAAAQMgANAAAAAAAABGYAiAAAABAwAAEAAAAQMQACAAAAEDIAAwAAAAMz'
    b'AGsAAAACX19jbGFzc19uYW1lX18AGgAAADxjbGFzcyAnZGVjaW1hbC5EZWNp'
    b'bWFsJz4AA19fZHVtcGVkX29ial9fACgAAAACX190eXBlX18ACAAAAERlY2lt'
    b'YWwAAnZhbHVlAAIAAAA0AAAAAAAAAA=='
)



class TestClass:
    def test_base64_dumps_01_1(self):
        data = str(simple_data)
        result = io.dumps(data, format='base64')
        assert result == base64_simple_encode

    def test_base64_dumps_01_2(self):
        data = str(simple_data)
        result = io.dumps(data, format='base64', encoding='utf-8')
        assert result == base64_simple

    def test_base64_dumps_01(self):
        result = io.dumps(nest_data, format='base64,json')
        assert result == nest_base64_json

    def test_base64_dumps_02(self):
        result = io.dumps(nest_data, format='base64,pickle')
        assert result == nest_base64_pickle

    def test_base64_dumps_03(self):
        result = io.dumps(nest_data, format='base64,yaml')
        assert result == nest_base64_yaml

    def test_base64_dumps_04(self):
        result = io.dumps(nest_data, format='base64,yaml:custom')
        assert result == nest_base64_yamlcustom

    def test_base64_dumps_05(self):
        result = io.dumps(nest_data, format='base64,msgpack')
        assert result == nest_base64_msgpack

    def test_base64_dumps_06(self):
        result = io.dumps(nest_data, format='base64,serpent')
        assert result == nest_base64_serpent

    def test_base64_dumps_07(self):
        result = io.dumps(nest_data, format='base64,dill')
        assert result == nest_base64_dill

    def test_base64_dumps_08(self):
        result = io.dumps(nest_data, format='base64,bson')
        assert result == nest_base64_bson

    def test_base64_encrypt_descrypt(self):
        s = io.dumps(nest_data, format='base64,json', password='python123')
        result = io.loads(s, format='base64,json', password='python123')
        assert result == nest_data


    def test_base64_loads_01(self):
        result = io.loads(nest_base64_json, format='base64,json')
        assert result ==nest_data

    def test_base64_loads_02(self):
        result = io.loads(nest_base64_pickle, format='base64,pickle')
        assert result ==nest_data

    def test_base64_loads_03(self):
        result = io.loads(nest_base64_yaml, format='base64,yaml')
        assert result ==nest_data

    def test_base64_loads_04(self):
        result = io.loads(nest_base64_yamlcustom,
                          format='base64,yaml:custom')
        assert result ==nest_data

    def test_base64_loads_05(self):
        result = io.loads(nest_base64_msgpack, format='base64,msgpack')
        assert result ==nest_data

    def test_base64_loads_06(self):
        result = io.loads(nest_base64_serpent, format='base64,serpent')
        assert result ==nest_data

    def test_base64_loads_07(self):
        result = io.loads(nest_base64_dill, format='base64,dill')
        assert result ==nest_data

    def test_base64_loads_08(self):
        result = io.loads(nest_base64_bson, format='base64,bson')
        assert result ==nest_data




    def test_base64_adict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = aDict({'a': 1, 'b': 2, 'c': 3})
        d = aDict(filepath, format='base64,json')
        assert d == expect

    def test_base64_adict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = aDict({'a': 1, 'b': 2, 'c': 3})
        d = aDict(filepath)
        assert d == expect

    def test_base64_udict_decode_case01(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = uDict({'a': 1, 'b': 2, 'c': 3})
        d = uDict(filepath, format='base64')
        assert d == expect

    def test_base64_udict_decode_case02(self):
        filepath = 'tests/serializer/data/valid-content.base64'
        expect = uDict({'a': 1, 'b': 2, 'c': 3})
        d = uDict(filepath)
        assert d == expect
