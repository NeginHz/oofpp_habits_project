import pytest
import sqlite3
from datetime import datetime, timedelta
# Helper class for mock habits
class MockHabit:
    """
    A mock class used to simulate a habit object for testing purposes.
    
    Attributes:
        name (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (str): How often the habit occurs (e.g., daily, weekly).
        creation_date (str): The date the habit was created (in YYYY-MM-DD format).
        creation_time (str): The time the habit was created (in HH:MM format).
    """
    def __init__(self, name, description, periodicity, creation_date, creation_time):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.creation_time = creation_time
# Test inserting a new habit
def test_insert_habit(habit_tracker_db):
    """
    Test inserting a new habit into the database.

    This test ensures that a habit is correctly inserted into the database and
    that the habit's attributes (name, description, and periodicity) are stored properly.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
    """
    new_habit = MockHabit("walking", "Daily walking habit", "daily", "2025-01-01", "06:30")
    habit_tracker_db.insert_habit(new_habit)

    # Verify the habit is in the database
    cursor = habit_tracker_db.connection.cursor()
    cursor.execute("SELECT * FROM habit WHERE name = ?", (new_habit.name,))
    inserted_habit = cursor.fetchone()

    assert inserted_habit is not None, "Habit should be inserted successfully."
    assert inserted_habit[1] == new_habit.name, "Habit name does not match."
    assert inserted_habit[2] == new_habit.description, "Habit description does not match."
    assert inserted_habit[3] == new_habit.periodicity, "Habit periodicity does not match."
# Test fetching habit metadata
def test_fetch_habit_metadata(habit_tracker_db, predefined_data):
    """
    Test fetching the metadata of an existing habit from the database.

    This test ensures that the correct metadata (description and periodicity) for a given habit is fetched.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    habit_name = "exercise"
    metadata = habit_tracker_db.fetch_habit_metadata(habit_name)

    assert metadata is not None, f"Metadata for habit '{habit_name}' should not be None."
    assert metadata == ("Weekly exercise habit", "weekly"), "Habit metadata does not match."
# Test inserting tracking record
def test_insert_tracking_record(habit_tracker_db, predefined_data):
    """
    Test inserting a tracking record for a specific habit.

    This test ensures that a habit's tracking record (indicating completion) is correctly inserted
    into the tracking table.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    habit_name = "exercise"
    completion_date = "2024-11-24"
    # The main logic ensures that get_valid_completion_date has already validated the date and ensures no duplicate exists
    # before calling insert_tracking_record.

    # Insert tracking record
    habit_tracker_db.insert_tracking_record(habit_name, completion_date)

    # Verify the record is inserted
    cursor = habit_tracker_db.connection.cursor()
    cursor.execute("SELECT * FROM habit_completions WHERE habit_name = ? AND completion_date = ?", (habit_name, completion_date))
    assert cursor.fetchone() is not None, "Tracking record should exist after insertion."
# Test checking habit existence
def test_habit_exists(habit_tracker_db, predefined_data):
    """
    Test checking the existence of a habit in the database.

    This test ensures that the method correctly identifies whether a habit exists in the database.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    assert habit_tracker_db.habit_exists("exercise"), "Habit 'exercise' should exist."
    assert not habit_tracker_db.habit_exists("nonexistent"), "Habit 'nonexistent' should not exist."
# Test when no habits are present in the database
def test_get_all_habits_empty_database(habit_tracker_db, predefined_data):
    """
    Test retrieving all habits when the database is empty.

    This test ensures that when there are no habits in the database, the function returns an empty list.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    # Clear the habit table
    habit_tracker_db._execute_query("DELETE FROM habit")

    # Fetch all habits
    habits = habit_tracker_db.get_all_habits()

    # Verify the result is an empty list
    assert habits == [], "When no habits exist, the result should be an empty list."
# Test retrieving all habits
def test_get_all_habits(habit_tracker_db, predefined_data):
    """
    Test retrieving all habits from the database.

    This test ensures that the correct habits are retrieved from the database and that
    the number of habits matches the predefined data.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    mock_habits, _ = predefined_data
    all_habits = habit_tracker_db.get_all_habits()

    # Verify the number of habits retrieved matches the predefined habits
    assert len(all_habits) == len(mock_habits), "Number of habits retrieved does not match predefined habits."

    # Verify that each habit exists in the retrieved list
    for habit in mock_habits:
        assert any(h[1] == habit.name for h in all_habits), f"Habit '{habit.name}' should exist in retrieved habits."
# Test retrieving all habit names
def test_get_all_habits_name(habit_tracker_db, predefined_data):
    """
    Test retrieving all habit names from the database.

    This test ensures that all habit names are correctly retrieved from the database.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    mock_habits, _ = predefined_data
    all_habit_names = habit_tracker_db.get_all_habits_name()

    # Verify the number of habit names retrieved matches the predefined habits
    assert len(all_habit_names) == len(mock_habits), "Number of habit names does not match predefined habits."

    # Verify that each habit name is in the retrieved list
    for habit in mock_habits:
        assert habit.name in all_habit_names, f"Habit name '{habit.name}' should be in the list of retrieved habit names."
