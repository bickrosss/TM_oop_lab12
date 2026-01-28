import sqlite3
import argparse
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Post:
    id: int
    title: str

@dataclass
class Worker:
    name: str
    post: str
    year: int

class StaffRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_title TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_name TEXT NOT NULL,
                post_id INTEGER NOT NULL,
                worker_year INTEGER NOT NULL,
                FOREIGN KEY(post_id) REFERENCES posts(post_id)
            )
        """)
        conn.commit()
        conn.close()

    def get_or_create_post(self, title: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT post_id FROM posts WHERE post_title = ?", (title,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("INSERT INTO posts (post_title) VALUES (?)", (title,))
            post_id = cursor.lastrowid
            conn.commit()
        else:
            post_id = row[0]
        conn.close()
        return post_id

    def add_worker(self, name: str, post: str, year: int):
        post_id = self.get_or_create_post(post)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workers (worker_name, post_id, worker_year)
            VALUES (?, ?, ?)
        """, (name, post_id, year))
        conn.commit()
        conn.close()

    def get_all_workers(self) -> list[Worker]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT workers.worker_name, posts.post_title, workers.worker_year
            FROM workers
            INNER JOIN posts ON posts.post_id = workers.post_id
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Worker(name=row[0], post=row[1], year=row[2]) for row in rows]

    def select_by_period(self, period: int) -> list[Worker]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT workers.worker_name, posts.post_title, workers.worker_year
            FROM workers
            INNER JOIN posts ON posts.post_id = workers.post_id
            WHERE (strftime('%Y', date('now')) - workers.worker_year) >= ?
        """, (period,))
        rows = cursor.fetchall()
        conn.close()
        return [Worker(name=row[0], post=row[1], year=row[2]) for row in rows]

def display_workers(workers: list[Worker]):
    if not workers:
        print("Список работников пуст.")
        return
    # Вывод таблицы в консоль
    # ... (код для форматирования таблицы)

def main():
    parser = argparse.ArgumentParser(description="Учёт сотрудников")
    parser.add_argument("--db", default="workers.db", help="Путь к базе данных")
    subparsers = parser.add_subparsers(dest="command")

    # Подкоманда add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--post", required=True)
    add_parser.add_argument("--year", type=int, required=True)

    # Подкоманда display
    subparsers.add_parser("display")

    # Подкоманда select
    select_parser = subparsers.add_parser("select")
    select_parser.add_argument("--period", type=int, required=True)

    args = parser.parse_args()
    repo = StaffRepository(args.db)

    if args.command == "add":
        repo.add_worker(args.name, args.post, args.year)
        print("Сотрудник добавлен.")
    elif args.command == "display":
        display_workers(repo.get_all_workers())
    elif args.command == "select":
        display_workers(repo.select_by_period(args.period))

if __name__ == "__main__":
    main()