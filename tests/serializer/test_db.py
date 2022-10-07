from pathlib import Path
from glob import glob

import pytest
from datajuggler import aDict
from datajuggler import serializer as io

DBPATH = 'tests/serializer/data/users.sqlite'

try:
    import dataset

    dataset_installed = True

    test_data = [
        { 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU' },
        { 'name': "Chloe O'Brian", 'age': 0, 'belongs': 'CTU' },
        { 'name': 'Anthony Tony', 'age': 29, 'belongs': 'CTU' },
        { 'name': 'David Gilmour', 'age': 75, 'belongs': 'Pink Floyd' },
        { 'name': 'Ann Wilson', 'age': 71, 'belongs': 'Heart' },
        { 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart' },
    ]

    expect_list = [
        {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'},
        {'id': 2, 'name': "Chloe O'Brian", 'age': 0, 'belongs': 'CTU'},
        {'id': 3, 'name': 'Anthony Tony', 'age': 29, 'belongs': 'CTU'},
        {'id': 4, 'name': 'David Gilmour', 'age': 75, 'belongs': 'Pink Floyd'},
        {'id': 5, 'name': 'Ann Wilson', 'age': 71, 'belongs': 'Heart'},
        {'id': 6, 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart'}
    ]


    class TestClass:
        @classmethod
        def setup_class(cls):
            dbfile = Path(DBPATH)
            db = dataset.connect(f'sqlite:///{DBPATH}')
            table = db['users']
            for user in test_data:
                table.insert(user)
            db.commit()
            db.close()

        @classmethod
        def teardown_class(cls):
            Path(DBPATH).unlink()
            Path(f'{DBPATH}-wal').unlink()
            Path(f'{DBPATH}-shm').unlink()

        def test_read_database_case01(self):
            DSN = f'sqlite:///{DBPATH}'
            data = io.read_database(DSN)
            assert list(data) == []

        def test_read_database_case02(self):
            DSN = f'sqlite:///{DBPATH}#users'
            data = io.read_database(DSN)
            assert list(data) == expect_list

        def test_read_database_case03(self):
            DSN = f'sqlite:///{DBPATH}#users'
            expect = [{'id': 1, 'name': 'Jack Bauer',
                       'age': 55, 'belongs': 'CTU'}]
            data = io.read_database(DSN, id={'==': 1})
            assert list(data) == expect

        def test_read_database_case04(self):
            DSN = f'sqlite:///{DBPATH}#users'
            data = io.read_database(DSN, id={'==': 1}, row_type=aDict)
            users = list(data)
            assert users[0].name == 'Jack Bauer'


        def test_read_contents_case01(self):
            DSN = f'sqlite:///{DBPATH}'
            data = io.read_contents(DSN)
            assert list(data) == []

        def test_read_contents_case02(self):
            DSN = f'sqlite:///{DBPATH}#users'
            data = io.read_contents(DSN)
            assert list(data) == expect_list

        def test_read_contents_case03(self):
            DSN = f'sqlite:///{DBPATH}#users'
            expect = [{'id': 1, 'name': 'Jack Bauer',
                       'age': 55, 'belongs': 'CTU'}]
            data = io.read_contents(DSN, id={'==': 1})
            assert list(data) == expect

        def test_read_contents_case04(self):
            DSN = f'sqlite:///{DBPATH}#users'
            data = io.read_contents(DSN, id={'==': 1}, row_type=aDict)
            users = list(data)
            assert users[0].name == 'Jack Bauer'


except ImportError:
    pass
