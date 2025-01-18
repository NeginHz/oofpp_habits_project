import pytest
from src.analytics import HabitAnalyzer
from datetime import datetime
class MockHabit:
    """
    A mock class to simulate a habit object for testing purposes.
    
    Attributes:
        name (str): Name of the habit.
        description (str): Description of the habit.
        periodicity (str): Periodicity of the habit (e.g., "daily", "weekly").
        creation_date (str): Date the habit was created (optional).
        creation_time (str): Time the habit was created (optional).
    """
    def __init__(self, name, description, periodicity, creation_date=None, creation_time=None):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.creation_time = creation_time
def test_check_habit_exists(predefined_data, habit_tracker_db):
    """
    Test checking if a habit exists in the database.

    This test checks both for the existence of habits that are already in the database 
    (from `predefined_data`) and non-existent habits.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Test for existing habits
    for habit in mock_habits:
        assert analyzer.check_habit_exists(habit.name) is True

    # Test for a non-existing habit
    assert analyzer.check_habit_exists("nonexistent_habit") is False
def test_get_habits_info(predefined_data, habit_tracker_db):
    """
    Test retrieving basic information about all habits in the database.

    This test checks if the `get_habits_info` method returns the correct information 
    (name, description, periodicity) for each habit.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Retrieve all habits' information
    habits_info = analyzer.get_habits_info()
    # Verify the number of habits retrieved matches the expected
    assert len(habits_info) == len(mock_habits)

    # Check that each habit's data is present in the retrieved info
    for habit in mock_habits:
        assert any(h[1] == habit.name and h[2] == habit.description and h[3] == habit.periodicity for h in habits_info)
def test_get_habit_description_and_periodicity(predefined_data, habit_tracker_db):
    """
    Test retrieving the description and periodicity of a specific habit.

    This test ensures that the `get_habit_description_and_periodicity` method correctly 
    returns the description and periodicity for each habit in the database.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

     # Test for existing habits (non-existent habits are not tested here, as they are selected from the menu)
    for habit in mock_habits:
        description, periodicity = analyzer.get_habit_description_and_periodicity(habit.name)
        assert description == habit.description
        assert periodicity == habit.periodicity
def test_get_creation_date_of_habit(predefined_data, habit_tracker_db):
    """
    Test retrieving the creation date of a specific habit.

    This test checks if the creation date returned matches the one stored in the predefined data.
    It also tests that a non-existent habit returns `None`.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Test for existing habits
    for habit in mock_habits:
        creation_date = analyzer.get_creation_date_of_habit(habit.name)
        assert creation_date == habit.creation_date
    # Test for a non-existing habit by the way it can
    assert analyzer.get_creation_date_of_habit("nonexistent_habit") is None
def test_check_tracking_records_of_habit_exists(predefined_data, habit_tracker_db):
    """
    Test checking if tracking records exist for a specific habit.

    This test verifies that the `check_tracking_records_of_habit_exists` method correctly 
    returns tracking records for habits that have records and `None` for habits without records.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    _, mock_tracking_data = predefined_data

    # Test for habits with tracking records
    tracking_records = analyzer.check_tracking_records_of_habit_exists("exercise")
    assert tracking_records is not None
    assert len(tracking_records) == len([record for record in mock_tracking_data if record[0] == "exercise"])

    # Create a new habit without tracking records
    new_habit = MockHabit("new_habit", "Test habit with no records", "daily", "2024-09-11","22:00")
    
    habit_tracker_db.insert_habit(new_habit)  # Add the new habit to the database

    # Test for the new habit with no tracking records
    assert analyzer.check_tracking_records_of_habit_exists("new_habit") is None
def test_remove_tracking_records_of_habit(predefined_data, habit_tracker_db):
    """
    Test removing tracking records for a habit.

    This test ensures that when tracking records are removed for a habit, the `check_tracking_records_of_habit_exists` 
    method returns `None`, confirming the records were deleted.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    # Test removing tracking records for an existing habit (habit must have records)
    analyzer.remove_tracking_records_of_habit("exercise")
    # Verify that tracking records for the habit are deleted
    tracking_records = analyzer.check_tracking_records_of_habit_exists("exercise")
    assert tracking_records is None  # All records should be deleted
