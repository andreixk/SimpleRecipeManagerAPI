import json
import traceback
class BaseStorage():
    def __init__(self, db_name):
        self.__db = db_name
    def read(self, start=0, end=None):
        try:
            with open(f'{self.__db}.json', 'r') as f:
                return json.load(f)[start:end]
        except Exception as e:
            return []
    def write(self, data):
        with open(f'{self.__db}.json', 'w') as f:
            json.dump(data, f)

class PrimitiveStorage(BaseStorage):
    def create(self, item):
        existing_items = set(super().read())
        existing_items |= set(item)
        super().write(sorted(list(existing_items)))

class ObjectStorage(BaseStorage):
    def create(self, item):
        existing_items = super().read()
        existing_items += [item]
        super().write(existing_items)
