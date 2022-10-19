from pathlib import Path

import pytest
from datajuggler import serializer as io


class TestClass:
    def test_parse_format_case01(self):
        result = io.core.parse_format('yaml')
        assert tuple(result) == ( 'yaml', '', 'yaml' )

    def test_parse_format_case02(self):
        result = io.core.parse_format('yaml:legacy')
        assert tuple(result) == ( 'yaml:legacy', '', 'yaml' )

    def test_parse_format_case03(self):
        result = io.core.parse_format('yaml:custom')
        assert tuple(result) == ( 'yaml:custom', '', 'yaml' )

    def test_parse_format_case04(self):
        result = io.core.parse_format('yaml:custom,,yml')
        assert tuple(result) == ( 'yaml:custom', '', 'yml' )

    def test_parse_format_case05(self):
        result = io.core.parse_format('base64,pickle')
        assert tuple(result) == ( 'base64', 'pickle', 'base64' )

    def test_parse_format_case06(self):
        result = io.core.parse_format('base64,pickle,b64')
        assert tuple(result) == ( 'base64', 'pickle', 'b64' )

    def test_parse_format_case07(self):
        result = io.core.parse_format('msgpack')
        assert tuple(result) == ( 'msgpack', '', 'msgpack' )

    def test_parse_format_case08(self):
        result = io.core.parse_format('json')
        assert tuple(result) == ( 'json', '', 'json' )

    def test_parse_format_case09(self):
        result = io.core.parse_format('json:custom')
        assert tuple(result) == ( 'json:custom', '', 'json' )

    def test_parse_format_case10(self):
        result = io.core.parse_format('csv')
        assert tuple(result) == ( 'csv', '', 'csv' )

    def test_parse_format_case11(self):
        result = io.core.parse_format('bson')
        assert tuple(result) == ( 'bson', '', 'bson' )

    def test_parse_format_case12(self):
        result = io.core.parse_format('toml')
        assert tuple(result) == ( 'toml', '', 'toml' )

    def test_parse_format_case13(self):
        result = io.core.parse_format('xml')
        assert tuple(result) == ( 'xml', '', 'xml' )

    def test_parse_format_case14(self):
        result = io.core.parse_format('querystring')
        assert tuple(result) == ( 'querystring', '', 'querystring' )

    def test_parse_format_case15(self):
        result = io.core.parse_format('querystring,,qs')
        assert tuple(result) == ( 'querystring', '', 'qs' )

    def test_parse_format_case16(self):
        result = io.core.parse_format('plist')
        assert tuple(result) == ( 'plist', '', 'plist' )

    def test_parse_format_case17(self):
        result = io.core.parse_format('yaml:custom', 'yml')
        assert tuple(result) == ( 'yaml:custom', '', 'yml' )

