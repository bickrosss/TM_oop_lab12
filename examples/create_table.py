import sqlite3

con = sqlite3.connect('mydatabase.db')
cursor_obj = con.cursor()

cursor_obj.execute("""
    CREATE TABLE employees (
        id integer PRIMARY KEY,
        name text,
        salary real,
        department text,
        position text,
        hireDate text)
""")
con.commit()