from unittest.mock import patch, Mock
import pytest
from src.cli import UserInterface
from datetime import date,datetime
from tabulate import tabulate
# Mock class for Habit, used for testing UserInterface methods.
class MockHabit:
    def __init__(self, name, description, periodicity, creation_date=None, creation_time=None):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.creation_time = creation_time
# Fixture to initialize the UserInterface with a mock database.
@pytest.fixture
def user_interface(habit_tracker_db):
    """Fixture to initialize the UserInterface with a mock database."""
    return UserInterface(db=habit_tracker_db)
# Test the display_menu method to ensure correct menu handling.
def test_display_menu(user_interface):
    """Test the display_menu method to ensure correct menu handling."""

    # Define the mocked methods that correspond to menu options
    mock_methods = {
        "Create New Habit": "add_habit",
        "Modify an Existing Habit": "modify_habit",
        "Remove a Habit": "remove_habit",
        "Add Tracking Record for a Habit": "add_tracking_record",
        "Show All Habits": "show_all_habits",
        "Show All Tracking Records": "show_all_tracking_records",
        "Show List of Habits Based on Periodicity": "show_habits_by_periodicity",
        "Show Tracking Records for a Habit": "show_tracking_records_of_habit",
        "Show Struggling Habits from the Last Month": "show_struggling_habits_last_month",
        "Show Current Streak for a Habit": "show_current_streak_for_habit",
        "Show Longest Run Streak for a Habit": "show_longest_streak_for_given_habit",
        "Show Longest Run Streak Among All Defined Habits": "show_longest_run_streak_of_all_habits",
        "Exit": "exit_program"
    }

    # Patch the methods in UserInterface
    with patch("questionary.select") as mock_select:
        for menu_option, method_name in mock_methods.items():
            # Mock the questionary.select response to return the current method
            mock_method = patch.object(user_interface, method_name, return_value=None).start()
            mock_select.return_value.ask.return_value = getattr(user_interface, method_name)

            # Call the display_menu method
            user_interface.display_menu()

            # Assert the corresponding method was called
            mock_method.assert_called_once()

            # Stop patching the method
            patch.stopall()

            # Reset the mock for the next iteration
            mock_select.reset_mock()
def test_clear_screen_windows(user_interface):
    """Test the clear_screen method for Windows OS."""
    with patch("platform.system", return_value="Windows"), patch("os.system") as mock_os_system:
        user_interface.clear_screen()
        mock_os_system.assert_called_once_with('cls')
def test_clear_screen_unix(user_interface):
    """Test the clear_screen method for Unix-based OS."""
    with patch("platform.system", return_value="Linux"), patch("os.system") as mock_os_system:
        user_interface.clear_screen()
        mock_os_system.assert_called_once_with('clear')
# Test get_limited_length_input with valid input.
@patch("questionary.text")
def test_get_limited_length_input_valid(mock_questionary_text, user_interface):
    """Test get_limited_length_input with valid input."""
    # Simulate a valid input that is within the max length
    mock_questionary_text.return_value.ask.return_value = "ValidInput"

    result = user_interface.get_limited_length_input(
        value="ValidInput",
        prompt="Enter a value:",
        max_length=12,
    )
    # Assert the result matches the input value
    assert result == "ValidInput"
    mock_questionary_text.return_value.ask.assert_not_called()
def test_ensure_habit_exists(user_interface):
    """Test the ensure_habit_exists method to ensure it correctly checks for habit existence."""
    
    # Mock check_habit_exists method to simulate the existence of habits
    with patch.object(user_interface.analytics, "check_habit_exists") as mock_check_habit_exists:
        
        # Case 1: Habit exists in the database
        mock_check_habit_exists.return_value = True
        habit_name = "exercise"
        
        exists = user_interface.ensure_habit_exists(habit_name)
        
        # Assert that ensure_habit_exists returns True when the habit exists
        assert exists is True
        mock_check_habit_exists.assert_called_once_with(habit_name)
        
        # Case 2: Habit does not exist in the database
        mock_check_habit_exists.return_value = False
        habit_name = "nonexistent_habit"
        
        exists = user_interface.ensure_habit_exists(habit_name)
        
        # Assert that ensure_habit_exists returns False when the habit does not exist
        assert exists is False
        mock_check_habit_exists.assert_called_with(habit_name)
