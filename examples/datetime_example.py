import sqlite3
import datetime
def adapt_date(date_obj):
    return date_obj.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date)

con = sqlite3.connect('mydatabase.db')
cursor_obj = con.cursor()

cursor_obj.execute("""
    CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER, 
        name TEXT, 
        date TEXT  -- Используем TEXT вместо DATE для совместимости
    )
""")

data = [
    (1, "Ridesharing", datetime.date(2017, 1, 2)),
    (2, "Water Purifying", datetime.date(2018, 3, 4))
]

cursor_obj.executemany("INSERT INTO assignments VALUES(?, ?, ?)", data)
con.commit()
print("Данные с датами успешно добавлены!")
con.close()