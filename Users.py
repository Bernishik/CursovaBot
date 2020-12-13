from db import DataBase
class Users:
    def __init__(self):
        self.db = DataBase()
        self.get_all_users()
    def get_all_users(self):
        return list(self.db.get_all_users())

    def add_user(self,chat_id,group,username,user_id,lang,date):
        self.db.add_user({"chat_id":chat_id,"group":group,"username":username,"lang":lang,"user_id": user_id,"date":date})

    def get_user_by_chat_id(self,chat_id):
        return self.db.get_user_by_chat_id(chat_id)

    def update_user(self,chat_id,group,username,user_id,lang,date):
        self.db.update_user({"chat_id":chat_id,"group":group,"username":username,"lang":lang,"user_id": user_id,"date":date})

    def remove_user(self,chat_id):
        self.db.remove_user(chat_id)