def test_list_habit_names(predefined_data, habit_tracker_db):
    """
    Test listing all habit names in the database.

    This test ensures that the `list_habit_names` method returns the correct list of habit names,
    and verifies that it handles the case where no habits exist in the database (returns `None`).
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Test listing all habit names
    habit_names = analyzer.list_habit_names()
    assert sorted(habit_names) == sorted([habit.name for habit in mock_habits])

    # Test when no habits exist in the database
    for habit in mock_habits:
        habit_tracker_db.delete_habit(habit.name)
    # Ensure all habits are removed
    assert analyzer.list_habit_names() is None
def test_add_new_tracking_record(habit_tracker_db):
    """
    Test adding a new tracking record for a habit.

    This test ensures that the `add_new_tracking_record` method correctly adds a new tracking record 
    for a habit with a unique completion date.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)

    # Add a new tracking record for 'exercise' habit
    habit_name = "exercise"
    completion_date = "2025-01-01" # Use a date not already in the database for this habit
    analyzer.add_new_tracking_record(habit_name, completion_date)

     # Verify the record was added
    tracking_records = analyzer.list_tracking_records_of_habit(habit_name)
    assert any(record[1] == habit_name and record[2] == completion_date for record in tracking_records)
def test_list_all_tracking_records(predefined_data, habit_tracker_db):
    """
    Test listing all tracking records in the database.

    This test verifies that the `list_all_tracking_records` method returns all tracking records 
    stored in the database and compares it against the predefined mock data.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    _, mock_tracking_data = predefined_data

    # Retrieve all tracking records
    tracking_records = analyzer.list_all_tracking_records()

    # Strip the `id` field from `tracking_records`
    tracking_data_without_ids = [(record[1], record[2]) for record in tracking_records]

    # Compare stripped tracking records with mock_tracking_data
    assert sorted(tracking_data_without_ids) == sorted(mock_tracking_data)
def test_list_tracking_records_of_habit(predefined_data, habit_tracker_db):
    """
    Test listing tracking records for a specific habit.

    This test ensures that the `list_tracking_records_of_habit` method correctly filters and 
    returns tracking records for a specific habit, and compares the result against predefined data.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    _, mock_tracking_data = predefined_data

    # Test for a specific habit (e.g., 'exercise')
    habit_name = "exercise"
    records = analyzer.list_tracking_records_of_habit(habit_name)
    # Filter expected records from predefined data
    expected_records = [record for record in mock_tracking_data if record[0] == habit_name]
    # Strip the `id` field from records for comparison
    tracking_data_without_ids = [(record[1], record[2]) for record in records]
    # Ensure the retrieved records match the expected records
    assert sorted(tracking_data_without_ids) == sorted(expected_records)
def test_list_habits_by_periodicity(predefined_data, habit_tracker_db):
    """
    Test listing habits by their periodicity (e.g., daily or weekly).

    This test ensures that the `list_habits_by_periodicity` method returns the correct habits 
    based on their periodicity and compares the result to predefined mock data.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Test for daily habits
    daily_habits = analyzer.list_habits_by_periodicity("daily")
    daily_habit_names = [habit[1] for habit in daily_habits]  # Extract only the habit names
    expected_daily_habits = [habit.name for habit in mock_habits if habit.periodicity == "daily"]
    
    assert sorted(daily_habit_names) == sorted(expected_daily_habits)

    # Test for weekly habits
    weekly_habits = analyzer.list_habits_by_periodicity("weekly")
    weekly_habit_names = [habit[1] for habit in weekly_habits]  # Extract only the habit names
    expected_weekly_habits = [habit.name for habit in mock_habits if habit.periodicity == "weekly"]
    assert sorted(weekly_habit_names) == sorted(expected_weekly_habits)
def test_count_habit_completions_last_month(predefined_data, habit_tracker_db):
    """
    Test counting habit completions in the previous calendar month.

    This test verifies that the `count_habit_completions_last_month` method correctly counts the 
    completions from the previous month, though actual verification may require mocking of 
    tracking data.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)

    # Count habit completions in the last month
    completions_last_month = analyzer.count_habit_completions_last_month()
    # Verify that the returned result is a list (actual counts can be verified if mock data supports it)
    assert isinstance(completions_last_month, list), \
        "Expected a list of habit completions for the last month."
