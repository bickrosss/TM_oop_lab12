import sqlite3

con = sqlite3.connect('mydatabase.db')
cursor_obj = con.cursor()

# Вставка данных напрямую в запрос
cursor_obj.execute("INSERT INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')")

# Вставка данных с использованием заполнителей ?
entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
cursor_obj.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", entities)

con.commit()