from unittest.mock import MagicMock, patch
from src.main import main

@patch("src.main.HabitTrackerDB")
@patch("src.main.UserInterface")
def test_main_flow(mock_ui_class, mock_db_class):
    """
    Test the main function by mocking the HabitTrackerDB and UserInterface classes.
    Ensures that the main flow initializes the database, passes it to the UI,
    runs the UI, and properly closes the database.

    Args:
        mock_ui_class (MagicMock): Mocked class for UserInterface.
        mock_db_class (MagicMock): Mocked class for HabitTrackerDB.
    """
    # Mock the HabitTrackerDB instance to simulate the database behavior
    mock_db_instance = MagicMock()
    mock_db_class.return_value = mock_db_instance

    # Mock the UserInterface instance to simulate the UI behavior
    mock_ui_instance = MagicMock()
    mock_ui_class.return_value = mock_ui_instance

    # Run the main function, which is the entry point for the application
    main()

    # Assertions to verify correct behavior:
    mock_db_class.assert_called_once()  # Ensure HabitTrackerDB was instantiated once
    mock_ui_class.assert_called_once_with(mock_db_instance)   # Ensure UI was initialized with the mocked DB instance
    mock_ui_instance.run.assert_called_once()  # Ensure the UI's 'run' method was called once
    mock_db_instance.close.assert_called_once() # Ensure the DB's 'close' method was called to clean up