def test_sort_habits_by_count():
    """
    Test sorting habits based on their completion counts.

    This test ensures that the `sort_habits_by_count` method correctly sorts habits by the number 
    of completions in descending order.
    """
    analyzer = HabitAnalyzer(None)  # No database needed for this method
    habit_counts = [("exercise", 5), ("reading", 2), ("meditation", 8)]

    # Sort habits by count (in descending order)
    sorted_habits = analyzer.sort_habits_by_count(habit_counts)
    # Expected sorted habits based on counts (highest to lowest)
    expected_sorted_habits = [("meditation", 8), ("exercise", 5), ("reading", 2)]
    # Assert that the sorted list matches the expected order
    assert sorted_habits == expected_sorted_habits
def test_find_struggling_habits_last_month(habit_tracker_db, predefined_data):
    """
    Test the find_struggling_habits_last_month method to ensure it identifies habits
    with missed completions correctly and sorts them as expected.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Assuming `count_habit_completions_last_month` returns completion counts for the last month.
    expected_habit_counts = {
        "exercise": 2,        # Exercise completed 2 times in the last month
        "meditation": 8,     # Meditation completed 8 times in the last month
        "reading": 3,         # Reading completed 3 times in the last month
        "coding": 1,          # Coding completed 1 times in the last month
        "water intake": 4,    # Water intake completed 4 times in the last month
    }

    # Expected sorted result based on completion counts (ascending order of struggling habits).
    expected_sorted_habits = [
        ("meditation", 8),
        ("water intake", 4),
        ("reading", 3),
        ("exercise", 2),
        ("coding", 1),
    ]

    # Call the method to test
    struggling_habits = analyzer.find_struggling_habits_last_month()

    # Validate the results
    assert struggling_habits is not None, "The method returned None unexpectedly."
    assert struggling_habits == expected_sorted_habits, (
        f"Expected sorted struggling habits: {expected_sorted_habits}, "
        f"but got: {struggling_habits}"
    )
def test_sort_dates_descending():
    """
    Test sorting a list of dates in descending order.

    This test ensures that the `sort_dates_descending` method correctly sorts dates from most recent 
    to least recent.
    """
    analyzer = HabitAnalyzer(None)  # No database needed for this method
    dates = ["2025-01-01", "2024-12-31", "2025-01-02"]

    # Sort dates in descending order
    sorted_dates = analyzer.sort_dates_descending(dates)
    expected_sorted_dates = ["2025-01-02", "2025-01-01", "2024-12-31"]
    assert sorted_dates == expected_sorted_dates
def test_get_habit_periodicity_str(predefined_data, habit_tracker_db):
    """
    Test retrieving the periodicity (daily, weekly, etc.) of a habit.

    This test ensures that the `get_habit_periodicity_str` method returns the correct periodicity for 
    each habit.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Test for existing habits
    for habit in mock_habits:
        periodicity = analyzer.get_habit_periodicity_str(habit.name)
        assert periodicity == habit.periodicity
