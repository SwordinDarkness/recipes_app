#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import RecipesApp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "recipes"
    meal = input("What meal do you want to eat?  ").strip()
    no_whitespace = meal.replace(" ", "-")
    file_name = f"{no_whitespace}-recipe-{timestamp }.md"

    inputs = {
        "file_name": file_name,
        "folder": folder,
        "meal": meal
    }
    
    try:
        RecipesApp().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