# Test updating an existing habit
def test_update_habit(habit_tracker_db, predefined_data):
    """
    Test updating the description and periodicity of an existing habit.

    This test ensures that the habit's description and periodicity are updated
    correctly in the database.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    #already habit is "meditation", "Daily meditation habit", "daily", "2024-11-20", "22:00"
    # Update the habit's description and periodicity
    updated_description="Weekly meditation habit"
    updated_periodicity="weekly"
    # Create a mock object for the updated habit
    updated_habit = MockHabit("meditation",updated_description,updated_periodicity,None,None)  # Mock object for the updated habit
    # Update the habit
    habit_tracker_db.update_habit(updated_habit)
    # Verify the update
    cursor = habit_tracker_db.connection.cursor()
    cursor.execute("SELECT description, periodicity FROM habit WHERE name = ?", (updated_habit.name,))
    updated_data = cursor.fetchone()
    assert updated_data == (updated_description, updated_periodicity), \
        f"Habit '{updated_habit.name}' should be updated with the new description and periodicity."
# Test retrieving tracking records for a specific habit
def test_get_tracking_records_of_habit(habit_tracker_db, predefined_data):
    """
    Test retrieving tracking records for a specific habit.

    This test ensures that tracking records for a habit are correctly retrieved from the database.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    # Test retrieving tracking records for an existing habit from predefined_data
    habit_name = "exercise"
    # Retrieve tracking records for the habit
    records = habit_tracker_db.get_tracking_records_of_habit(habit_name)

    # Verify that records are returned correctly
    assert records is not None, f"Tracking records for habit '{habit_name}' should not be None."
    assert len(records) > 0, f"There should be tracking records for habit '{habit_name}'."
# Test fetching all tracking records from the database
def test_get_all_tracking_records(habit_tracker_db, predefined_data):
    """
    Test to ensure all tracking records are retrieved from the database.

    This test ensures that the method retrieves all tracking records and compares them to predefined data.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined tracking data for testing.
    """
    # Call the method to fetch all tracking records
    all_records = habit_tracker_db.get_all_tracking_records()

    # Extract the predefined tracking data from the fixture
    _, predefined_tracking_data = predefined_data

    # Extract only the (habit_name, completion_date) from the database records
    extracted_records = [(record[1], record[2]) for record in all_records]

    # Verify the total number of tracking records matches the predefined data
    assert len(extracted_records) == len(predefined_tracking_data), (
        f"Expected {len(predefined_tracking_data)} tracking records, but got {len(extracted_records)}."
    )

    # Verify each predefined tracking record exists in the extracted data
    for habit_name, completion_date in predefined_tracking_data:
        assert (habit_name, completion_date) in extracted_records, (
            f"Tracking record ({habit_name}, {completion_date}) is missing from the database."
        )
# Test fetching the creation date of a habit
def test_get_creation_date_of_habit(habit_tracker_db, predefined_data):
    """
    Test retrieving the creation date of a specific habit.

    This test ensures that the creation date returned from the database matches the expected value.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    # Test with an existing habit and it cannot be non-existent habit
    habit_name = "exercise"
    creation_date = habit_tracker_db.get_creation_date_of_habit(habit_name)
    expected_creation_date = "2024-11-01"  # From predefined data

    assert creation_date == expected_creation_date, f"Creation date for '{habit_name}' does not match expected value."
# Test retrieving the completion dates of a specific habit
def test_get_completion_dates_of_habit(habit_tracker_db, predefined_data):
    """
    Test retrieving completion dates for a specific habit.

    This test ensures that the list of completion dates for a habit is fetched correctly
    and matches the predefined data.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined tracking data for testing.
    """
    completion_dates = habit_tracker_db.get_completion_dates_of_habit("exercise")

    # Extract expected completion dates for "exercise" from predefined tracking data and sort them
    _, predefined_tracking_data = predefined_data
    expected_dates = sorted(
        [record[1] for record in predefined_tracking_data if record[0] == "exercise"]
    )

    # Sort the fetched completion dates for a proper comparison
    completion_dates = sorted(completion_dates)

    # Verify the fetched completion dates match the expected dates
    assert completion_dates == expected_dates, (
        f"Expected completion dates: {expected_dates}, but got: {completion_dates}"
    )
# Test deleting tracking records of a habit
def test_delete_tracking_records_of_habit(habit_tracker_db, predefined_data):
    """
    Test deleting tracking records of a specific habit.

    This test ensures that tracking records for a habit are deleted successfully from the database.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    habit_name = "meditation"
    # Perform the deletion of the tracking records
    habit_tracker_db.delete_tracking_records_of_habit(habit_name)


    # Verify that the tracking records have been deleted
    final_records = habit_tracker_db.get_tracking_records_of_habit(habit_name)
    assert final_records == [], f"All tracking records for '{habit_name}' should be deleted."
    habit_tracker_db, predefined_data