def test_ensure_lowercase_with_string(user_interface):
    """Test ensure_lowercase with a string input."""
    assert user_interface.ensure_lowercase("HELLO") == "hello"
    assert user_interface.ensure_lowercase("TeSt") == "test"
def test_ensure_lowercase_with_non_string(user_interface):
    """Test ensure_lowercase with non-string inputs."""
    assert user_interface.ensure_lowercase(123) == 123  # Integer input remains unchanged
    assert user_interface.ensure_lowercase(45.67) == 45.67  # Float input remains unchanged
def test_ensure_lowercase_with_special_characters(user_interface):
    """Test ensure_lowercase with strings containing special characters."""
    assert user_interface.ensure_lowercase("!@#$%^") == "!@#$%^"
    assert user_interface.ensure_lowercase("Hello, World!") == "hello, world!"
def test_get_valid_habit_name():
    ui = UserInterface()

    with patch("questionary.text") as mock_questionary_text, \
         patch.object(UserInterface, "ensure_habit_exists") as mock_ensure_habit_exists, \
         patch.object(UserInterface, "get_limited_length_input") as mock_get_limited_length_input:

        # Case 1: Habit does not exist
        mock_questionary_text.return_value.ask.side_effect = ["exercise"]
        mock_get_limited_length_input.side_effect = ["exercise"]
        mock_ensure_habit_exists.side_effect = [False]
        result = ui.get_valid_habit_name()
        assert result == "exercise"

        # Case 2: Habit already exists
        mock_questionary_text.return_value.ask.side_effect = ["exercise", "meditation"]
        mock_get_limited_length_input.side_effect = ["exercise", "meditation"]
        mock_ensure_habit_exists.side_effect = [True, False]
        result = ui.get_valid_habit_name()
        assert result == "meditation"

        # Case 3: Input too long
        mock_questionary_text.return_value.ask.side_effect = ["ThisIsAVeryLongHabitNameOverLimit", "exercise"]
        mock_get_limited_length_input.side_effect = ["exercise"]
        mock_ensure_habit_exists.side_effect = [False]
        result = ui.get_valid_habit_name()
        assert result == "exercise"
def test_get_description(user_interface):
    """Test the get_description method to ensure proper input handling."""
    
    # Case 1: User provides a valid description within the limit
    with patch("questionary.text") as mock_text:
        mock_text.return_value.ask.return_value = "This is a valid description"
        
        description = user_interface.get_description()
        
        # Assert that the returned description matches the mock input
        assert description == "This is a valid description"
        mock_text.assert_called_once_with("Enter the description of the habit  shorter than 100 characters:")

    # Case 2: User provides a description longer than the max length
    with patch("questionary.text") as mock_text:
        # Simulate the user entering a long description
        mock_text.return_value.ask.return_value = "A" * 200  # 200 characters
        
        # Mock the prompt asking for the description again
        with patch.object(user_interface, "get_limited_length_input") as mock_get_limited_length_input:
            mock_get_limited_length_input.return_value = "Short valid description"
            
            description = user_interface.get_description()
            
            # Assert that the returned description matches the corrected input
            assert description == "Short valid description"
            mock_text.assert_called_with("Enter the description of the habit  shorter than 100 characters:")
            mock_get_limited_length_input.assert_called_once()

    # Case 3: User provides an empty description
    with patch("questionary.text") as mock_text:
        # Simulate empty user input
        mock_text.return_value.ask.return_value = ""
        
        # Mock the prompt asking for the description again
        with patch.object(user_interface, "get_limited_length_input") as mock_get_limited_length_input:
            mock_get_limited_length_input.return_value = "Short valid description"
            
            description = user_interface.get_description()
            
            # Assert that the returned description matches the corrected input
            assert description == "Short valid description"
            mock_text.assert_called_with("Enter the description of the habit  shorter than 100 characters:")
            mock_get_limited_length_input.assert_called_once()
