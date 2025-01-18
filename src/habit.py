# habit.py
from .database import HabitTrackerDB
"""
Represents a habit with associated metadata and database operations.
"""

class Habit:
    def __init__(self, name, description, periodicity, creation_date=None, creation_time=None, database=HabitTrackerDB()):
        """
        Initialize a new habit.

        Args:
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (str): The periodicity of the habit (e.g., 'daily', 'weekly').
            creation_date (str, optional): The date the habit was created. Defaults to None.
            creation_time (str, optional): The time the habit was created. Defaults to None.
            database (HabitTrackerDB, optional): An instance of the HabitTrackerDB to interact with the database. Defaults to an instance of HabitTrackerDB.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date if creation_date is not None else 'Unknown'  # Default to 'Unknown' if not provided
        self.creation_time = creation_time if creation_time is not None else 'Unknown'  # Default to 'Unknown' if not provided
        self.db = database
    def __str__(self):
        """
        Return a string representation of the habit.

        Returns:
            str: A string describing the habit.
        """
        return (
            f"Habit(name='{self.name}', description='{self.description}', "
            f"periodicity='{self.periodicity}', creation_date='{self.creation_date}', "
            f"creation_time='{self.creation_time}')"
        )
    def add_habit(self):
        """
        Add the habit to the database.

        This method uses the insert_habit function from the HabitTrackerDB
        to save the current habit object to the database.
        """
        try:
            self.db.insert_habit(self)
        except Exception as e:
            print(f"Failed to add habit '{self.name}': {e}")
    def modify_habit(self):
        """
        Modify the habit details in the database.

        This method uses the update_habit function from the HabitTrackerDB
        to update the habit's information in the database.
        """
        try:
            self.db.update_habit(self)
        except Exception as e:
            print(f"Failed to modify habit '{self.name}': {e}")
    def remove_habit(self):
        """
        Remove the habit from the database.

        This method uses the delete_habit function from the HabitTrackerDB
        to delete the habit based on its name from the database.
        """
        try:
            self.db.delete_habit(self.name)
        except Exception as e:
            print(f"Failed to remove habit '{self.name}': {e}")
        