# Test deleting a habit from the database
def test_delete_habit(habit_tracker_db, predefined_data):
    """
    Test deleting a habit from the database.

    This test ensures that a habit is deleted successfully from the database and no longer exists.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    habit_name = "meditation"
    # Perform the deletion
    habit_tracker_db.delete_habit(habit_name)

    # Verify the habit has been deleted
    assert not habit_tracker_db.habit_exists(habit_name), f"Habit '{habit_name}' should be deleted."
#Test fetching the periodicity of a habit
def test_get_habit_periodicity(habit_tracker_db, predefined_data):
    """
    Test retrieving the periodicity of a specific habit.

    This test ensures that the periodicity returned from the database matches the expected value.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    # Test with an existing habit it cannot be non-existent habit it already checked
    #test weekly habit
    habit_name = "exercise"
    periodicity = habit_tracker_db.get_habit_periodicity(habit_name)
    expected_periodicity = "weekly"  # From predefined data
    assert periodicity == expected_periodicity, f"Periodicity for '{habit_name}' does not match expected value."
    #test daily habit
    habit_name = "meditation"
    periodicity = habit_tracker_db.get_habit_periodicity(habit_name)
    expected_periodicity = "daily"  # From predefined data
    assert periodicity == expected_periodicity, f"Periodicity for '{habit_name}' does not match expected value."   
# Test fetching habits by periodicity
def test_get_habits_by_periodicity(habit_tracker_db, predefined_data):
    """
    Test retrieving habits from the database based on their periodicity (daily/weekly).

    This test ensures that the `get_habits_by_periodicity` method correctly filters habits 
    based on their periodicity and matches them against expected data.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined data for testing.
    """
    # Fetch daily habits
    daily_habits = habit_tracker_db.get_habits_by_periodicity("daily")

    # Define expected daily habits from predefined data
    expected_daily_habits = [
        ("meditation", "Daily meditation habit", "daily", "2024-10-30", "22:00"),
        ("coding", "Daily coding practice", "daily", "2024-11-02", "10:00"),
        ("water intake", "Track daily water intake", "daily", "2024-11-10", "11:00"),
    ]

    # Extract habit names for comparison
    daily_habit_names = [habit[1] for habit in daily_habits]
    expected_daily_habit_names = [habit[0] for habit in expected_daily_habits]
    # Verify the fetched daily habits match the expected ones
    assert daily_habit_names == expected_daily_habit_names, "Daily habits do not match expected data."

    # Fetch weekly habits
    weekly_habits = habit_tracker_db.get_habits_by_periodicity("weekly")

    # Define expected weekly habits from predefined data
    expected_weekly_habits = [
        ("exercise", "Weekly exercise habit", "weekly", "2024-11-01", "08:00"),
        ("reading", "Weekly reading habit", "weekly", "2024-10-28", "09:00"),
    ]

    # Extract habit names for comparison
    weekly_habit_names = [habit[1] for habit in weekly_habits]
    expected_weekly_habit_names = [habit[0] for habit in expected_weekly_habits]
    # Verify the fetched weekly habits match the expected ones
    assert weekly_habit_names == expected_weekly_habit_names, "Weekly habits do not match expected data."
# Test fetching habit completions from the previous calendar month
def test_get_habit_completions_last_month(habit_tracker_db, predefined_data):
    """
    Test to verify the retrieval of habit completions from the previous calendar month.

    This test checks that the `get_habit_completions_last_month` method correctly retrieves
    habit completions for the last month based on predefined tracking data.

    Args:
        habit_tracker_db (Mock): A mock instance of the HabitTrackerDB used to simulate database interactions.
        predefined_data (Mock): A fixture providing predefined tracking data for testing.
    """
    # Get today's date to calculate the date range for the previous month
    today = datetime.today().date()

    # Calculate the first and last day of the previous month
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    # Fetch habit completions from the previous calendar month
    completions = habit_tracker_db.get_habit_completions_last_month()

    # Extract expected completions from predefined data for the previous month
    _, predefined_tracking_data = predefined_data
    expected_completions = [
        (record[0], record[1])
        for record in predefined_tracking_data
        if first_day_of_last_month <= datetime.strptime(record[1], "%Y-%m-%d").date() <= last_day_of_last_month
    ]

    # Sort both the fetched and expected results for consistent comparison
    completions = sorted(completions, key=lambda x: (x[0], x[1]))
    expected_completions = sorted(expected_completions, key=lambda x: (x[0], x[1]))

    # Assert that the fetched completions match the expected completions
    assert completions == expected_completions, (
        f"Expected completions: {expected_completions}, but got: {completions}"
    )
