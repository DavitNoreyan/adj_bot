import sqlite3

from constants import Constants


class Database:
    def __init__(self):
        # print(Constants.DB_PATH)
        # self.conn = sqlite3.connect(Constants.DB_PATH)
        # self.cursor = self.conn.cursor()
        with sqlite3.connect(Constants.DB_PATH) as self.conn:
            self.cursor = self.conn.cursor()

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS users " \
                "(id integer primary key AUTOINCREMENT, " \
                "username varchar(30) not null, " \
                "password varchar(30) not null, " \
                "user_id varchar(30) not null," \
                "user_hash varchar(30) not null," \
                "chance_count varchar(30));"
        self.cursor.execute(query)

    def insert_user(self, username, password, user_id, user_hash):
        query = f'INSERT INTO users (username, password, user_id, user_hash) values("{username}", "{password}", "{user_id}", "{user_hash}");'
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_users_from_db(self):
        query = 'SELECT * FROM users;'
        users = self.cursor.execute(query).fetchall()
        return users

    def get_one_user(self, user_id):
        query = f'SELECT * FROM users WHERE user_id={user_id}'
        user = self.cursor.execute(query).fetchone()
        return user

    def delete_user_from_table(self, id, username):
        query = f'DELETE FROM users where user_id="{id}" AND username ="{username}";'
        self.cursor.execute(query)
        self.conn.commit()

    def update_value_in_table(self, chance_count, user_id):
        query = f'UPDATE users SET chance_count = "{chance_count}" WHERE user_id = {user_id};'
        self.cursor.execute(query)
        self.conn.commit()






if __name__ == '__main__':
    db = Database()
    db.create_table()
    # for i in range(10):
    #     db.insert_user('davit', 'noreyan', f'123456{i}')
    # print(db.get_all_users_from_db())
    # print(db.get_one_user('123456'))
    # # db.delete_user_from_table(1)
