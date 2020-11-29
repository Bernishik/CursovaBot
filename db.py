import os
import sqlite3


# готовий
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    connection = None
    abs_path = os.getcwd()
    DB_path = os.path.join(abs_path, "DB")
    db_path = os.path.join(DB_path, "database.db")

    def __init__(self):
        if self.connection is None:
            if not os.path.exists(self.DB_path):
                os.makedirs('DB')
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Fep22(day CHARACTER UNIQUE,first VARCHAR ,second VARCHAR ,thirth VARCHAR ,"
            "fourth VARCHAR ,fifth VARCHAR ,sixth VARCHAR , seventh VARCHAR ,eighth VARCHAR )")
        self.connection.commit()

    def get_rozk(self, group,day):
        self.cursor.execute("SELECT * FROM "+ group + " WHERE day = (?)",(day,))
        rozk = {}
        for day in self.cursor.fetchall():
            rozk = {
                "1": day[1],
                "2": day[2],
                "3": day[3],
                "4": day[4],
                "5": day[5],
                "6": day[6],
                "7": day[7],
                "8": day[8],
                "group": group,
                "day":day[0]
            }
        return rozk

    def set_rozk(self, group, json):
        for day in json:
            self.cursor.execute(
                'INSERT OR IGNORE  INTO ' + group + '(day,first ,second ,thirth,fourth,fifth,sixth,seventh,eighth) VALUES (?,?,?,?,?,?,?,?,?)',
                (day, json[day]["1"], json[day]["2"], json[day]["3"], json[day]["4"], json[day]["5"], json[day]["6"],json[day]["7"],json[day]["8"]))
        self.connection.commit()


json = {
    "monday": {
        "1": "Вишмат",
        "2": "",
        "3": "Англійська",
        "4": "Коман",
        "5": "",
        "6": "Бази Даних"
    },
    "wednesday": {
        "1": "Вишмат",
        "2": "",
        "3": "Англійська",
        "4": "Коман",
        "5": "",
        "6": "Бази Даних"
    }
}


