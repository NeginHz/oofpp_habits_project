
#analytics.py
from datetime import datetime, timedelta,date
from collections import Counter
class HabitAnalyzer:
    def __init__(self, db):
        """
        Initialize a HabitAnalyzer instance.

        Args:
            db (HabitTrackerDB): An instance of the HabitTrackerDB to 
                                 perform database operations related to habits.
        """
        self.db = db
    def check_habit_exists(self, habit_name):
        """Checks if the habit already exists in the database."""
        return self.db.habit_exists(habit_name)
    def get_habits_info(self):
        """
        Retrieve all habits from the database.

        Returns:
            list: A list of tuples containing habit information, or an empty list if no habits are found.
        """
        habits = self.db.get_all_habits()
        if habits:
            return habits #is list
        else:
            return []
    def get_habit_description_and_periodicity(self, habit_name):
        """Retrieve and return the description and periodicity of a habit if found."""
        try:
            # Fetch habit metadata from the database
            habit_metadata = self.db.fetch_habit_metadata(habit_name)

            # Check if the result is None, indicating the habit was not found
            if habit_metadata is not None:
                return habit_metadata
            else:
                raise ValueError(f"Habit '{habit_name}' not found in the database.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def get_creation_date_of_habit(self,habit_name):
        """
        Retrieve the creation date of a specific habit.

        Args:
            habit_name (str): The name of the habit for which to retrieve the 
                              creation date.
        """
        creation_date=self.db.get_creation_date_of_habit(habit_name)
        return creation_date 
    def check_tracking_records_of_habit_exists(self,habit_name):
        """
        Check if tracking records exist for a specified habit.

        Args:
            habit_name (str): The name of the habit to check for tracking records.

        Returns:
            list or None: A list of tracking records if they exist, 
                          or None if no records are found.

        Raises:
            Exception: If an error occurs while accessing the database.
        """
        try:
            records=self.db.get_tracking_records_of_habit(habit_name)
            if records :
                return records
            else :
                #there isnt any record
                return None
        except Exception as e:
            print(f"An error occurred while check tracking records of habit exists : {e}")
    def remove_tracking_records_of_habit(self,habit_name):
        """
        Remove all tracking records for a specific habit.

        Args:
            habit_name (str): The name of the habit for which to remove tracking records.

        Returns:
            None: This method does not return any value.
        """
        try:
            records=self.check_tracking_records_of_habit_exists(habit_name)
            if records :
                self.db.delete_tracking_records_of_habit(habit_name)
            else :
                #there isnt any record
                return None
        except Exception as e:
            print(f"An error occurred while remove tracking records of habit : {e}")
    def list_habit_names(self):
        """
        Retrieve a list of all habit names in the database.

        Returns:
            list or None: A list of habit names if they exist, or None if no habits 
                          are found.
        """
        habits = self.db.get_all_habits_name()
        if habits:
            return habits
        else:
           
            #No habits found.
            return None
    def add_new_tracking_record(self,habit_name, completion_date):
        """
        Add a new tracking record for a specific habit.

        Args:
            habit_name (str): The name of the habit for which to add the tracking record.
            completion_date (str): The date of completion for the tracking record.

        Returns:
            None: This method does not return any value.
        """
        
        self.db.insert_tracking_record(habit_name, completion_date)
    def list_all_tracking_records(self):#list
        """
        Retrieve a list of all tracking records from the database.

        Returns:
            list: A list of all tracking records, or an empty list if no records exist.
        """
        tracking_records = self.db.get_all_tracking_records()
        return tracking_records
    def list_tracking_records_of_habit(self, habit_name): #list of tuple
        """
        Retrieve tracking records for a specific habit.

        Args:
            habit_name (str): The name of the habit for which to retrieve tracking records.

        Returns:
            list of tuple: A list of tracking records for the specified habit. Each 
                            record is represented as a tuple, or None if no records 
                            are found.
        """
        return self.db.get_tracking_records_of_habit(habit_name)
    def list_habits_by_periodicity(self,periodicity):
        """
        Retrieve a list of habits filtered by their periodicity.

        Args:
            periodicity (str): The periodicity to filter habits by (e.g., 'daily', 'weekly').

        Returns:
            list: A list of habits that match the specified periodicity. Returns an empty 
                list if no habits are found for the given periodicity.
        """
        return self.db.get_habits_by_periodicity(periodicity) 
    def count_habit_completions_last_month(self):
        """
        Counts the number of times each habit appears in the completions list for the last month.

        Returns:
        --------
        list of tuples
            A list of tuples where each tuple contains a habit name and the count of its completions.
            For example: [('dancing', 6), ('workout', 1)].

        Raises:
            Exception: If an error occurs while retrieving or processing data.
        """
        try:
            habit_completions_list_last_month=self.db.get_habit_completions_last_month()
            if habit_completions_list_last_month is not None:
                # Extract habit names from the list of completions
                habit_names = [habit_name for habit_name, _ in habit_completions_list_last_month]
                
                # Count occurrences of each habit name
                habit_counts = Counter(habit_names)
                
                # Convert the Counter object to a list of tuples
                result = [(habit, count) for habit, count in habit_counts.items()]  #[('dancing', 6), ('workout', 1)]
                return result
            else:
                return None
        except Exception as e:
            print(f"An error occurred while count habit completions last_month : {e}")
    def sort_habits_by_count(self,habit_completions_list):
        """
        Sorts a list of tuples containing habit names and their counts in descending order based on the count.

        Parameters:
        -----------
        habit_completions_list : list of tuples
            A list where each tuple contains a habit name and its count.

        Returns:
        --------
        list of tuples
            A list of tuples sorted by count in descending order.
        """
        # Sort the list of tuples based on the second element (count) in descending order
        sorted_habits = sorted(habit_completions_list, key=lambda x: x[1], reverse=True)
        
        return sorted_habits
    def find_struggling_habits_last_month(self):
        """
        Identifies habits that are struggling based on missed completions over the past month.

        Returns:
        --------
        list of tuples:
            A list of tuples containing the habit name and the number of missed completions,
            sorted by completion count.
        """
        try:
            count_habit_completions_last_month=self.count_habit_completions_last_month()
            if count_habit_completions_last_month is not None:
                return self.sort_habits_by_count(count_habit_completions_last_month)
            else:
                return None
        except Exception as e:
            print(f"An error occurred while find struggling habits last_month : {e}")
    def sort_dates_descending(self,date_list):
        """
        Sorts a list of date strings in descending order.

        Parameters:
        -----------
        date_list : list of str
            A list of date strings in 'YYYY-MM-DD' format.

        Returns:
        --------
        list of str
            The sorted list of date strings with the latest dates first.

        Raises:
            ValueError: If any date string is in an invalid format.
        """
        try:
            # Convert date strings to datetime objects for sorting
            sorted_dates = sorted(date_list, key=lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True)
            return sorted_dates
        except ValueError as e:
            print(f"Error parsing dates: {e}")
            return []
    def get_habit_periodicity_str(self, habit_name):
        """
        Retrieve the periodicity of a specified habit.

        Args:
            habit_name (str): The name of the habit for which to retrieve 
                            the periodicity.

        Returns:
            str: The periodicity of the habit (e.g., 'daily', 'weekly').

        Raises:
            Exception: If there is an error accessing the database or 
                    if the habit is not found.
        """
        return self.db.get_habit_periodicity(habit_name)
    def list_completion_dates_of_habit(self, habit_name):
        """
        Retrieves and returns a list of completion dates for a given habit.
        
        Returns:
        --------
        list of str:
            A list of completion dates (strings) in 'YYYY-MM-DD' format, if they exist, otherwise None.
        """
        try:
            list_completion_dates = self.db.get_completion_dates_of_habit(habit_name)  # list of dates
            
            # If dates are found, return the list; otherwise, return None
            if list_completion_dates:
                return list_completion_dates
            return None

        except Exception as e:  # Generic exception handling for other errors
            print(f"Unexpected error occurred: {e}")
            return 0
    def calculate_current_streak_for_daily_habit(self,list_completion_dates_of_habit_descending):
        """
        Calculate the current streak of daily completions for a habit.

        Args:
            list_completion_dates_of_habit_descending (list): A list of completion dates 
            for the habit, sorted from most recent to oldest.

        Returns:
            int: The current streak of consecutive days the habit has been completed. 
                 Returns 0 if no valid streak is found or if there is an error in parsing dates.
        """
        try:
            # Convert date strings to datetime objects
            list_completion_dates_of_habit_descending = [datetime.strptime(date, '%Y-%m-%d') for date in list_completion_dates_of_habit_descending]
            # Initialize streak variables
            current_streak = 1
            period_delta=timedelta(days=1)
            for i in range(1, len(list_completion_dates_of_habit_descending)):
                if list_completion_dates_of_habit_descending[i-1] - list_completion_dates_of_habit_descending[i] == period_delta:
                    current_streak += 1
                else:
                    break
            return current_streak   
        except ValueError as e:
            print(f"Error parsing list completion dates of habit descending: {e}")
            return 0
    def are_dates_in_consecutive_weeks(self, date1, date2):
        """
        Check if two given dates fall in consecutive weeks.

        Args:
            date1 (str or datetime.date): The first date in 'YYYY-MM-DD' format or datetime.date.
            date2 (str or datetime.date): The second date in 'YYYY-MM-DD' format or datetime.date.

        Returns:
            bool: True if the two dates fall in consecutive weeks, False otherwise.

        Raises:
            ValueError: If there is an issue while converting date strings to datetime objects.
        """
        try:
            # Convert strings to datetime.date if necessary
            if isinstance(date1, str):
                date1 = datetime.strptime(date1, "%Y-%m-%d").date()
            if isinstance(date2, str):
                date2 = datetime.strptime(date2, "%Y-%m-%d").date()

            # Ensure date1 is earlier
            if date1 > date2:
                date1, date2 = date2, date1

            # Get ISO calendar info for both dates
            year1, week1, _ = date1.isocalendar()
            year2, week2, _ = date2.isocalendar()

            # Check if weeks are consecutive within the same year
            if year1 == year2:
                return week2 - week1 == 1

            # Handle consecutive weeks across years
            if year2 - year1 == 1:  # Check if the years are consecutive
                last_week_of_year1 = date(year1, 12, 28).isocalendar()[1]
                return week1 == last_week_of_year1 and week2 == 1

            return False
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    def are_in_same_week(self,date1_str, date2_str):
        """
        Check if two given dates fall within the same week of the year.

        Args:
            date1_str (str): The first date in the format 'YYYY-MM-DD'.
            date2_str (str): The second date in the format 'YYYY-MM-DD'.

        Returns:
            bool: True if both dates are in the same week and year, False otherwise.
            None: Returns None if either date is invalid.
        """
        try:
            # Convert input strings to datetime objects
            date1 = datetime.strptime(date1_str, '%Y-%m-%d')
            date2 = datetime.strptime(date2_str, '%Y-%m-%d')
        except ValueError:
            return None  # Return None if a date is invalid
        # Get the week number and year for both dates
        week1 = date1.isocalendar()[1]  # Week number for date1
        year1 = date1.isocalendar()[0]  # Year for date1
        week2 = date2.isocalendar()[1]  # Week number for date2
        year2 = date2.isocalendar()[0]  # Year for date2

        # Check if both dates are in the same week and year
        return week1 == week2 and year1 == year2
    def calculate_current_streak_for_weekly_habit(self,list_completion_dates_of_habit_descending):
        """
        Calculate the current streak of weekly completions for a habit.

        Args:
            list_completion_dates_of_habit_descending (list): A list of completion dates for the habit, sorted in descending order.

        Returns:
            int: The current streak of weekly completions. Returns 0 if an error occurs.
        """
        try:
            
            # Initialize streak variables
            current_streak = 1
            for i in range(1, len(list_completion_dates_of_habit_descending)):
                if self.are_dates_in_consecutive_weeks(list_completion_dates_of_habit_descending[i-1],list_completion_dates_of_habit_descending[i]):
                    current_streak += 1
                    
                elif self.are_in_same_week(list_completion_dates_of_habit_descending[i-1],list_completion_dates_of_habit_descending[i]):
                    
                    continue
                else:
                    break
            return current_streak   
        except ValueError as e:
            print(f"Error parsing list completion dates of habit descending: {e}")
            return 0
    def get_current_streak_for_habit(self, habit_name):
        """
        Calculate the current streak of completions for a given habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            int: The current streak of completions for the habit. Returns 0 if no completions are recorded.
        """
        periodicity_str=self.get_habit_periodicity_str(habit_name)
        list_completion_dates_of_habit=self.list_completion_dates_of_habit(habit_name)
        list_completion_dates_of_habit_descending= self.sort_dates_descending(list_completion_dates_of_habit)

        if periodicity_str=="daily":
            return self.calculate_current_streak_for_daily_habit(list_completion_dates_of_habit_descending)
        if periodicity_str=="weekly":
            return self.calculate_current_streak_for_weekly_habit(list_completion_dates_of_habit_descending)
    def calculate_longest_streak_for_daily_habit(self,list_completion_dates_of_habit_ascending):
        """
        Calculate the longest streak of daily completions for a given habit.

        Args:
            list_completion_dates_of_habit_ascending (list): A list of completion dates for the habit, sorted in ascending order.

        Returns:
            int: The longest streak of daily completions. Returns 0 if an error occurs.
        """
        try:
            # Convert date strings to datetime objects
            list_completion_dates_of_habit_ascending = [datetime.strptime(date, '%Y-%m-%d') for date in list_completion_dates_of_habit_ascending]
            
            # Define the timedelta based on periodicity
            period_delta = timedelta(days=1)
            
            # Initialize streak variables
            current_streak = 1
            max_streak = 1
            
            # Calculate the current streak
            for i in range(1, len(list_completion_dates_of_habit_ascending)):
                if list_completion_dates_of_habit_ascending[i] - list_completion_dates_of_habit_ascending[i-1] == period_delta:
                    current_streak += 1
                else:
                    max_streak = max(max_streak, current_streak)
                    current_streak = 1  # Always reset the streak
            
            # Final comparison for the last streak
            max_streak = max(max_streak, current_streak)
            return max_streak
        except ValueError as e:
            print(f"Error parsing list completion dates of habit ascending: {e}")
            return 0
    def calculate_longest_streak_for_weekly_habit(self,list_completion_dates_of_habit_ascending):
        """
        Calculate the longest streak of weekly completions for a given habit.

        Args:
            list_completion_dates_of_habit_ascending (list): A list of completion dates for the habit, sorted in ascending order.

        Returns:
            int: The longest streak of weekly completions. 
                Returns 0 if an error occurs.

        Raises:
            ValueError: If there is an issue with parsing the list of completion dates.

        This method iterates through the list of completion dates to determine the longest 
        streak of consecutive weeks during which the habit was completed. It uses helper methods 
        `are_dates_in_consecutive_weeks` and `are_in_same_week` to determine the relationship between 
        consecutive dates.
        """
        try:
            
            # Initialize streak variables
            current_streak = 1
            max_streak=1
            for i in range(1, len(list_completion_dates_of_habit_ascending)):
                # Check if two dates are in consecutive weeks
                if self.are_dates_in_consecutive_weeks(list_completion_dates_of_habit_ascending[i],list_completion_dates_of_habit_ascending[i-1]):
                    current_streak += 1
                # If they are in the same week, continue the streak    
                elif self.are_in_same_week(list_completion_dates_of_habit_ascending[i],list_completion_dates_of_habit_ascending[i-1]):  
                    continue
                else:
                    # If no longer in consecutive weeks, update max streak and reset current streak
                    if current_streak > max_streak:
                        max_streak=current_streak
                        current_streak=1
            # Return the longest streak found
            if current_streak> max_streak:
                max_streak=current_streak  
            return max_streak   
        except ValueError as e:
            print(f"Error parsing list completion dates of habit ascending: {e}")
            return 0
    def get_longest_streak_for_given_habit(self, habit_name):    
        """
        Calculate the longest streak of completions for a given habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            int: The longest streak of completions for the habit.
                If no completions are recorded, returns 0.
                If the habit does not exist, returns None.

        Raises:
            ValueError: If there is an issue with processing the data.

        This method retrieves the periodicity of the given habit and the list of completion dates, 
        sorts the completion dates, and calculates the longest streak based on the habit's periodicity 
        (either 'daily' or 'weekly').
        """
        try:
            periodicity_str=self.get_habit_periodicity_str(habit_name)
            list_completion_dates_of_habit=self.list_completion_dates_of_habit(habit_name)
            # If there are no completion dates for the habit
            if list_completion_dates_of_habit :
                # Sort the completion dates in ascending order
                list_completion_dates_of_habit_ascending = sorted(list_completion_dates_of_habit)
                # Calculate the longest streak based on the periodicity
                if periodicity_str == "daily":
                    return self.calculate_longest_streak_for_daily_habit(list_completion_dates_of_habit_ascending)
                elif periodicity_str =="weekly":
                    return self.calculate_longest_streak_for_weekly_habit(list_completion_dates_of_habit_ascending)
            else:
                return 0 # Return 0 if there are no completion dates or the habit doesn't exist
        except ValueError as e:
            print(f"Error : {e}")
            return 0
    def sort_habits_by_max_streak(self,habit_streak_list):
        """
        Sorts a list of habits based on the maximum streak in descending order.

        Parameters:
        -----------
        habit_streak_list : list of tuples
            List of tuples where each tuple contains (habit_name, max_streak).

        Returns:
        --------
        list of tuples
            The sorted list based on max streak in descending order.
        """
        # Sort the list by the second element (max streak) in descending order
        return sorted(habit_streak_list, key=lambda x: x[1], reverse=True)
    def calculate_longest_run_streak_of_all_defined_habits(self):
        """
        Calculates the longest run streak for all defined habits.

        Returns:
        --------
        list of tuples or None:
            A list of habits and their longest streaks, sorted by the streak in descending order.
            Returns None if no habits are found or there is an error.

        This method retrieves all defined habits, calculates the longest streak for each habit,
        and returns a list sorted by the longest streak in descending order.
        """
        try:
            habits=self.list_habit_names()# Get the list of all habits
            if habits :
                # Calculate the longest run streak for each habit
                list_all_habits_long_streak = [
                (habit, self.get_longest_streak_for_given_habit(habit)) for habit in habits]
                return self.sort_habits_by_max_streak(list_all_habits_long_streak)
            else:
                return None # Return None if no habits exist
        except Exception as e:  
            print(f"Unexpected error occurred: {e}")
            return 0
    
    