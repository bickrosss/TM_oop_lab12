import argparse

from db import SessionLocal
from recipe_repository import RecipeRepository, display_recipes


def main() -> None:
    parser = argparse.ArgumentParser(description="Учёт рецептов (SQLAlchemy)")
    subparsers = parser.add_subparsers(dest="command")

    add_recipe = subparsers.add_parser("add_recipe")
    add_recipe.add_argument("name")
    add_recipe.add_argument("description")

    add_ingredient = subparsers.add_parser("add_ingredient")
    add_ingredient.add_argument("recipe_id", type=int)
    add_ingredient.add_argument("name")
    add_ingredient.add_argument("amount")

    subparsers.add_parser("show_recipes")

    find = subparsers.add_parser("find_by_ingredient")
    find.add_argument("name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    session = SessionLocal()
    try:
        repo = RecipeRepository(session)

        if args.command == "add_recipe":
            repo.add_recipe(args.name, args.description)
            print("Рецепт добавлен")

        elif args.command == "add_ingredient":
            repo.add_ingredient(args.recipe_id, args.name, args.amount)
            print("Ингредиент добавлен")

        elif args.command == "show_recipes":
            display_recipes(repo.get_recipes())

        elif args.command == "find_by_ingredient":
            display_recipes(repo.get_recipes_by_ingredient(args.name))

    finally:
        session.close()


if __name__ == "__main__":
    main()