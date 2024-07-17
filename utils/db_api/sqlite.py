import sqlite3


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")


U_CID = 0
U_STEP = 1
U_FULL_NAME = 2
U_IS_BLOCKED = 3
U_PHONE = 4


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
CREATE TABLE Users (
    cid varchar(255) NOT NULL,
    full_name varchar(255) NOT NULL ,
    is_blocked int(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (cid)
);
"""
        self.execute(sql, commit=True)

    def add_user(self, cid, is_blocked, full_name, phone, lan):
        sql = """INSERT INTO Users(cid, is_blocked,full_name,phone,lan) VALUES(?, ?,?,?,?)"""
        self.execute(sql, parameters=(cid, is_blocked, full_name, phone, lan), commit=True)

    def select_users_all_ids(self):
        return self.execute("SELECT cid FROM Users WHERE is_blocked=0;", fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def format_update_args(self, kwargs):
        set_clause = ", ".join([f"{key} = ?" for key in kwargs if key != "id"])
        parameters = [value for key, value in kwargs.items() if key != "id"]
        return set_clause, parameters

    def update_user(self, id, **kwargs):
        if not kwargs:
            return None

        set_clause, parameters = self.format_update_args(kwargs)
        print(set_clause)
        print(parameters)
        sql = f"UPDATE Users SET {set_clause} WHERE cid = ?"
        parameters.append(id)
        params = tuple(parameters)
        return self.execute(sql, parameters=params, commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_active_users(self):
        return self.execute("SELECT COUNT(*) FROM Users WHERE is_blocked=0;", fetchone=True)

    def select_user_all(self):
        return self.execute('SELECT * FROM Users;', fetchall=True)

    def select_menu_all(self, menu):
        sql = f"""SELECT * FROM menus WHERE menu=?;"""
        return self.execute(sql, parameters=(menu), fetchall=True)

    def select_user_all_body(self):
        return self.execute('SELECT cid, full_name, phone, is_blocked FROM Users;', fetchall=True)

    def update_user_block(self, is_blocked, cid):
        sql = f"""UPDATE Users SET is_blocked=? WHERE cid=?"""
        return self.execute(sql, parameters=(is_blocked, cid), commit=True)

    def update_user_phone(self, phone, cid):
        sql = f"""UPDATE Users SET phone=? WHERE cid=?"""
        return self.execute(sql, parameters=(phone, cid), commit=True)

    def drop_table(self):
        return self.execute(f"DROP TABLE Users", commit=True)

    def delete_user(self, cid):
        return self.execute(f'DELETE FROM Users WHERE cid=?', parameters=(cid,), commit=True)

    def add_text(self, caption, button):
        sql = """INSERT INTO Texts(caption, button) VALUES(?, ?)"""
        self.execute(sql, parameters=(caption, button), commit=True)

    def add_channel(self, channel_id, channel_name, channel_users):
        sql = """INSERT INTO Channels(channel_id, channel_name,channel_users) VALUES(?, ?, ?)"""
        self.execute(sql, parameters=(channel_id, channel_name, channel_users), commit=True)

    def add_admin(self, cid, name):
        sql = """INSERT INTO Admins(cid, name) VALUES(?, ?)"""
        self.execute(sql, parameters=(cid, name), commit=True)

    def delete_texts(self):
        sql = """DELETE FROM Texts"""
        self.execute(sql, commit=True)

    def select_all_channels(self):
        return self.execute("SELECT * FROM Channels", fetchall=True)

    def select_all_channel(self):
        return self.execute("SELECT channel_id FROM Channels", fetchall=True)

    def select_all_adminss(self):
        return self.execute("SELECT cid FROM Admins", fetchall=True)

    def select_all_from_texts(self):
        return self.execute("SELECT * FROM Texts", fetchall=True)

    def select_all_admins(self):
        return self.execute("SELECT * FROM Admins", fetchall=True)

    def select_all_admin(self, call):
        return self.execute(f"SELECT * FROM Admins WHERE name = {call}")

    def delete_admin(self, cid):
        return self.execute(f'DELETE FROM Admins WHERE cid=?', parameters=(cid,), commit=True)

    def delete_channel(self, channel):
        return self.execute(f'DELETE FROM Channels WHERE channel_id=?', parameters=(channel,), commit=True)

    def select_menu_buttons(self, menu):
        sql = "SELECT menu_button_uz FROM menus WHERE menu=?"
        return self.execute(sql, (menu,), fetchall=True)

    def select_menu_content(self, button_text, lan):
        if lan == 'uz':
            column = 'menu_button_uz'
            column2 = 'content_uz'
        elif lan == 'ru':
            column = 'menu_button_ru'
            column2 = 'content_ru'
        else:
            column = 'menu_button_kr'
            column2 = 'content_kr'
        sql = f"SELECT {column2} FROM menus WHERE {column}=?"
        return self.execute(sql, (button_text,), fetchall=True)

    def add_menu_buttons(self, menu, menu_button_uz, menu_button_ru, menu_button_kr, content_uz, content_ru,
                         content_kr):
        sql = """INSERT INTO menus(menu, menu_button_uz, menu_button_ru, menu_button_kr, content_uz, content_ru, content_kr) VALUES(?, ?, ?, ?, ?, ?, ?)"""
        self.execute(sql, parameters=(
            menu, menu_button_uz, menu_button_ru, menu_button_kr, content_uz, content_ru, content_kr), commit=True)

    def delete_menu_buttons(self, menu):
        sql = "DELETE FROM menus WHERE menu=?"
        return self.execute(sql, (menu,), commit=True)


db = Database()

try:
    db.create_table_users()
except Exception as e:
    print(e)
