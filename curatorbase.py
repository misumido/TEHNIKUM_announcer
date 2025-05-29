import sqlite3
from datetime import datetime
connection = sqlite3.connect("cdb.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS groups (name TEXT, tg_id INTEGER, reg_date DATETIME);")
connection.commit()

def check_name(name):
    connection = sqlite3.connect("cdb.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT name FROM groups WHERE name=?;", (name,)).fetchone()
    if checker:
        return True
    return False
def add_group(name, tg_id):
    connection = sqlite3.connect("cdb.db")
    sql = connection.cursor()
    checker = check_name(name)
    if checker == False:
        sql.execute("INSERT INTO groups (name, tg_id, reg_date) "
                    "VALUES (?, ?, ?);", (name, tg_id, datetime.now()))
        connection.commit()
        return True
    else:
        return False
def get_groups():
    connection = sqlite3.connect("cdb.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT name, tg_id FROM groups;").fetchall()
    return checker

