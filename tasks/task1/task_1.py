import argparse
from pathlib import Path

from recipe_repository import RecipeRepository, display_recipes


def main() -> None:
    parser = argparse.ArgumentParser(description="Учёт рецептов")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    add_recipe = subparsers.add_parser("add_recipe", help="Добавить рецепт")
    add_recipe.add_argument("name", help="Название рецепта")
    add_recipe.add_argument("description", help="Описание")

    add_ingredient = subparsers.add_parser("add_ingredient", help="Добавить ингредиент")
    add_ingredient.add_argument("recipe_id", type=int, help="ID рецепта")
    add_ingredient.add_argument("name", help="Название ингредиента")
    add_ingredient.add_argument("amount", help="Количество")

    subparsers.add_parser("show_recipes", help="Показать все рецепты")

    by_ing = subparsers.add_parser(
        "find_by_ingredient", help="Найти рецепты по ингредиенту"
    )
    by_ing.add_argument("name", help="Название ингредиента")

    args = parser.parse_args()

    repo = RecipeRepository(Path("recipes.db"))

    if args.command == "add_recipe":
        repo.add_recipe(args.name, args.description)
        print(f"Рецепт '{args.name}' добавлен")

    elif args.command == "add_ingredient":
        repo.add_ingredient(args.recipe_id, args.name, args.amount)
        print("Ингредиент добавлен")

    elif args.command == "show_recipes":
        display_recipes(repo.get_recipes())

    elif args.command == "find_by_ingredient":
        recipes = repo.get_recipes_by_ingredient(args.name)
        display_recipes(recipes)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