def test_get_periodicity(user_interface):
    """Test the get_periodicity method to ensure it handles periodicity selection correctly."""
    
    # Mock questionary.select to simulate user input
    
    # Case 1: User selects 'Daily' as periodicity
    with patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "daily"  # Simulate 'Daily' choice
        
        periodicity = user_interface.get_periodicity()
        
        # Assert that the returned periodicity is 'daily'
        assert periodicity == "daily"
        mock_select.assert_called_once_with("Please Choose a periodicity: ", choices=[
            {"name": "Daily", "value": "daily"},
            {"name": "Weekly", "value": "weekly"}
        ])
    
    # Case 2: User selects 'Weekly' as periodicity
    with patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "weekly"  # Simulate 'Weekly' choice
        
        periodicity = user_interface.get_periodicity()
        
        # Assert that the returned periodicity is 'weekly'
        assert periodicity == "weekly"
        mock_select.assert_called_once_with("Please Choose a periodicity: ", choices=[
            {"name": "Daily", "value": "daily"},
            {"name": "Weekly", "value": "weekly"}
        ])
def test_get_today_date(user_interface):
    """Test the get_today_date method to ensure it returns the date in YYYY-MM-DD format."""
    
    result = user_interface.get_today_date()
    assert result == date.today().strftime('%Y-%m-%d')
def test_get_valid_date(user_interface):
    """Test the get_valid_date method to ensure it correctly handles date input validation."""
    
    # Case 1: User enters a valid date
    with patch("builtins.input", return_value="2025-01-14"):  # Mock valid user input
        valid_date = user_interface.get_valid_date()
        
        # Assert that the returned date is correct
        assert valid_date == "2025-01-14"

    # Case 2: User enters an invalid date format once, then a valid date
    with patch("builtins.input", side_effect=["invalid-date", "2025-01-14"]):  # Mock invalid input, then valid input
        valid_date = user_interface.get_valid_date()
        
        # Assert that the returned date is correct
        assert valid_date == "2025-01-14"
    
    # Case 3: User enters an invalid date format repeatedly
    with patch("builtins.input", side_effect=["invalid-date", "another-invalid-date", "2025-01-14"]):
        valid_date = user_interface.get_valid_date()
        
        # Assert that the returned date is correct
        assert valid_date == "2025-01-14"
def test_get_date(user_interface):
    """Test the get_date method to ensure it correctly handles 'Today' and 'Custom Date' choices."""
    
    # Case 1: User selects 'Today'
    with patch("questionary.select") as mock_select, patch.object(user_interface, "get_today_date") as mock_get_today_date:
        # Simulate user selecting 'Today' and mock the get_today_date method to return a fixed date
        mock_select.return_value.ask.return_value = mock_get_today_date
        mock_get_today_date.return_value = "2025-01-14"  # Mock today date

        date_selected = user_interface.get_date("Select a date option:")
        
        # Assert that the returned date is '2025-01-14' (mocked today date)
        assert date_selected == "2025-01-14"
        mock_get_today_date.assert_called_once()

    # Case 2: User selects 'Custom Date' and enters a valid date
    with patch("questionary.select") as mock_select, patch.object(user_interface, "get_valid_date") as mock_get_valid_date:
        # Simulate user selecting 'Custom Date' and mock the get_valid_date method to return a valid custom date
        mock_select.return_value.ask.return_value = mock_get_valid_date
        mock_get_valid_date.return_value = "2025-01-15"  # Mock a custom date

        date_selected = user_interface.get_date("Select a date option:")
        
        # Assert that the returned date is '2025-01-15' (mocked custom date)
        assert date_selected == "2025-01-15"
        mock_get_valid_date.assert_called_once()
