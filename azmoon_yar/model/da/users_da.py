import mysql.connector
from model.entity.users import Users
class Users_da:
    def connect(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Av3032941??",
            database="azmoon_yar"
        )
        self.cursor1 = self.db.cursor()

    def disconnect(self):
        self.cursor1.close()
        self.db.close()

    def save(self, users):
        self.connect()
        self.cursor1.execute(
            "INSERT INTO users (id, name, family, role) VALUES (%s, %s, %s, %s)",
            [users.id, users.name, users.family, users.role]
        )
        self.db.commit()
        self.disconnect()

    def edit(self, users):
        self.connect()
        self.cursor1.execute(
            "UPDATE users SET name=%s, family=%s, role=%s WHERE id=%s",
            [users.name, users.family, users.role, users.id]
        )
        self.db.commit()
        self.disconnect()

    def remove(self, id):
        self.connect()
        self.cursor1.execute("DELETE FROM users WHERE id=%s", [id])
        self.db.commit()
        self.disconnect()

    def find_all(self):
        self.connect()
        self.cursor1.execute("SELECT * FROM users")
        userslist = self.cursor1.fetchall()
        self.disconnect()
        return userslist

    def find_one(self, id):
        self.connect()
        self.cursor1.execute("SELECT * FROM users WHERE id = %s", [id])
        user = self.cursor1.fetchone()
        self.disconnect()
        return user
