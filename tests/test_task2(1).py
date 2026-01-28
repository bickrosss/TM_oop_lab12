
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Добавляем путь к корню проекта в sys.path
project_root = Path(__file__).resolve().parents[1]  # Поднимаемся на один уровень вверх
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    
from tasks.task2.recipe_repository import Base, RecipeRepository, display_recipes, Recipe, Ingredient


@pytest.fixture
def session():
    # in-memory sqlite database для тестов
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()


def test_add_and_get_recipe(session):
    repo = RecipeRepository(session)
    repo.add_recipe("Пицца", "С помидорами")
    recipes = repo.get_recipes()
    assert len(recipes) == 1
    assert recipes[0].name == "Пицца"
    assert recipes[0].description == "С помидорами"


def test_add_ingredient_and_find(session):
    repo = RecipeRepository(session)
    repo.add_recipe("Пицца", "С помидорами")
    recipes = repo.get_recipes()
    rid = recipes[0].id

    repo.add_ingredient(rid, "Томат", "100 г")
    found = repo.get_recipes_by_ingredient("Томат")
    assert len(found) == 1
    assert found[0].id == rid