def test_get_valid_time(user_interface):
    """Test the get_valid_time method to ensure it handles time validation properly."""
    
    # Case 1: User enters a valid time
    with patch("builtins.input", return_value="14:30"):  # Mock valid user input
        valid_time = user_interface.get_valid_time()
        
        # Assert that the returned time is correct and formatted as HH:MM
        assert valid_time == "14:30"
    
    # Case 2: User enters an invalid time once, then a valid time
    with patch("builtins.input", side_effect=["invalid-time", "14:30"]):  # Mock invalid input, then valid input
        valid_time = user_interface.get_valid_time()
        
        # Assert that the returned time is correct and formatted as HH:MM
        assert valid_time == "14:30"
    
    # Case 3: User enters an invalid time format repeatedly
    with patch("builtins.input", side_effect=["invalid-time", "another-invalid-time", "14:30"]):
        valid_time = user_interface.get_valid_time()
        
        # Assert that the returned time is correct and formatted as HH:MM
        assert valid_time == "14:30"

    # Case 4: User enters a time in 24-hour format (e.g., 23:59)
    with patch("builtins.input", return_value="23:59"):  # Mock valid time input at the upper limit
        valid_time = user_interface.get_valid_time()
        
        # Assert that the returned time is correct and formatted as HH:MM
        assert valid_time == "23:59"
def test_check_dates(user_interface):
    """Test the check_dates function to ensure correct date validation and error handling."""

    # Case 1: Valid completion date (after creation date)
    with patch.object(user_interface, "get_date", return_value="2024-11-15"): 
        creation_date = "2024-11-10"
        completion_date = "2024-11-15"
        
        # Call check_dates with valid dates
        result = user_interface.check_dates(creation_date, completion_date)
        
        # Assert that the returned date is the same as the valid completion date
        assert result == datetime.strptime(completion_date, "%Y-%m-%d").date()

    # Case 2: Invalid completion date (before creation date)
    with patch.object(user_interface, "get_date", return_value="2024-11-20"):  # First invalid, then valid date
        creation_date = "2024-11-10"
        completion_date = "2024-11-05"  # Invalid, should prompt for a new date
        
        # Call check_dates, it should prompt for a new date and return the valid one (2024-11-20)
        result = user_interface.check_dates(creation_date, completion_date)
        
        # Assert that the returned date is valid
        assert result == datetime.strptime("2024-11-20", "%Y-%m-%d").date()

    # Case 3: Error in date format (invalid input)
    with patch.object(user_interface, "get_date", return_value="invalid-date-input"):
        creation_date = "2024-11-10"
        completion_date = "invalid-date-input"  # Invalid date
        
        # Call check_dates and assert that the exception is handled
        result = user_interface.check_dates(creation_date, completion_date)
        
        # Assert that None is returned due to invalid date input
        assert result is None
def test_is_date_in_completion_dates(user_interface, predefined_data):
    """Test the is_date_in_completion_dates function to ensure correct date checking."""
    
    # Case 1: Completion date exists in the habit's completion dates
    with patch.object(user_interface.analytics, "list_completion_dates_of_habit", return_value=[
        "2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04"]):
        habit_name = "meditation"
        completion_date = datetime.strptime("2024-11-02", "%Y-%m-%d").date()  # Valid date in the list
        
        # Call is_date_in_completion_dates
        result = user_interface.is_date_in_completion_dates(habit_name, completion_date)
        
        # Assert that the result is True, since the completion date is in the list
        assert result is True

    # Case 2: Completion date does not exist in the habit's completion dates
    with patch.object(user_interface.analytics, "list_completion_dates_of_habit", return_value=[
        "2024-11-01", "2024-11-03", "2024-11-04"]):
        habit_name = "meditation"
        completion_date = datetime.strptime("2024-11-02", "%Y-%m-%d").date()  # Invalid date not in the list
        
        # Call is_date_in_completion_dates
        result = user_interface.is_date_in_completion_dates(habit_name, completion_date)
        
        # Assert that the result is False, since the completion date is not in the list
        assert result is False

    # Case 3: The habit has no completion dates (i.e., the list is None)
    with patch.object(user_interface.analytics, "list_completion_dates_of_habit", return_value=None):
        habit_name = "nonexistent_habit"
        completion_date = datetime.strptime("2024-11-02", "%Y-%m-%d").date()  # Any valid date
        
        # Call is_date_in_completion_dates
        result = user_interface.is_date_in_completion_dates(habit_name, completion_date)
        
        # Assert that the result is False, since no completion dates exist
        assert result is False
