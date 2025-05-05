from core.runner import make_food_recipe
from utils.diet import Diet
from utils.difficulty import Difficulty
from constants.output import *
import asyncio
import os
import sys

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


def choose_interface():
    print("📱 Choose an interface:")
    print("1. Command Line Interface 💻")
    print("2. Graphical User Interface (Gradio) 🖼️")
    
    while True:
        try:
            choice = int(input("Please enter your choice (1 or 2): "))
            if choice in [1, 2]:
                return choice
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def cli_interface():
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


def gradio_interface():
    try:
        # Import the Gradio app from the UI folder
        sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))
        from ui.gradio_app import launch_app
        
        print("🚀 Launching Gradio interface...")
        app = launch_app()
        app.launch()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Make sure you have installed Gradio. You can install it with:")
        print("pip install gradio")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred while launching the Gradio interface: {e}")
        sys.exit(1)


def main():
    print("👋 Welcome to Personal Chef AI!")
    interface_choice = choose_interface()
    
    if interface_choice == 1:
        cli_interface()
    else:
        gradio_interface()


if __name__ == "__main__":
    main()