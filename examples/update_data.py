import sqlite3

con = sqlite3.connect('mydatabase.db')
cursor_obj = con.cursor()

cursor_obj.execute("UPDATE employees SET name = 'Rogers' WHERE id = 2")
con.commit()