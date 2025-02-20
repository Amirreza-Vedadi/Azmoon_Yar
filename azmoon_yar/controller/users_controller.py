from model.entity.users import *
from model.da.users_da import *
import re

class Users_controller:
    def validate_user(self, id, role):
        u_d = Users_da()
        user = u_d.find_one(id)

        if user and user[3] == role:
            return True
        return False

    def search(self, id):
        u_d = Users_da()
        user = u_d.find_one(id)
        return user

    def save(self, id, name, family, role):
        if not re.fullmatch(r'\d{10}', id):
            return {"status": "error", "message": "کد ملی باید 10 رقم و فقط عدد باشد"}

        u_d = Users_da()
        existing_user = u_d.find_one(id)
        if existing_user:
            return {"status": "error", "message": "کد ملی تکراری است"}

        users = Users(id, name, family, role)
        u_d.save(users)
        return {"status": "success", "message": "اطلاعات ذخیره شد"}

    def edit(self, id, name, family, role):
        users = Users(id, name, family, role)
        u_d = Users_da()
        u_d.edit(users)

    def remove(self, id):
        u_d = Users_da()
        u_d.remove(id)

    def find_all(self):
        u_d = Users_da()
        users_list = u_d.find_all()
        return users_list
