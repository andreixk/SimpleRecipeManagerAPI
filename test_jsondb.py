import pytest
from fastapi.testclient import TestClient
from unittest import mock
from unittest.mock import mock_open
import json
from jsondb import PrimitiveStorage, ObjectStorage
from conftest import Stub

class TestStorage():
    @pytest.mark.parametrize('Storage,fake_data', [
        (PrimitiveStorage, ['a','b']), 
        (ObjectStorage, [{'a':'b'}])
    ])
    def test_gets_list_of_items_from_file(self, Storage, fake_data):
        collection = 'hello'
        mocked_open = mock_open(read_data=json.dumps(fake_data))
        with mock.patch('builtins.open', mocked_open) as open_stub:
            store = Storage(collection)
            rs = store.read()
        assert rs == fake_data
        assert Stub(open_stub).called_with(f'{collection}.json', 'r')

    @pytest.mark.parametrize('Storage,fake_data', [
        (PrimitiveStorage, ['a','b','c','d']), 
        (ObjectStorage, [{'a':'b'},{'c':'d'},{'e':'f'},{'g':'h'}])
    ])
    def test_can_limit_number_of_items_returned(self, Storage, fake_data):
        collection = 'hello'
        mocked_open = mock_open(read_data=json.dumps(fake_data))
        start=1
        end=3
        with mock.patch('builtins.open', mocked_open) as open_stub:
            store = Storage(collection)
            rs = store.read(start=start,end=end)
        assert rs == fake_data[start:end]
        assert Stub(open_stub).called_with(f'{collection}.json', 'r')

    @pytest.mark.parametrize('Storage,input_data,expected_data', [
        (PrimitiveStorage, ['a','b', 'c'], ['a', 'b', 'c']), 
        (ObjectStorage, {'a':'b'}, [{'a':'b'}])
    ])
    @mock.patch('jsondb.json.dump')
    def test_adds_items_to_file(self, jdump_stub, Storage, input_data, expected_data):
        collection = 'byebye'
        mocked_open = mock_open()
        with mock.patch('builtins.open', mocked_open) as open_stub:
            Storage(collection).create(input_data)
        assert Stub(open_stub).called_with(f'{collection}.json', 'w')
        assert Stub(jdump_stub).called_with(expected_data, mocked_open())

    @mock.patch('jsondb.json.dump')
    def test_primitive_adds_unique_sorted_items_to_file(self, jdump_stub):
        collection = 'byebye'
        input_data = ['b', 'b', 'c', 'a', 'a']
        expected_data = ['a','b','c']
        mocked_open = mock_open()
        with mock.patch('builtins.open', mocked_open) as open_stub:
            PrimitiveStorage(collection).create(input_data)
        assert Stub(jdump_stub).called_with(expected_data, mocked_open())
