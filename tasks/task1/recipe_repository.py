import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Recipe:
    id: int
    name: str
    description: str

    def str(self) -> str:
        return f"ID: {self.id:>3} | Название: {self.name:<20} | Описание: {self.description}"


@dataclass(frozen=True)
class Ingredient:
    id: int
    recipe_id: int
    name: str
    amount: str

    def str(self) -> str:
        return (
            f"ID: {self.id:>3} | Рецепт: {self.recipe_id:>3} | "
            f"Ингредиент: {self.name:<15} | Кол-во: {self.amount}"
        )


class RecipeRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._create_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _create_db(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    amount TEXT,
                    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                )
            """
            )

    def add_recipe(self, name: str, description: str) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipes (name, description) VALUES (?, ?)",
                (name, description),
            )

    def add_ingredient(self, recipe_id: int, name: str, amount: str) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ingredients (recipe_id, name, amount)
                VALUES (?, ?, ?)
            """,
                (recipe_id, name, amount),
            )

    def get_recipes(self) -> list[Recipe]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description FROM recipes")
            rows = cursor.fetchall()
            return [Recipe(*row) for row in rows]

    def get_recipes_by_ingredient(self, ingredient_name: str) -> list[Recipe]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT r.id, r.name, r.description
                FROM recipes r
                JOIN ingredients i ON r.id = i.recipe_id
                WHERE i.name LIKE ?
            """,
                (f"%{ingredient_name}%",),
            )
            rows = cursor.fetchall()
            return [Recipe(*row) for row in rows]


def display_recipes(recipes: list[Recipe]) -> None:
    if not recipes:
        print("Список рецептов пуст.")
        return

    line = f"+-{'-' * 4}-+-{'-' * 20}-+-{'-' * 25}+"
    print(line)
    print(f"| {'ID':^4} | {'Название':^20} | {'Описание':^25} |")
    print(line)
    for r in recipes:
        print(f"| {r.id:^4} | {r.name:^20} | {r.description:^25} |")

    print(line)