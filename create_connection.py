import sqlite3

# Создание соединения с файлом базы данных
con = sqlite3.connect('mydatabase.db')

# Или создание базы данных в оперативной памяти
con = sqlite3.connect(':memory:')