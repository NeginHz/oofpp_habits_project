import questionary
from datetime import date,datetime
from .habit import Habit
from .database import HabitTrackerDB
from .analytics import HabitAnalyzer
import os
import platform
from tabulate import tabulate
class UserInterface:
    """
    A command-line interface (CLI) for managing and analyzing habits in the Habit Tracker application.
    Provides methods for interacting with the user, such as creating, modifying, and analyzing habits,
    as well as displaying analytics and tracking records.

    Attributes:
        habit_db (HabitTrackerDB): Instance of the HabitTrackerDB for habit data management.
        analytics (HabitAnalyzer): Instance of HabitAnalyzer for analyzing habit data.
    """
    def __init__(self, db=HabitTrackerDB()):
        """
        Initialize the UserInterface class with a HabitTrackerDB instance.

        Args:
            db (HabitTrackerDB): The database instance to manage habits and records. Defaults to HabitTrackerDB().
        """
        self.habit_db = db
        self.analytics = HabitAnalyzer(self.habit_db)
    def display_menu(self):
        
        """
        Display the main menu and execute the selected option.
        Presents the user with a list of options related to habit management and tracking.
        The selected option triggers the corresponding method.
        """
        menu_choices =[
            {"name": "Create New Habit", "value": self.add_habit},
            {"name": "Modify an Existing Habit", "value": self.modify_habit},
            {"name": "Remove a Habit", "value": self.remove_habit},
            {"name": "Add Tracking Record for a Habit", "value": self.add_tracking_record},
            {"name": "Show All Habits", "value": self.show_all_habits},
            {"name": "Show All Tracking Records", "value": self.show_all_tracking_records},
            {"name": "Show List of Habits Based on Periodicity", "value": self.show_habits_by_periodicity },
            {"name": "Show Tracking Records for a Habit", "value": self.show_tracking_records_of_habit}, 
            {"name": "Show Struggling Habits from the Last Month", "value": self.show_struggling_habits_last_month},
            {"name": "Show Current Streak for a Habit", "value": self.show_current_streak_for_habit},
            {"name": "Show Longest Run Streak for a Habit", "value": self.show_longest_streak_for_given_habit},
            {"name": "Show Longest Run Streak Among All Defined Habits", "value": self.show_longest_run_streak_of_all_habits},
            {"name": "Exit", "value": self.exit_program}
        ]

        # Use questionary to display the menu and get the user's choice
        choice = questionary.select("Please Choose an option:", choices=menu_choices).ask()
        # Call the corresponding method for the selected choice
        if choice:
            choice()
    def clear_screen(self):
        """
        Clears the terminal screen based on the operating system.
        """
        # Get the operating system name
        os_name = platform.system()
        if os_name == "Windows":
            os.system('cls')  # For Windows
        else:
            os.system('clear')  # For Unix-based systems
    def ensure_lowercase(self,value):
        """
        Convert the input value to lowercase if it's a string.

        Args:
            value (str, int, or float): The value to be processed.

        Returns:
            str, int, or float: The lowercase string if the input is a string,
            otherwise the unchanged input value.
        """
        if isinstance(value, str):
            return value.lower()
        return value
    def get_limited_length_input(self,value,prompt,max_length):
        """
        Validate user input to ensure it meets length restrictions.

        Args:
            value (str): The initial input value.
            prompt (str): The prompt message for the user.
            max_length (int): Maximum allowed length for the input.

        Returns:
            str: A valid user input.
        """
        while True:
            user_input = value.strip() # Strip leading and trailing whitespace
            if not user_input:
                print("Cannot be empty. Please try again.")
                value = questionary.text(prompt).ask()
            elif len(user_input) > max_length:  # Check if the input is too long
                print(f"this is too long. Please enter shorter than {max_length} characters.")
                value = questionary.text(prompt).ask()
            else:
                return user_input
    def ensure_habit_exists(self, habit_name):
        """
        Check if the habit exists in the database.

        Args:
            habit_name (str): The name of the habit to check.

        Returns:
            bool: True if the habit exists, False otherwise.
        """
        return self.analytics.check_habit_exists(habit_name)
    def get_valid_habit_name(self):
        """
        Prompt the user for a valid habit name that doesn't already exist in the database.

        Returns:
            str: A unique habit name.
        """
        max_length=25
        name = self.ensure_lowercase(self.get_limited_length_input(questionary.text(f"Enter the name of the habit shorter than {max_length} characters:").ask(),"Enter the name of the habit again:",max_length))
        
        while self.ensure_habit_exists(name.strip()):
            print(f"{name} is already added,please type new name.")
            name = self.ensure_lowercase(self.get_limited_length_input(questionary.text(f"Enter the name of the habit shorter than {max_length} characters:").ask(),"Enter the name of the habit again:",max_length))
        return name
    def get_description(self):
        """
        Prompt the user for a non-empty description of the habit.

        Returns:
            str: A valid description for the habit.
        """
        max_length=100
        return self.get_limited_length_input(questionary.text(f"Enter the description of the habit  shorter than {max_length} characters:").ask(),"Enter the description of the habit again:",max_length)
    def get_periodicity(self):
        """
        Prompt the user to select the periodicity of the habit.

        Returns:
            str: The selected periodicity ('daily' or 'weekly').
        """
        periodicity_choices=[
            {"name": "Daily", "value": "daily"},
            {"name": "Weekly", "value": "weekly"}
            ]
        return questionary.select("Please Choose a periodicity: ", choices=periodicity_choices).ask()
    def get_today_date(self):
        """
        Return today's date in YYYY-MM-DD format.

        Returns:
        str: The current date as a string in the format YYYY-MM-DD.
        """
        return date.today().strftime('%Y-%m-%d')  
    def get_valid_date(self):
        """
        Prompt the user to input a date, validate the input, and return it in YYYY-MM-DD format.

        This function continuously prompts the user to enter a date in the format YYYY-MM-DD.
        It uses the `date.fromisoformat` method to validate the input. If the input is valid,
        the date is returned as a string in the format YYYY-MM-DD. If the input is invalid,
        the user is prompted to enter the date again until a valid date is provided.

        Returns:
        str: The valid date entered by the user, formatted as a string in the format YYYY-MM-DD.

        Raises:
        ValueError: If the user input cannot be converted to a valid date in the format YYYY-MM-DD.
        """
        while True:
            # Prompt user for date input
            user_input = input("Enter a date (YYYY-MM-DD): ")
            
            try:
                # Try to parse the date input into a date object
                valid_date = date.fromisoformat(user_input)
                # Return the date in YYYY-MM-DD format
                return valid_date.strftime('%Y-%m-%d')
            except ValueError:
                # If parsing fails, prompt user again
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    def get_date(self,prompt):
        """
        Return today's date in YYYY-MM-DD format.

        Returns:
            str: The current date as a string in the format YYYY-MM-DD.
        """
        date_choices=[
            {"name": "Today", "value": self.get_today_date},
            {"name": "Custom Date", "value": self.get_valid_date}
            ]
        date = questionary.select(prompt, choices=date_choices).ask()
        return date()
    def get_valid_time(self):
        """
        Prompt the user for a valid time input in HH:MM format.
        
        Returns:
            str: A valid time string in HH:MM format.
        """
        while True:
            time_input = input("Please enter the creation time in 24-hour format (HH:MM), between 00:00 and 23:59:  ")
            try:
                # Attempt to parse the input time
                valid_time = datetime.strptime(time_input, "%H:%M")
                
                # Return the time as a string in HH:MM format
                return valid_time.strftime("%H:%M")
            except ValueError:
                print("Invalid input. Please ensure the time in 24-hour format (HH:MM), between 00:00 and 23:59 , and try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")
    def check_dates(self,creation_date,completion_date):
        """
        Validate that the completion date is not before the creation date.

        Args:
            creation_date (str): The creation date in YYYY-MM-DD format.
            completion_date (str): The completion date in YYYY-MM-DD format.

        Returns:
            date: A valid completion date.
        """
        try:
            # Convert the input strings to date objects
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d').date()
            completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
            
            # Ensure the completion date is after the creation date
            while creation_date > completion_date:
                print(f"Invalid date: Completion Date {completion_date} should be after Creation Date {creation_date}.")
                completion_date=self.get_date("Enter completion date ")
                completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
            return completion_date  # Return the valid dates object
        
        except ValueError as e:
            print("Error:", e)
            print("Please ensure the dates are in the correct format (YYYY-MM-DD).")
            return None
    def is_date_in_completion_dates(self,habit_name,completion_date):
        """
        Check if the completion date exists in the habit's recorded completion dates.

        Args:
            habit_name (str): The name of the habit.
            completion_date (date): The completion date to check.

        Returns:
            bool: True if the date exists, False otherwise.
        """
        try:
            completion_dates_of_habit=self.analytics.list_completion_dates_of_habit(habit_name)
            if completion_dates_of_habit is not None:
                return completion_date.strftime('%Y-%m-%d') in completion_dates_of_habit
            else:
                return False

        except Exception as e:
            print(f"An error occurred while in is_date_in_completion_dates function: {e}")
    def get_valid_completion_date(self,habit_name):
        """
        Prompt the user for a valid completion date that is not already recorded.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            date: A valid completion date.
        """
        try:
            completion_date =self.check_dates(self.analytics.get_creation_date_of_habit(habit_name),self.get_date("Enter completion date "))
        
            while self.is_date_in_completion_dates(habit_name,completion_date):
                print(f"The date {completion_date} is already Saved. Please enter a different date:")
                completion_date=self.get_valid_completion_date(habit_name)
        
            return completion_date
        except Exception as e:
            print(f"An error occurred while in get_valid_completion_date function: {e}")
    def select_habit_name(self):
        """
        Allow the user to select a habit name from the available habits.

        Returns:
            str: The selected habit name, or None if no habits are available.
        """
        habits=self.analytics.list_habit_names()
        try:
            # Check if habits is None or an empty list
            if habits is None:
                print("No habits found. Please create a habit first.")
                return None
            
            if not habits:
                print("No habits available for selection.")
                return None
            response = questionary.select(
                "Select your habit name:",
                choices=habits
            ).ask()

            if response:
                print(f"You selected {response}.")
                return response
            else:
                print("No option selected.")

        except Exception as e:
            print(f"An error occurred: {e}")
    def final_menu(self):
        """
        Display a menu with options to return to the main menu or exit the program.
        """
        menu_choices =[
            {"name": "Back to Main Menu", "value": self.clear_screen },
            {"name": "Exist", "value": self.exit_program}
        ]
        choice = questionary.select("Please Choose an option:", choices=menu_choices).ask()

        # Call the corresponding method for the selected choice
        if choice:
            choice() 
    def add_habit(self):
        """
        Add a new habit to the tracker.
        
        This method handles the logic for creating and storing a new habit.
        """

        name=self.get_valid_habit_name() # Get a valid name for the habit
        description = self.get_description() # Get the habit's description
        periodicity = self.get_periodicity() # Get the habit's periodicity
        creation_date= self.get_date("Select your creation date:") # Get the creation date
        creation_time=self.get_valid_time() # Get the creation time
        # Create a new Habit instance and add it
        habit = Habit(name, description, periodicity, creation_date,creation_time,self.habit_db)
        habit.add_habit()
        print("Habit added successfully!")
        self.final_menu()
    def modify_habit(self):
        """
        Modify an existing habit.
        
        This method allows the user to update the details of a habit that has already been created.
        """
        
        try:
            habit_name=self.select_habit_name() # Select a habit to modify
            # Fetch current description and periodicity only if habit_name is not None
            if habit_name is not None:
                # Prompt user for new details
                description, periodicity = self.analytics.get_habit_description_and_periodicity(habit_name)
                
                # Ask the user if they want to modify each field
                if questionary.confirm("Do you want to change the description?").ask():
                    description = self.get_description()
                
                if questionary.confirm("Do you want to change the periodicity?").ask():
                    periodicity = self.get_periodicity()
                    old_periodicity=self.analytics.get_habit_periodicity_str(habit_name)
                    # Handle changes in periodicity and associated tracking records
                    if periodicity != old_periodicity:
                        records=self.analytics.check_tracking_records_of_habit_exists(habit_name)
                        if records:
                            print(f"Found {len(records)} tracking records for habit '{habit_name}' Because you changed the periodicity Previous tracking records should be deleted. Deleting now...")
                            self.analytics.remove_tracking_records_of_habit(habit_name)
                            print("Tracking records deleted successfully.")
                            #removed Tracking
                        else:
                            print(f"Because you changed the periodicity Previous tracking records should be deleted but There wasnt any Previous tracking records for '{habit_name}'  habit!")
                    else: 
                        # Optional: Remove old tracking records even if periodicity didn't change
                        confirmation = questionary.confirm(f"Although the periodicity of '{habit_name}' did not change, Do you want to remove previous tracking records of '{habit_name}'?").ask()
                        if confirmation:
                            records=self.analytics.check_tracking_records_of_habit_exists(habit_name)
                            if records:
                                print(f"Found {len(records)} tracking records for habit '{habit_name}'. Deleting now...")
                                self.analytics.remove_tracking_records_of_habit(habit_name)
                                print("Tracking records deleted successfully.")
                                #removed Tracking
                            else:
                                print(f"There wasnt any Previous tracking records for '{habit_name}' habit!")

                # Update the habit
                habit = Habit(habit_name, description, periodicity, creation_date=None, creation_time=None)
                habit.modify_habit()
                print("Habit modified successfully!")
        except Exception as e:
            print(f"An error occurred while modifying the habit: {e}")
        self.final_menu()
    def remove_habit(self):
        """
        Remove a habit from the tracker.
        
        This method handles the logic for deleting a habit from the tracker.
        """
        try:
            habit_name=self.select_habit_name()
            # only if habit_name is not None
            if habit_name is not None:
                confirmation = questionary.confirm(f"Are you sure you want to remove habit '{habit_name}'?").ask()
                if confirmation:
                        habit = Habit(habit_name, description=None, periodicity=None, creation_date=None, creation_time=None)
                        habit.remove_habit()

                        records=self.analytics.check_tracking_records_of_habit_exists(habit_name)
                        if records:
                            print(f"Found {len(records)} tracking records for habit '{habit_name}'. Deleting now...")
                            self.analytics.remove_tracking_records_of_habit(habit_name)
                            print("Tracking records deleted successfully.")
                            #removed Tracking
                        else:
                            print("There wasnt any tracking record for this habit!")
                   
                        print("Habit removed successfully!")
                else:
                    print("No habit was removed. The habits remain unchanged.")
        except Exception as e:
            print(f"An error occurred while removing the habit: {e}")
        self.final_menu()
    def add_tracking_record(self):
        """
        Add a tracking record for a specific habit.
        
        This method allows the user to log progress or activity related to a specific habit.
        """
        try:
            habit_name=self.select_habit_name()
            if habit_name is not None:
                completion_date =self.get_valid_completion_date(habit_name)
                self.analytics.add_new_tracking_record(habit_name, completion_date)
                #self.habit_db.insert_tracking_record(habit_name, completion_date)
                print("Tracking record added successfully!")
        except Exception as e:
            print(f"An error occurred while add tracking record : {e}")
        self.final_menu()
    def show_all_habits(self):
        """
        Display all habits currently being tracked.
        
        This method lists all the habits that have been created by the user.
        """
        habits=self.analytics.get_habits_info()
        if habits:
            # Transform data to match the desired format
            formatted_habits = [(habit, description, periodicity, date.split()[0] , time) for _, habit, description, periodicity, date,time in habits]

            # Print table with headers
            print(tabulate(formatted_habits, headers=['Habit Name', 'Description', 'Periodicity', 'Creation Date','Creation Time'], tablefmt='grid'))

        else:
            print("No habits found.")

        self.final_menu()
    def show_all_tracking_records(self):
        """
        Display all tracking records for all habits.
        
        This method provides a comprehensive view of all the tracking records associated with all habits.
        """
        tracking_records=self.analytics.list_all_tracking_records()
        if tracking_records:
            # Transform data to match the desired format
            formatted_tracking_records = [(habit, date.split()[0]) for _, habit, date in tracking_records]
            # Print table
            print(tabulate(formatted_tracking_records, headers=['Habit', 'Completion Date'], tablefmt='grid'))
        else:
            print("No tracking records found.")
        self.final_menu()
    def show_habits_by_periodicity(self):
        """
        Display habits based on their periodicity (e.g., daily, weekly).
        
        This method filters and shows habits according to the frequency with which they are tracked.
        """
        periodicity = self.get_periodicity()
        habits = self.analytics.list_habits_by_periodicity(periodicity)
        if habits:
            # Transform data to match the desired format
            formatted_habits = [(habit, description, periodicity, date.split()[0] ,creation_time ) for _, habit, description, periodicity, date ,creation_time  in habits]
            # Print table with headers
            print(tabulate(formatted_habits, headers=['Habit Name', 'Description', 'Periodicity', 'Creation Date' , 'Creation Time '], tablefmt='grid'))

        else:
            print("No habits found with the given periodicity.")
        self.final_menu()
    def show_tracking_records_of_habit(self):
        """
        Display tracking records for a specific habit by its name.

        This method retrieves and displays the tracking history for a selected habit
        identified by its unique name, formatted in a table for readability.
        """
        try:
            habit_name=self.select_habit_name()
            if habit_name is not None:
                tracking_records=self.analytics.list_tracking_records_of_habit(habit_name)
                if tracking_records:
                    # Transform data to match the desired format: (Habit, Completion Date)
                    formatted_tracking_records = [(habit, date.split()[0]) for _, habit, date in tracking_records]

                    # Display the tracking records in a tabular format
                    print(tabulate(formatted_tracking_records, headers=['Habit', 'Completion Date'], tablefmt='grid'))

                else:
                    print(f"No tracking records for {habit_name} found.")
        except Exception as e:
            print(f"An error occurred while show tracking records of  habit : {e}")
        self.final_menu()
    def show_struggling_habits_last_month(self):
        """
        Display habits that have been struggled with over the past month.

        This method identifies and displays habits where the user has been inconsistent
        during the previous month, showing completion times for each habit.
        """
        try:
            list_struggling_habits_last_month=self.analytics.find_struggling_habits_last_month()
            if list_struggling_habits_last_month is not None:
                # Format habits and their completion counts for display
                formatted_habits = [(habit, count) for habit, count in list_struggling_habits_last_month]
                # Display the struggling habits in a tabular format
                print("The struggling habits in the last month:")
                print(tabulate(formatted_habits, headers=['Habit Name', 'Completion Times'], tablefmt='grid'))
                # Highlight the top struggled habit
                habit_name, times = list_struggling_habits_last_month[0]
                print(f"Your top struggled habit last month: {habit_name} {times} times")
            else:
                print("No habits found in the last month.")
        except Exception as e:
            print(f"An error occurred while show struggling habits last month : {e}")
        self.final_menu()
    def show_current_streak_for_habit(self):
        """
        Display the current streak for a specific habit.

        This method calculates and displays the ongoing streak (number of consecutive successful days)
        for the selected habit.
        """
        try:
            habit_name=self.select_habit_name()
            if habit_name is not None:
                tracking_records=self.analytics.list_tracking_records_of_habit(habit_name)
                if tracking_records:
                    print(f"Your Current Streak for {habit_name} is {self.analytics.get_current_streak_for_habit(habit_name)}")
                else:
                    print(f"No tracking records for {habit_name} found.")
        except Exception as e:
            print(f"An error occurred while show tracking records of  habit : {e}")
        self.final_menu()
    def show_longest_streak_for_given_habit(self):
        """
        Display the longest streak for a specific habit.

        This method calculates and shows the longest period during which a selected habit
        was consistently maintained.
        """
        try:
            habit_name=self.select_habit_name()
            if habit_name is not None:
                longest_streak_for_given_habit=self.analytics.get_longest_streak_for_given_habit(habit_name) 
                if longest_streak_for_given_habit :
                    print(f"The longest streak for {habit_name} is :",longest_streak_for_given_habit)
                else:
                    print(f"The longest streak for {habit_name} is not found.")
        except Exception as e:
            print(f"An error occurred while show longest streak for given habit : {e}")
        self.final_menu()
    def show_longest_run_streak_of_all_habits(self):
        """
        Display the longest run streak among all habits.

        This method identifies and displays the habit(s) with the longest streak among
        all habits tracked by the user.
        """
        try:
            list_longest_run_streak_of_all_habits=self.analytics.calculate_longest_run_streak_of_all_defined_habits()
            if list_longest_run_streak_of_all_habits:
                # Format the streak data for display
                formatted_habits = [(habit, longest_streak) for habit, longest_streak in list_longest_run_streak_of_all_habits]
                # Display all longest streaks in a tabular format
                print("The longest run streak of all habits:")
                print(tabulate(formatted_habits, headers=['Habit Name', 'Longest Run Streak'], tablefmt='grid'))
                
                # Identify habits with the maximum streak
                max_streak = list_longest_run_streak_of_all_habits[0][1]

                # Filter to find all habits with the max streak
                longest_streak_habits = [
                    (habit, streak) for habit, streak in list_longest_run_streak_of_all_habits if streak == max_streak
                ]
                # Display the habits with the longest streak
                print("Your longest run streak Among All Defined Habits is:")
                for habit, streak in longest_streak_habits:
                    print(f"{habit}: {streak} times")
            elif list_longest_run_streak_of_all_habits==0:
                print("Error!")
            else:
             print("No Habits Found!")
        except Exception as e:
            print(f"An error occurred while show longest streak for given habit : {e}")
        self.final_menu()
    def exit_program(self):
        """
        Exit the habit tracker program.

        This method safely exits the program, ensuring any necessary cleanup is performed.
        """
        self.clear_screen()
        print("Exiting the program...")
        exit()
    def run(self):
        """
        Run the main loop of the user interface.

        This method continuously displays the main menu and processes user input
        until the user chooses to exit the program.
        """
        while True:
            self.display_menu()

# Example usage
if __name__ == "__main__":

    ui=UserInterface()
    ui.run()

