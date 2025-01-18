import pytest
from src.habit import Habit
from unittest.mock import Mock
class TestHabit:
    def test_add_habit(self, habit_tracker_db):
        """
        Test adding a new habit to the database.

        This test ensures that when a new habit is added, it is properly 
        stored in the database with the correct metadata.
        
        Args:
            habit_tracker_db (Mock): A mock instance of the HabitTrackerDB.
        """
        # Create a new habit object
        new_habit = Habit(
            name="running",
            description="Daily running habit",
            periodicity="daily",
            creation_date="2025-01-10",
            creation_time="07:00",
            database=habit_tracker_db
        )

        new_habit.add_habit()

        # Retrieve the habit from the database to validate it was added
        assert habit_tracker_db.habit_exists("running") is not None, "Habit was not added to the database."
        assert habit_tracker_db.fetch_habit_metadata("running") == (new_habit.description , new_habit.periodicity)
    def test_modify_habit(self, habit_tracker_db, predefined_data):
        """
        Test modifying an existing habit in the database.

        This test ensures that when a habit's details are modified, the changes
        are correctly reflected in the database, without altering the habit's name.

        Args:
            habit_tracker_db (Mock): A mock instance of the HabitTrackerDB.
            predefined_data (Mock): A mock fixture providing predefined habits for modification.
        """
        # Create a habit to modify
        habit_to_modify = Habit(
            name="meditation",
            description="Updated meditation habit",
            periodicity="weekly",
            database=habit_tracker_db
        )
        # Modify the habit's description and periodicity
        habit_to_modify.modify_habit()
       # Retrieve the habit from the database to validate the modifications
        assert habit_tracker_db.fetch_habit_metadata("meditation") == (habit_to_modify.description , habit_to_modify.periodicity)
    def test_remove_habit(self, habit_tracker_db, predefined_data):
        """
        Test removing a habit from the database.

        This test ensures that when a habit is removed, it is no longer present
        in the database.

        Args:
            habit_tracker_db (Mock): A mock instance of the HabitTrackerDB.
            predefined_data (Mock): A mock fixture providing predefined habits for removal.
        """
        # Create a habit to remove
        habit_to_remove = Habit(
            name="reading",
            description="Weekly reading habit",
            periodicity="weekly",
            database=habit_tracker_db
        )
        # Remove the habit from the database
        habit_to_remove.remove_habit()
        # Verify the habit was successfully removed
        removed_habit = habit_tracker_db.habit_exists("reading")
        assert removed_habit is False, "Habit was not removed from the database."
