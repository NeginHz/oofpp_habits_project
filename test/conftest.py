"""
conftest.py
------------
This module provides shared pytest fixtures for the HabitTrackerDB application.
It includes:
- An in-memory SQLite database fixture for testing the HabitTrackerDB class.
- A fixture for preloading the database with mock data to simulate real-world scenarios.
"""
import pytest
import sqlite3
from src.database import HabitTrackerDB
class MockHabit:
    """
    Represents a mock habit object for testing purposes.
    """
    def __init__(self, name, description, periodicity, creation_date=None, creation_time=None):
        """
        Initialize a MockHabit instance.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            periodicity (str): Periodicity of the habit (e.g., 'daily', 'weekly').
            creation_date (str, optional): Date the habit was created.
            creation_time (str, optional): Time the habit was created.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.creation_time = creation_time
@pytest.fixture
def habit_tracker_db():
    """
    Pytest fixture to provide an in-memory HabitTrackerDB instance for testing.

    Yields:
        HabitTrackerDB: An instance of HabitTrackerDB connected to an in-memory SQLite database.
    """
    mock_db = sqlite3.connect(":memory:") # Use an in-memory database for isolation and performance
    habit_tracker = HabitTrackerDB(connection=mock_db)
    yield habit_tracker # Provide the database instance to the test
    habit_tracker.close() # Ensure the database connection is closed after the test
@pytest.fixture
def predefined_data(habit_tracker_db):
    """
    Pytest fixture to preload the HabitTrackerDB with predefined mock data.

    Args:
        habit_tracker_db (HabitTrackerDB): The in-memory database fixture.

    Returns:
        tuple: A tuple containing:
            - list of MockHabit objects added to the database.
            - list of tracking data (habit name and completion date) added to the database.
    """
    # Define mock habits
    mock_habits = [
        MockHabit("exercise", "Weekly exercise habit", "weekly", "2024-11-01", "08:00"),
        MockHabit("meditation", "Daily meditation habit", "daily", "2024-10-30", "22:00"),
        MockHabit("reading", "Weekly reading habit", "weekly", "2024-10-28", "09:00"),
        MockHabit("coding", "Daily coding practice", "daily", "2024-11-02", "10:00"),
        MockHabit("water intake", "Track daily water intake", "daily", "2024-11-10", "11:00"),
    ]
    # Define mock tracking data
    mock_tracking_data = [
        # Exercise tracking records
        ("exercise", "2024-11-01"),  # Week 44
        ("exercise", "2024-11-03"),  # Week 44
        ("exercise", "2024-11-05"),  # Week 45
        ("exercise", "2024-11-06"),  # Week 45
        ("exercise", "2024-11-22"),  # Week 47
        ("exercise", "2024-11-27"),  # Week 48
        ("exercise", "2024-11-29"),  # Week 48
        ("exercise", "2024-12-02"),  # Week 49
        ("exercise", "2024-12-03"),  # Week 49
        # Meditation tracking records
        ("meditation", "2024-11-01"), 
        ("meditation", "2024-11-02"), 
        ("meditation", "2024-11-03"), 
        ("meditation", "2024-11-04"),
        ("meditation", "2024-11-09"), 
        ("meditation", "2024-11-23"), 
        ("meditation", "2024-11-24"), 
        ("meditation", "2024-11-13"),
        ("meditation", "2024-11-14"), 
        ("meditation", "2024-11-15"), 
        ("meditation", "2024-11-27"), 
        ("meditation", "2024-11-28"),
        ("meditation", "2024-11-29"), 
        ("meditation", "2024-11-30"),
        ("meditation", "2024-12-01"),
        ("meditation", "2024-12-02"),
        ("meditation", "2024-12-04"),
        ("meditation", "2024-12-06"),
        ("meditation", "2024-12-07"),    
        ("meditation", "2024-12-09"),
        ("meditation", "2024-12-10"),
        ("meditation", "2024-12-11"),
        # reading tracking records
        ("reading", "2024-11-05"),#week 45
        ("reading", "2024-11-06"),#week 45
        ("reading", "2024-11-10"),#week 45
        ("reading", "2024-11-18"),#week 47
        ("reading", "2024-11-25"),#week 48
        ("reading", "2024-12-05"),#week 49
        ("reading", "2024-12-15"),#week 50
        ("reading", "2024-12-16"),#week 51
        # coding tracking records
        ("coding", "2024-11-03"),
        ("coding", "2024-11-04"), 
        ("coding", "2024-11-05"),
        ("coding", "2024-11-06"),
        ("coding", "2024-11-07"),
        ("coding", "2024-11-08"), 
        ("coding", "2024-11-09"),
        ("coding", "2024-11-11"),    
        ("coding", "2024-11-13"),
        ("coding", "2024-11-16"), 
        ("coding", "2024-11-17"),
        ("coding", "2024-11-18"),
        ("coding", "2024-11-23"),
        ("coding", "2024-11-30"), 
        ("coding", "2024-12-01"),
        # water intake tracking records
        ("water intake", "2024-11-11"),
        ("water intake", "2024-11-13"),
        ("water intake", "2024-11-19"),
        ("water intake", "2024-11-20"),
        ("water intake", "2024-11-21"),
        ("water intake", "2024-11-22"),
        ("water intake", "2024-11-25"),
        ("water intake", "2024-11-26"),       
        ("water intake", "2024-11-28"),
        ("water intake", "2024-11-30"),
        ("water intake", "2024-12-01"),
        ("water intake", "2024-12-02"), 
        ("water intake", "2024-12-03"),
        ("water intake", "2024-12-04"),
    ]
    # Insert habits and tracking data into the database
    for habit in mock_habits:
        habit_tracker_db.insert_habit(habit)
    for habit_name, completion_date in mock_tracking_data:
        habit_tracker_db.insert_tracking_record(habit_name, completion_date)
    return mock_habits, mock_tracking_data
