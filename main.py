from core.runner import make_food_recipe
from utils.diet import Diet
from utils.difficulty import Difficulty
from constants.output import *
import asyncio


def choose_diet():
    print("🍽️ Choose a diet from the following options:")
    for i, diet in enumerate(Diet, 1):
        print(f"{i}. {diet.name} 🍎" if diet == Diet.VEGAN or diet == Diet.VEGETARIAN else f"{i}. {diet.name} 🥩")

    choice = int(input("Please enter the number corresponding to your choice: "))
    try:
        selected_diet = Diet(choice)
        return selected_diet
    except ValueError:
        print("❌ Invalid choice. Please try again.")
        return choose_diet()



def choose_difficulty():
    print("⚡ Choose a difficulty level from the following options:")
    for i, difficulty in enumerate(Difficulty, 1):
        print(f"{i}. {difficulty.name} 💪")

    choice = int(input("Please enter the number corresponding to your choice: "))
    try:
        selected_difficulty = Difficulty(choice)
        return selected_difficulty
    except ValueError:
        print("❌ Invalid choice. Please try again.")
        return choose_difficulty()



def main():
    print("👋 Welcome! Let's start by choosing your diet and difficulty level.")

    diet = choose_diet()
    print(f"✅ You have chosen the diet: {diet.name}\n")

    difficulty = choose_difficulty()
    print(f"✅ You have chosen the difficulty level: {difficulty.name}\n")


    try:
        result = asyncio.run(make_food_recipe(diet, difficulty))
        print("🎉 Here is your generated recipe! 🍽️")
        print("Title: " + result[RECIPE_TITLE_KEY] + "\n")
        print("Instructions:\n" + result[RECIPE_INSTRUCTIONS_KEY] + "\n")
        print("Ingredients:\n" + result[RECIPE_INGREDIENTS_KEY] + "\n")
        print("Total cost: " + result[RECIPE_COST_KEY] + "€")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()
