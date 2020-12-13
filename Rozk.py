import glob
import os
import shutil

import excel2img

from Xlsmwork import Xlsmwork
from db import DataBase

class Rozk:

    def __init__(self):
        self.db = DataBase()
        self.load_data()

    def clear_tmp(self):
        files = glob.glob('./tmp/*')
        for f in files:
            os.remove(f)
        files = glob.glob('./rozk/*')
        for f in files:
            os.remove(f)

    def load_data(self):
            for group in  self.db.get_group_list():
                g = group["group"] + str(group["kurs"]) + str(group["group_num"]) + "-" + str(group["subgroup"])

                try:
                    path = self.load_xlsx_for_group(g)
                    self.load_rozk_for_group(g)
                except IndexError:
                    print("no such files in " + g)


    def get_day_rozk(self,group,day):
        # повертає шлях зображення
        return os.path.join(os.path.join(os.path.abspath("rozk"), str(group)),str(day)+".png")


    def load_xlsx_for_group(self,group):
        # Підгружає розклад як xlsx
        work = Xlsmwork()
        work.fill_full_rozk(self.db.get_group_rozk(group))
        path =work.save_file(str(group) + ".xlsx")
        return path

    def load_rozk_for_group(self,group):
        # завантажує в папку rozk зображення всього тижня для групи
        path  =os.path.join(os.path.abspath("tmp"), str(group)+".xlsx")
        out_path = os.path.join(os.path.abspath("rozk"), str(group))
        os.makedirs(out_path,exist_ok=True)
        sheets = Xlsmwork.get_sheet_len(path)
        for sheet in sheets:
            excel2img.export_img(path, os.path.join(out_path ,sheet+".png"),page=sheet)

    def get_group_list(self):
        return self.db.get_group_list()

    def get_group_list_by_kurs(self,kurs):
        return self.db.get_group_list_by_kurs(kurs)


dirpath="./tmp"
for filename in os.listdir(dirpath):
    filepath = os.path.join(dirpath, filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)

# db = DataBase()
# print(db.get_rozk("Fep22", "monday"))
# data = {
#     "1": {
#         "always": "",
#         "doubled": {
#             "even": "matan123",
#             "odd": "ывпыв"
#         }
#
#     },
#     "2": {"always": "kek",
#           "doubled": None},
#     "3": {"always": "Англійська",
#           "doubled": None},
#     "4": {"always": "Коман",
#           "doubled": None
#           },
#     "5": {"always": "",
#           "doubled": None
#           },
#     "6": {"always": "Бази Даних",
#           "doubled": None
#           },
#     "7": {"always": "",
#           "doubled": None
#           },
#     "8": {"always": "",
#           "doubled": None
#           },
#     "group": "ФеП-21",
#     "day": "Вівторок"
#
# }
#
#
#