def test_list_completion_dates_of_habit(predefined_data, habit_tracker_db):
    """
    Test listing the completion dates for a specific habit.

    This test verifies that the `list_completion_dates_of_habit` method returns the correct list of 
    completion dates for each habit, based on predefined tracking data.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    _, mock_tracking_data = predefined_data

    # Group tracking data by habit name for testing
    habit_tracking_dict = {}
    for habit_name, completion_date in mock_tracking_data:
        if habit_name not in habit_tracking_dict:
            habit_tracking_dict[habit_name] = []
        habit_tracking_dict[habit_name].append(completion_date)

    # Test for habits with tracking data
    for habit_name, expected_dates in habit_tracking_dict.items():
        completion_dates = analyzer.list_completion_dates_of_habit(habit_name)
        assert sorted(completion_dates) == sorted(expected_dates)
def test_calculate_current_streak_for_daily_habit():
    """
    Test calculating the current streak for a daily habit.

    This test verifies that the `calculate_current_streak_for_daily_habit` method correctly calculates 
    the streak of consecutive days for a daily habit.
    """
    analyzer = HabitAnalyzer(None)  # Mock storage not needed for date calculations
    # Test with valid streak
    dates = ["2025-01-01", "2024-12-31", "2024-12-28", "2024-12-17"]
    assert analyzer.calculate_current_streak_for_daily_habit(dates) == 2
    # Test with non-consecutive dates
    dates = ["2025-01-10", "2025-01-08", "2025-01-07"]
    assert analyzer.calculate_current_streak_for_daily_habit(dates) == 1
    dates = ["2025-01-01", "2024-12-31"]
    assert analyzer.calculate_current_streak_for_daily_habit(dates) == 2
def test_are_dates_in_consecutive_weeks():
    """
    Test checking whether two dates are in consecutive weeks.

    This test ensures that the `are_dates_in_consecutive_weeks` method correctly identifies whether two 
    dates fall into consecutive ISO weeks.
    """
    analyzer = HabitAnalyzer(None)

    # Test with dates in consecutive weeks
    date1 = "2024-12-31"  #(ISO week 1 of 2025)
    date2 = "2024-12-24" # (ISO week 52 of 2024)
    assert analyzer.are_dates_in_consecutive_weeks(date1, date2) is True


    # Test with dates in consecutive weeks
    date1 = "2025-01-01"  # Week 1 of 2025
    date2 = "2025-01-08"  # Week 2 of 2025
    assert analyzer.are_dates_in_consecutive_weeks(date1, date2) is True

    # Test with dates in the same week
    date1 = "2025-01-01"
    date2 = "2025-01-03"
    assert analyzer.are_dates_in_consecutive_weeks(date1, date2) is False

    # Test with dates far apart
    date1 = "2025-01-01"
    date2 = "2025-02-01"
    assert analyzer.are_dates_in_consecutive_weeks(date1, date2) is False

    # Test cases
    assert analyzer.are_in_same_week("2024-12-24", "2024-12-28") is True  # Same ISO week (Week 52)
    assert analyzer.are_in_same_week("2024-12-31", "2025-01-01") is True  # Same ISO week (Week 1)
    assert analyzer.are_in_same_week("2024-12-24", "2024-12-31") is False  # Different ISO weeks
def test_are_in_same_week():
    """
    Test checking whether two dates fall in the same week.

    This test verifies that the `are_in_same_week` method correctly identifies if two dates belong to the 
    same ISO week.
    """
    analyzer = HabitAnalyzer(None)

    # Test with dates in the same week
    date1 = "2025-01-01"
    date2 = "2025-01-03"
    assert analyzer.are_in_same_week(date1, date2) is True

    # Test with dates in different weeks
    date1 = "2025-01-01"
    date2 = "2025-01-08"
    assert analyzer.are_in_same_week(date1, date2) is False

    # Test with dates in different year
    date1 = "2025-01-01"
    date2 = "2024-01-01"
    assert analyzer.are_in_same_week(date1, date2) is False
def test_calculate_current_streak_for_weekly_habit(predefined_data, habit_tracker_db):
    """
    Test calculating the current streak for a weekly habit.

    This test ensures that the `calculate_current_streak_for_weekly_habit` method correctly calculates 
    the streak of consecutive weeks for a weekly habit.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)

    # Mock data for weekly habit completion dates (in descending order)
    list_completion_dates = [
        "2024-12-03",  # Week 49
        "2024-12-02",  # Week 49 (same week as above)
        "2024-11-29",  # Week 48
        "2024-11-27",  # Week 48 (same week as above)
        "2024-11-22",  # Week 47
        "2024-11-06",  # Week 45
        "2024-11-01",  # Week 44
    ]

    # Call the method
    streak = analyzer.calculate_current_streak_for_weekly_habit(list_completion_dates)

    # Assert the current streak
    assert streak == 3 , "The streak should be 3 for weeks 49, 48, and 47." # Weeks 49, 48, and 47

    # Test with a single date (edge case)
    single_date_streak = analyzer.calculate_current_streak_for_weekly_habit(["2024-12-03"])
    assert single_date_streak == 1 ,"Single date streak should be 1."


    # Test with non-consecutive dates
    non_consecutive_dates = [
        "2024-12-03",  # Week 49
        "2024-11-01",  # Week 44 (break in streak)
    ]
    non_consecutive_streak = analyzer.calculate_current_streak_for_weekly_habit(non_consecutive_dates)
    assert non_consecutive_streak == 1 , "Non-consecutive weeks should result in a streak of 1." # Only the most recent week counts
