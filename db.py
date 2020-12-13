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

    def get_group_list(self):
        collection = self.db['groups']
        data = collection.find({},{"_id":0})
        return list(data)

    def get_group_list_by_kurs(self,kurs):
        collection = self.db['groups']
        data = collection.find({"kurs":int(kurs)}, {"_id": 0})
        return list(data)

    def get_rozk(self, group,day):
        collection = self.db[group]
        return collection.find_one({"day":day},{"_id":0})

    def get_group_rozk(self, group):
        collection = self.db[group]
        return list(collection.find({},{"_id":0}))

    def set_rozk(self, group, json):
        collection = self.db[group]
        collection.update({"day":json['day']},json,upsert=True)
        # collection.insert_one(json)

    # users method

    def get_all_users(self):
        collection = self.db['users']
        return collection.find({},{"_id":0})

    def add_user(self,data):
        collection = self.db['users']
        collection.update({"chat_id":data["chat_id"]},data,upsert=True)

    def get_user_by_chat_id(self,chat_id):
        collection = self.db['users']
        return collection.find_one({"chat_id":chat_id},{"_id":0})

    def update_user(self,data):
        collection = self.db['users']
        collection.update({"chat_id":data["chat_id"]},data,upsert=True)

    def remove_user(self,chat_id):
        collection = self.db['users']
        collection.delete_one({"chat_id":chat_id})

