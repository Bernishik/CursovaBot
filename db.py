from pymongo import MongoClient


# готовий
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    connection = None
    def __init__(self):
        if self.connection is None:
            self.connection = MongoClient("mongodb://127.0.0.1:27017")
            self.db = self.connection['rozk']

    def get_rozk(self, group,day):
        collection = self.db[group]
        return collection.find_one({"day":day},{"_id":0})

    def set_rozk(self, group, json):
        collection = self.db[group]
        collection.update({"day":json['day']},json,upsert=True)
        # collection.insert_one(json)