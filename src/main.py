"""
main.py
-------
The main entry point for the Habit Tracker application. This script initializes
the database and the command-line interface (CLI) and runs the application.
"""
from .database import HabitTrackerDB
from .cli import UserInterface

def main():
    """
    Main function to run the Habit Tracker application.

    - Initializes the HabitTrackerDB for database operations.
    - Initializes the UserInterface for command-line interaction.
    - Executes the CLI to interact with the user.
    - Ensures the database connection is closed properly after use.
    """
    # Initialize the database
    db = HabitTrackerDB()
    try:
        # Initialize the command-line interface
        ui = UserInterface(db)

        # Run the command-line interface
        ui.run()
    finally:
        # Ensure the database connection is always closed
        db.close()

if __name__ == "__main__":
    # Entry point of the application
    main()