def test_get_current_streak_for_habit(predefined_data, habit_tracker_db):
    """
    Test getting the current streak for a habit.

    This test verifies that the `get_current_streak_for_habit` method correctly calculates the streak 
    for both daily and weekly habits.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    # Test for a daily habit with a streak
    habit_name_daily = "meditation"
    daily_streak = analyzer.get_current_streak_for_habit(habit_name_daily)
    # Based on `predefined_data`, "meditation" has recent consecutive completions.
    assert daily_streak == 3 , "Expected daily streak to be 3."

    # Test for a weekly habit with a streak
    habit_name_weekly = "exercise"
    weekly_streak = analyzer.get_current_streak_for_habit(habit_name_weekly)
    # Based on `predefined_data`, "exercise" has recent weekly completions.
    assert weekly_streak == 3 ,"Expected weekly streak to be 3."
def test_calculate_longest_streak_for_daily_habit(predefined_data, habit_tracker_db):
    """
    Test calculating the longest streak for a daily habit.

    This test ensures that the `calculate_longest_streak_for_daily_habit` method correctly calculates 
    the longest streak for a daily habit.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    #the habit name is exist and has tracking records , they are checked before called this function


    # Test for a habit with multiple streaks
    completion_dates = [
        "2025-01-01", "2025-01-02", "2025-01-03",  # Streak of 3
        "2025-01-05", "2025-01-06",# Streak of 2
        "2025-01-08",  # Streak of 1
        "2025-01-10", "2025-01-11",  # Streak of 2
    ]
    result = analyzer.calculate_longest_streak_for_daily_habit(sorted(completion_dates))
    assert result == 3, "Longest streak should be 3"

    # Test for a habit with a single streak
    completion_dates = ["2024-12-31","2025-01-01", "2025-01-02", "2025-01-03"]  # Streak of 4
    result = analyzer.calculate_longest_streak_for_daily_habit(sorted(completion_dates))
    assert result == 4, "Longest streak should be 4"

    # Test for a habit with no streaks
    completion_dates = ["2025-01-01", "2025-01-05", "2025-01-10"]  # No consecutive days
    result = analyzer.calculate_longest_streak_for_daily_habit(sorted(completion_dates))
    assert result == 1, "Longest streak should be 1 for non-consecutive dates"

    # Test for a single completion date
    completion_dates = ["2025-01-01"]
    result = analyzer.calculate_longest_streak_for_daily_habit(sorted(completion_dates))
    assert result == 1, "Longest streak for single completion date should be 1"

    completion_dates = [
    "2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04",
    "2024-11-09", "2024-11-13", "2024-11-14", "2024-11-15",
    "2024-11-23", "2024-11-24", "2024-11-27", "2024-11-28",
    "2024-11-29", "2024-11-30", "2024-12-01", "2024-12-02",
    "2024-12-04", "2024-12-06", "2024-12-07", "2024-12-09",
    "2024-12-10", "2024-12-11",
    ]
    # Convert to ascending order (already sorted in this case)
    sorted_dates = sorted(completion_dates)
    # Call the function
    result = analyzer.calculate_longest_streak_for_daily_habit(sorted_dates)
    # Expected result
    expected_streak = 6
    assert result == expected_streak, f"Expected {expected_streak}, but got {result}"