def test_get_valid_completion_date(user_interface, predefined_data):
    """Test that the get_valid_completion_date function returns a valid date that is not already saved."""
    
    habit_name = "meditation"
    valid_date = datetime.strptime("2024-12-12", "%Y-%m-%d").date()
    
    # Mock the relevant methods
    with patch.object(user_interface, "check_dates", return_value=valid_date), \
         patch.object(user_interface, "get_date", return_value="2024-12-12"), \
         patch.object(user_interface, "is_date_in_completion_dates", return_value=False) as mock_is_date_in_completion_dates:

        # Call the method
        completion_date = user_interface.get_valid_completion_date(habit_name)
        
        # Assert that the valid date is returned and the duplicate check is not triggered
        assert completion_date == valid_date
        mock_is_date_in_completion_dates.assert_called_once_with(habit_name, valid_date)
def test_select_habit_name_no_habits(user_interface):
    # Mock the behavior of list_habit_names to return an empty list (no habits)
    with patch.object(user_interface.analytics, 'list_habit_names', return_value=[]):
        # Patch the questionary.select to avoid user interaction
        with patch('questionary.select') as mock_select:
            mock_select.return_value.ask.return_value = None
            result = user_interface.select_habit_name()
            assert result is None
            mock_select.assert_not_called()  # No selection should have been made
def test_select_habit_name_with_habits(user_interface):
    # Mock list_habit_names to return a list of habits
    with patch.object(user_interface.analytics, 'list_habit_names', return_value=['exercise', 'reading', 'coding']):
        # Patch questionary.select to simulate user selecting 'reading'
        with patch('questionary.select') as mock_select:
            mock_select.return_value.ask.return_value = 'reading'
            result = user_interface.select_habit_name()
            assert result == 'reading'  # The returned habit should be 'reading'
            mock_select.assert_called_once()  # The select method should be called once
def test_final_menu(user_interface):
    """Test the final_menu method to ensure correct option handling."""
    with patch("questionary.select") as mock_select, patch.object(user_interface, "clear_screen") as mock_clear_screen, patch.object(user_interface, "exit_program") as mock_exit_program:
        # Mock the menu choice to "Back to Main Menu"
        mock_select.return_value.ask.return_value = mock_clear_screen

        # Call the final_menu method
        user_interface.final_menu()

        # Assert clear_screen is called
        mock_clear_screen.assert_called_once()

        # Mock the menu choice to "Exit"
        mock_select.return_value.ask.return_value = mock_exit_program

        # Call the final_menu method
        user_interface.final_menu()

        # Assert exit_program is called
        mock_exit_program.assert_called_once()
def test_add_habit(user_interface):
    """Test the add_habit method to ensure correct habit creation and navigation."""
    # Mock user inputs for the habit details
    with patch.object(user_interface, "get_valid_habit_name", return_value="Test Habit"), \
         patch.object(user_interface, "get_description", return_value="This is a test habit"), \
         patch.object(user_interface, "get_periodicity", return_value="daily"), \
         patch.object(user_interface, "get_date", return_value="2025-01-13"), \
         patch.object(user_interface, "get_valid_time", return_value="10:00"), \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the add_habit method
        user_interface.add_habit()

        # Verify the habit exists in the database
        assert user_interface.habit_db.habit_exists("Test Habit"), "The habit should exist in the database."

        # Verify the final_menu method is called
        mock_final_menu.assert_called_once()
