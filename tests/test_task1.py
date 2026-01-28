import os
import tempfile
import pytest
from pathlib import Path

from tasks.task1.recipe_repository import RecipeRepository, display_recipes


@pytest.fixture
def temp_db():
    # Создаем временный файл БД
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    yield Path(db_path)
    os.remove(db_path)


def test_add_and_get_recipe(temp_db):
    repo = RecipeRepository(temp_db)
    repo.add_recipe("Паста", "С сыром")
    recipes = repo.get_recipes()
    assert len(recipes) == 1
    assert recipes[0].name == "Паста"
    assert recipes[0].description == "С сыром"


def test_add_ingredient_and_find(temp_db):
    repo = RecipeRepository(temp_db)
    repo.add_recipe("Паста", "С сыром")
    recipes = repo.get_recipes()
    rid = recipes[0].id

    repo.add_ingredient(rid, "Сыр", "200 г")
    found = repo.get_recipes_by_ingredient("Сыр")
    assert len(found) == 1
    assert found[0].id == rid
