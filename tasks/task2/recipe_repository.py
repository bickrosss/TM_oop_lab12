from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

try:
    from tasks.task2.db import Base, engine
except ImportError:
    from db import Base, engine


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    ingredients = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(String)

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="ingredients")


Base.metadata.create_all(engine)


class RecipeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_recipe(self, name: str, description: str) -> None:
        recipe = Recipe(name=name, description=description)
        self.session.add(recipe)
        self.session.commit()

    def add_ingredient(self, recipe_id: int, name: str, amount: str) -> None:
        ing = Ingredient(recipe_id=recipe_id, name=name, amount=amount)
        self.session.add(ing)
        self.session.commit()

    def get_recipes(self):
        return self.session.query(Recipe).all()

    def get_recipes_by_ingredient(self, ingredient_name: str):
        return (
            self.session.query(Recipe)
            .join(Ingredient)
            .filter(Ingredient.name.like(f"%{ingredient_name}%"))
            .all()
        )


def display_recipes(recipes):
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