def test_remove_habit(user_interface):
    """Test the remove_habit method to ensure correct habit deletion and tracking records removal."""
    # Prepopulate the database with a habit and associated tracking records
    habit_name = "exercise"
    # Mock user inputs for removing the habit
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch("questionary.confirm", return_value=Mock(return_value=True)), \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the remove_habit method
        user_interface.remove_habit()

        # Verify the habit no longer exists in the database
        assert not user_interface.habit_db.habit_exists(habit_name), "The habit should be removed from the database."

        # Verify the tracking records for the habit are removed
        tracking_records = user_interface.analytics.check_tracking_records_of_habit_exists(habit_name)
        assert not tracking_records, "Tracking records for the removed habit should be deleted."

        # Verify the final_menu method is called
        mock_final_menu.assert_called_once()
def test_modify_habit(user_interface):
    """Test the modify_habit method to ensure habits are updated correctly."""
    habit_name = "meditation"

    # Mock user inputs and method behaviors
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch("questionary.confirm", return_value=Mock(return_value=True)), \
         patch.object(user_interface, "get_description", return_value="Updated meditation habit"), \
         patch.object(user_interface, "get_periodicity", return_value="weekly"), \
         patch.object(user_interface.analytics, "get_habit_description_and_periodicity", return_value=("Daily meditation habit", "daily")), \
         patch.object(user_interface.analytics, "get_habit_periodicity_str", return_value="daily"), \
         patch.object(user_interface.analytics, "check_tracking_records_of_habit_exists", return_value=[("2024-11-01",), ("2024-11-02",)]), \
         patch.object(user_interface.analytics, "remove_tracking_records_of_habit") as mock_remove_tracking_records, \
         patch.object(user_interface, "final_menu") as mock_final_menu, \
         patch("src.cli.Habit.modify_habit") as mock_modify_habit:

        # Call the modify_habit method
        user_interface.modify_habit()

        # Verify that the habit modification was called with updated details
        mock_modify_habit.assert_called_once_with()
        print("modify_habit was called with updated details.")

        # Verify that tracking records were removed due to periodicity change
        mock_remove_tracking_records.assert_called_once_with(habit_name)

        # Verify final_menu is called after the modification
        mock_final_menu.assert_called_once()

        print("Test passed: Habit modification successful.")