def test_calculate_longest_streak_for_weekly_habit(predefined_data, habit_tracker_db):
    """
    Test the calculation of the longest streak for a weekly habit.

    This test ensures that the `calculate_longest_streak_for_weekly_habit` method correctly calculates
    the longest streak for weekly habits based on completion dates.
    """
    analyzer = HabitAnalyzer(None)  # No DB needed for this method
    # Test for consecutive weekly dates
    completion_dates = ["2025-01-07", "2024-12-31", "2024-12-24"]  # Consecutive weeks
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 3, "Longest streak should be 3 for consecutive weekly dates"

    # Test for non-consecutive weekly dates
    completion_dates = ["2025-01-07", "2024-12-24", "2024-12-10"]  # Gaps in weeks
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 1, "Longest streak should be 1 for non-consecutive weekly dates"

    # Test for a single date
    completion_dates = ["2025-01-07"]
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 1, "Longest streak should be 1 for a single completion date"

    # Use predefined data for further testing
    _, tracking_data = predefined_data  # Extract tracking data from predefined_data

    # Filter completion dates for the habit "reading"
    reading_dates = sorted([
        date for habit_name, date in tracking_data if habit_name == "reading"
    ])

    # Calculate the longest streak for "reading"
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(reading_dates))
    
    # Define the expected result based on reading completion dates
    expected_streak = 5  # Adjust this based on your calculation of the given data

    # Assert the result
    assert result == expected_streak, f"Longest streak for 'reading' should be {expected_streak}, but got {result}"
    # Test a sequence with mixed weeks and breaks
    completion_dates= ["2024-11-05",#week 45
                        "2024-11-06",#week 45
                        "2024-11-10",#week 45
                        "2024-11-18",#week 47
                        "2024-11-25",#week 48
                        "2024-12-05",#week 49
                        "2024-12-15",#week 50
                        "2024-12-16",#week 51
                        "2024-12-17",#week 51
                        ]
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 5, "Longest streak should be 1 for a single completion date"
    # Test with gaps in the weeks
    completion_dates= ["2024-11-05",#week 45
                        "2024-11-06",#week 45
                        "2024-11-10",#week 45
                        "2024-11-18",#week 47
                        "2024-11-25",#week 48
                        "2024-12-05",#week 49
                        "2024-12-15",#week 50
                        "2024-12-30",#week 52
                        ]
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 4 
    # Test with completely non-consecutive weeks
    completion_dates= ["2024-11-02",#week 44
                        "2024-11-11",#week 46
                        "2024-11-18",#week 47
                        "2024-12-15",#week 50
                        "2024-12-16",#week 51
                        "2024-12-23",#week 52
                        "2024-12-29",#week 52
                        ]
    result = analyzer.calculate_longest_streak_for_weekly_habit(sorted(completion_dates))
    assert result == 3
