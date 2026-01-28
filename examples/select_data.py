import sqlite3

con = sqlite3.connect('mydatabase.db')
cursor_obj = con.cursor()

cursor_obj.execute("SELECT * FROM employees")
rows = cursor_obj.fetchall()

for row in rows:
    print(row)