def test_add_tracking_record(user_interface):
    """Test the add_tracking_record method to ensure tracking records are added correctly."""
    habit_name = "meditation"
    completion_date = "2025-01-13"

    # Mock user inputs and method behaviors
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch.object(user_interface, "get_valid_completion_date", return_value=completion_date), \
         patch.object(user_interface.analytics, "add_new_tracking_record") as mock_add_new_tracking_record, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the add_tracking_record method
        user_interface.add_tracking_record()

        # Verify that the tracking record was added
        mock_add_new_tracking_record.assert_called_once_with(habit_name, completion_date)
        print("add_new_tracking_record was called with correct arguments.")

        # Verify final_menu is called after adding the record
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Tracking record added successfully.")
def test_show_all_tracking_records(user_interface):
    """Test the show_all_tracking_records method to ensure tracking records are displayed correctly."""
    # Mock tracking records
    tracking_records = [
        (1, "meditation", "2025-01-13"),
        (2, "exercise", "2025-01-14"),
    ]

    # Expected formatted tracking records
    formatted_tracking_records = [
        ("meditation", "2025-01-13"),
        ("exercise", "2025-01-14"),
    ]

    # Mock the analytics method and the final_menu call
    with patch.object(user_interface.analytics, "list_all_tracking_records", return_value=tracking_records), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_all_tracking_records method
        user_interface.show_all_tracking_records()

        # Verify list_all_tracking_records is called
        user_interface.analytics.list_all_tracking_records.assert_called_once()
        print("list_all_tracking_records was called.")

        # Verify the print output includes the formatted tracking records
        formatted_table = tabulate(formatted_tracking_records, headers=['Habit', 'Completion Date'], tablefmt='grid')
        mock_print.assert_any_call(formatted_table)

        # Verify final_menu is called after showing records
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: All tracking records were displayed correctly.")
def test_show_habits_by_periodicity(user_interface):
    """Test the show_habits_by_periodicity method to ensure habits are filtered and displayed correctly."""
    # Mock input periodicity and corresponding habits data
    periodicity = "daily"
    habits = [
        (1, "meditation", "Daily meditation habit", "daily", "2024-10-30 22:00:00", "22:00"),
        (2, "exercise", "Daily exercise habit", "daily", "2024-11-01 07:00:00", "07:00"),
    ]

    # Expected formatted habits for tabulate
    formatted_habits = [
        ("meditation", "Daily meditation habit", "daily", "2024-10-30", "22:00"),
        ("exercise", "Daily exercise habit", "daily", "2024-11-01", "07:00"),
    ]

    # Mock the required methods and dependencies
    with patch.object(user_interface, "get_periodicity", return_value=periodicity), \
         patch.object(user_interface.analytics, "list_habits_by_periodicity", return_value=habits), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_habits_by_periodicity method
        user_interface.show_habits_by_periodicity()

        # Verify that get_periodicity is called
        user_interface.get_periodicity.assert_called_once()
        print("get_periodicity was called.")

        # Verify list_habits_by_periodicity is called with the correct periodicity
        user_interface.analytics.list_habits_by_periodicity.assert_called_once_with(periodicity)
        print("list_habits_by_periodicity was called with periodicity:", periodicity)

        # Verify the printed table includes the formatted habits
        formatted_table = tabulate(
            formatted_habits,
            headers=['Habit Name', 'Description', 'Periodicity', 'Creation Date', 'Creation Time '],
            tablefmt='grid',
        )
        mock_print.assert_any_call(formatted_table)

        # Verify final_menu is called
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Habits by periodicity were displayed correctly.")
def test_show_tracking_records_of_habit(user_interface):
    """Test the show_tracking_records_of_habit method to ensure tracking records are displayed correctly."""
    # Mock input habit name and corresponding tracking records
    habit_name = "meditation"
    tracking_records = [
        (1, "meditation", "2025-01-13 10:00:00"),
        (2, "meditation", "2025-01-14 10:00:00"),
    ]

    # Expected formatted tracking records for tabulate
    formatted_tracking_records = [
        ("meditation", "2025-01-13"),
        ("meditation", "2025-01-14"),
    ]

    # Mock the required methods and dependencies
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch.object(user_interface.analytics, "list_tracking_records_of_habit", return_value=tracking_records), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_tracking_records_of_habit method
        user_interface.show_tracking_records_of_habit()

        # Verify that select_habit_name is called
        user_interface.select_habit_name.assert_called_once()
        print("select_habit_name was called.")

        # Verify list_tracking_records_of_habit is called with the correct habit name
        user_interface.analytics.list_tracking_records_of_habit.assert_called_once_with(habit_name)
        print("list_tracking_records_of_habit was called with habit name:", habit_name)

        # Verify the printed table includes the formatted tracking records
        formatted_table = tabulate(
            formatted_tracking_records,
            headers=['Habit', 'Completion Date'],
            tablefmt='grid',
        )
        mock_print.assert_any_call(formatted_table)

        # Verify final_menu is called
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Tracking records of habit were displayed correctly.")
def test_show_struggling_habits_last_month(user_interface):
    """Test the show_struggling_habits_last_month method to ensure struggling habits are displayed correctly."""
    # Mock data for struggling habits
    struggling_habits = [
        ("meditation", 2),
        ("exercise", 1),
    ]

    # Expected formatted habits for tabulate
    formatted_habits = [
        ("meditation", 2),
        ("exercise", 1),
    ]

    # Mock the required methods and dependencies
    with patch.object(user_interface.analytics, "find_struggling_habits_last_month", return_value=struggling_habits), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_struggling_habits_last_month method
        user_interface.show_struggling_habits_last_month()

        # Verify that find_struggling_habits_last_month is called
        user_interface.analytics.find_struggling_habits_last_month.assert_called_once()
        print("find_struggling_habits_last_month was called.")

        # Verify the print output includes the formatted struggling habits table
        formatted_table = tabulate(
            formatted_habits,
            headers=['Habit Name', 'Completion Times'],
            tablefmt='grid',
        )
        mock_print.assert_any_call("The struggling habits in the last month:")
        mock_print.assert_any_call(formatted_table)

        # Verify the top struggling habit is printed correctly
        mock_print.assert_any_call("Your top struggled habit last month: meditation 2 times")

        # Verify final_menu is called
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Struggling habits for the last month were displayed correctly.")
def test_show_current_streak_for_habit(user_interface):
    """Test the show_current_streak_for_habit method to ensure the correct streak is displayed."""
    # Mock habit name and tracking data
    habit_name = "meditation"
    tracking_records = [
        (1, "meditation", "2025-01-10"),
        (2, "meditation", "2025-01-11"),
        (3, "meditation", "2025-01-12"),
        (4, "meditation", "2025-01-13"),
    ]
    current_streak = 4  # Mocked current streak value

    # Mock the required methods and behaviors
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch.object(user_interface.analytics, "list_tracking_records_of_habit", return_value=tracking_records), \
         patch.object(user_interface.analytics, "get_current_streak_for_habit", return_value=current_streak), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_current_streak_for_habit method
        user_interface.show_current_streak_for_habit()

        # Verify that list_tracking_records_of_habit is called
        user_interface.analytics.list_tracking_records_of_habit.assert_called_once_with(habit_name)
        print("list_tracking_records_of_habit was called.")

        # Verify that get_current_streak_for_habit is called
        user_interface.analytics.get_current_streak_for_habit.assert_called_once_with(habit_name)
        print("get_current_streak_for_habit was called.")

        # Verify the correct streak is printed
        mock_print.assert_any_call(f"Your Current Streak for {habit_name} is {current_streak}")

        # Verify final_menu is called
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Current streak for the habit was displayed correctly.")
def test_show_longest_streak_for_given_habit(user_interface):
    """Test the show_longest_streak_for_given_habit method to ensure the correct longest streak is displayed."""
    # Mock habit name and longest streak data
    habit_name = "meditation"
    longest_streak = 10  # Mocked longest streak value

    # Mock the required methods and behaviors
    with patch.object(user_interface, "select_habit_name", return_value=habit_name), \
         patch.object(user_interface.analytics, "get_longest_streak_for_given_habit", return_value=longest_streak), \
         patch("builtins.print") as mock_print, \
         patch.object(user_interface, "final_menu") as mock_final_menu:

        # Call the show_longest_streak_for_given_habit method
        user_interface.show_longest_streak_for_given_habit()

        # Verify that select_habit_name is called
        user_interface.select_habit_name.assert_called_once()
        print("select_habit_name was called.")

        # Verify that get_longest_streak_for_given_habit is called
        user_interface.analytics.get_longest_streak_for_given_habit.assert_called_once_with(habit_name)
        print("get_longest_streak_for_given_habit was called.")

        # Verify the correct longest streak message is printed
        mock_print.assert_any_call(f"The longest streak for {habit_name} is :", longest_streak)

        # Verify final_menu is called
        mock_final_menu.assert_called_once()
        print("final_menu was called.")

        print("Test passed: Longest streak for the habit was displayed correctly.")
# Test for the exit_program method
def test_exit_program(user_interface):
    """Test the exit_program method to ensure it exits the program correctly."""
    with patch("builtins.exit") as mock_exit, \
         patch.object(user_interface, "clear_screen") as mock_clear_screen, \
         patch("builtins.print") as mock_print:

        # Call the exit_program method
        user_interface.exit_program()

        # Ensure clear_screen was called
        mock_clear_screen.assert_called_once()

        # Ensure the exit message was printed
        mock_print.assert_called_with("Exiting the program...")

        # Ensure exit() was called to exit the program
        mock_exit.assert_called_once()