def test_get_longest_streak_for_given_habit(predefined_data, habit_tracker_db):
    """
    Test retrieving the longest streak for a given habit.

    This test checks the behavior of the `get_longest_streak_for_given_habit` function for different
    types of habits (weekly and daily).
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, mock_tracking_data = predefined_data

    # Test for a weekly habit with multiple streaks
    habit_name_weekly = "exercise"
    assert analyzer.get_longest_streak_for_given_habit(habit_name_weekly) == 3, \
        "Longest streak should be 3 for weekly habit with consecutive completions"

    
    #Test for a daily habit with a streak
    habit_name_daily = "meditation"
    assert analyzer.get_longest_streak_for_given_habit(habit_name_daily) == 6, \
        "Longest streak should be 6 for daily habit with consecutive completions"
def test_sort_habits_by_max_streak():
    """
    Test sorting habits by their maximum streak in descending order.

    This test verifies that the `sort_habits_by_max_streak` function correctly sorts habits based on
    their maximum streaks.
    """
    analyzer = HabitAnalyzer(None)  # No database connection needed for this test

    # Mock data for testing
    habit_streak_list = [
        ("coding", 7),
        ("exercise", 3), 
        ("meditation", 6),
        ("reading", 5), 
        ("water intake", 5), 
    ]

    # Expected result
    expected = [
        ("coding", 7),        # Longest streak for "coding"
        ("meditation", 6),    # Longest streak for "meditation"
        ("reading", 5),       # Longest streak for "reading"
        ("water intake", 5),  # Longest streak for "water intake"
        ("exercise", 3),      # Longest streak for "exercise"
    ]

    # Call the method and assert the result
    result = analyzer.sort_habits_by_max_streak(habit_streak_list)
    assert result == expected, "The sorted list does not match the expected order."
def test_calculate_longest_run_streak_of_all_defined_habits(predefined_data, habit_tracker_db):
    """
    Test calculating the longest streaks for all defined habits.

    This test checks the `calculate_longest_run_streak_of_all_defined_habits` function to ensure that it
    correctly calculates the longest streaks for each habit and sorts them in descending order.
    """
    analyzer = HabitAnalyzer(habit_tracker_db)
    mock_habits, _ = predefined_data

    # Execute the function to calculate the longest streaks
    result = analyzer.calculate_longest_run_streak_of_all_defined_habits()

    # Expected results based on the mock data


    expected = [
    ("coding", 7),        # Longest streak for "coding"
    ("meditation", 6),    # Longest streak for "meditation"
    ("reading", 5),       # Longest streak for "reading"
    ("water intake", 5),  # Longest streak for "water intake"
    ("exercise", 3),      # Longest streak for "exercise"
    ]

    # Validate that the result matches the expected output
    assert result == sorted(expected, key=lambda x: x[1], reverse=True), \
        "The calculated longest streaks do not match the expected results."

    # Additional validation: ensure all habits are included
    calculated_habits = [habit[0] for habit in result]
    expected_habits = [habit.name for habit in mock_habits]
    assert set(calculated_habits) == set(expected_habits), \
        "Not all habits are accounted for in the result."


    # Remove all tracking records for a specific habit
    habit_to_remove = "reading"
    habit_tracker_db.delete_tracking_records_of_habit(habit_to_remove)

    # Execute the function to calculate the longest streaks
    result = analyzer.calculate_longest_run_streak_of_all_defined_habits()

    # Expected results after removing tracking for 'reading'
    expected = [
        ("coding", 7),        # Longest streak for "coding"
        ("meditation", 6),    # Longest streak for "meditation"
        ("water intake", 5),  # Longest streak for "water intake"
        ("exercise", 3),      # Longest streak for "exercise"
        ("reading", 0),       # Longest streak for "reading"

    ]  # "reading"  has no tracking data

    # Validate that the result matches the expected output
    assert result == sorted(expected, key=lambda x: x[1], reverse=True), \
        "The calculated longest streaks do not match the expected results after removing a habit's tracking."
