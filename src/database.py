import sqlite3
from datetime import datetime, timedelta
import os

class HabitTrackerDB:
    def __init__(self, connection=None, db_name='habit_tracker.db'):
        """
        Initializes the HabitTrackerDB class.

        Args:
            connection (sqlite3.Connection, optional): A pre-existing connection to the database. 
                If not provided, a new connection is created.
            db_name (str, optional): The SQLite database file name. Defaults to 'habit_tracker.db'.

        Behavior:
            If no `connection` is provided, a new SQLite connection is created.
            The `_initialize_db()` method is called to set up tables if they don't already exist.
        """
        self.db_name = db_name
        self.db_path = self._get_db_path(db_name)
        self.connection = connection if connection else sqlite3.connect(self.db_path)
        self._initialize_db()

    def _get_db_path(self, db_name):
        """
        Returns the full path to the database file inside the `habit_tracker` package.

        Args:
            db_name (str): The database file name.

        Returns:
            str: The full path to the SQLite database file.
        """
        # Get the path to the `src` package directory
        package_dir = os.path.dirname(os.path.abspath(__file__))
        # Set the database path to be inside the `src` package
        return os.path.join(package_dir, db_name)
    def close(self):
        """
        Closes the connection to the database.

        Behavior:
            Ensures the database connection is safely closed. If any error occurs, 
            it logs the exception.
        """
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")
    def _initialize_db(self):
        """
        Initializes the database schema.

        Behavior:
            Creates the necessary tables (`habit` and `habit_completions`) 
            if they do not already exist.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()

                # Create the 'habit' table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit (
                        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT NOT NULL,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT NOT NULL,
                        creation_time TEXT NOT NULL 
                    )
                """)

                # Create the 'habit_completions' table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS habit_completions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT NOT NULL,
                        completion_date TEXT NOT NULL,
                        FOREIGN KEY(habit_name) REFERENCES habit(name),
                        UNIQUE (habit_name, completion_date)      
                    )
                """)
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
    def _execute_query(self, query, parameters=None):
        """
        Executes a SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (tuple, optional): Parameters to bind to the query. Defaults to None.

        Returns:
            list: Query results, if any, or an empty list if no results.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
    def insert_habit(self, habit):
        """
        Inserts a new habit into the database.

        Args:
            habit (object): An instance of the habit containing the necessary details.

        Query:
            INSERT INTO habit (name, description, periodicity, creation_date, creation_time)
            VALUES (?, ?, ?, ?, ?)
        """
        query = """
            INSERT INTO habit (name, description, periodicity, creation_date,creation_time)
            VALUES (?, ?, ?, ?, ?)
        """
        # Ensure creation_date and creation_time are strings
        creation_date = str(habit.creation_date)
        creation_time = str(habit.creation_time)
        self._execute_query(query, (habit.name, habit.description, habit.periodicity, creation_date,creation_time))
    def insert_tracking_record(self, habit_name, completion_date):
        """
        Inserts a new tracking record into the database.

        Args:
            habit_name (str): The name of the habit.
            completion_date (str): The date the habit was completed (format: YYYY-MM-DD).

        Query:
            INSERT INTO habit_completions (habit_name, completion_date)
            VALUES (?, ?)
        """
        
        query = """
            INSERT INTO habit_completions (habit_name, completion_date)
            VALUES (?, ?)
        """
        self._execute_query(query, (habit_name, completion_date))
    def habit_exists(self, habit_name):
        """
        Checks if a habit exists in the database.

        Args:
            habit_name (str): The name of the habit to check.

        Returns:
            bool: True if the habit exists, False otherwise.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM habit WHERE name = ?", (habit_name,))
                count = cursor.fetchone()[0]
                return count > 0  # Return True if count > 0, else False 
            
        except sqlite3.Error as e:
            print(f"Error checking if habit exists: {e}")
            return False
    def fetch_habit_metadata(self, habit_name):
        """
        Fetches metadata (description and periodicity) of a habit.

        Args:
            habit_name (str): The name of the habit to fetch metadata for.

        Returns:
            tuple or None: A tuple (description, periodicity) if the habit exists,
                           otherwise None.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT description, periodicity FROM habit WHERE name = ?", (habit_name,))
                result = cursor.fetchone()

                if result is None:
                    print(f"Habit '{habit_name}' not found!")
                    return None
                else:
                    # Return the tuple (description, periodicity) directly
                    return result
        except sqlite3.Error as e:
            print(f"Error fetching habit metadata: {e}")
            return None
    def get_all_habits(self):
        """
        Retrieves all habits from the database.

        Returns:
            list: A list of tuples containing all habit records.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM habit")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving all habits: {e}")
            return []
    def get_all_habits_name(self):
        """
        Retrieves the names of all habits.

        Returns:
            list: A list of habit names (strings).
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT name FROM habit")
                habits = cursor.fetchall()  # Fetch all habit names
                return [habit[0] for habit in habits]  # Extract habit names from tuples
        except sqlite3.Error as e:
            print(f"Error retrieving all habits: {e}")
            return []
    def update_habit(self, habit):
        """
        Updates the details of an existing habit in the database.

        Args:
            habit (object): An instance of the habit containing updated details.

        Query:
            UPDATE habit SET description = ?, periodicity = ? WHERE name = ?
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE habit
                    SET description = ?, periodicity = ?
                    WHERE name = ? 
                """, ( habit.description, habit.periodicity, habit.name))
        except sqlite3.Error as e:
            print(f"Error updating habit: {e}")
    def delete_habit(self, habit_name):
        """
        Deletes a habit from the database by its name.

        Args:
            habit_name (str): The name of the habit to delete.

        Behavior:
            Deletes the habit from the `habit` table where the name matches.

        Exceptions:
            Prints an error message if a database error occurs.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM habit WHERE name = ?", (habit_name,))
        except sqlite3.Error as e:
            print(f"Error deleting habit: {e}")
    def insert_tracking_record(self, habit_name, completion_date):
        """
        Inserts a tracking record for a habit.

        Args:
            habit_name (str): The name of the habit.
            completion_date (str): The date of the completion (format: YYYY-MM-DD).

        Query:
            INSERT INTO habit_completions (habit_name, completion_date)
        """
        query = """
            INSERT INTO habit_completions (habit_name, completion_date)
            VALUES (?, ?)
        """
        completion_date = str(completion_date)
        self._execute_query(query, (habit_name, completion_date))
    def get_all_tracking_records(self):
        """
        Retrieves all tracking records from the database.

        Returns:
            list: A list of all tracking records as tuples (habit_name, completion_date).
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM habit_completions")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving all tracking records: {e}")
            return []
    def get_creation_date_of_habit(self,habit_name):
        """
        Fetches the creation date of a habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            str or None: The creation date as a string if the habit is found; otherwise, None.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT creation_date FROM habit WHERE name = ?", (habit_name,))
                result = cursor.fetchone()
                if result:
                    creation_date = result[0]  # Extract creation_date from the tuple
                    return creation_date 
                else:
                    print("Habit not found.")
                    return None  # Return None if habit is not found
        except sqlite3.Error as e:
            print(f"Error retrieving all habits: {e}")
            return None
    def get_habit_periodicity(self, habit_name):
        """
        Fetches the periodicity of a habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            str or None: The periodicity if found; otherwise, None.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT periodicity FROM habit WHERE name = ?", (habit_name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the periodicity 
            else:
                print(f"Habit '{habit_name}' not found!")
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving habit periodicity: {e}")
            return None
    def get_completion_dates_of_habit(self, habit_name):
        """
        Fetches the completion dates of a habit by its name.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            list or None: A list of completion dates (strings) if found; otherwise, None.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT completion_date FROM habit_completions WHERE habit_name = ?", (habit_name,))
                result = cursor.fetchall()

                if result:  # Check if there are any completion dates
                    return [row[0] for row in result]  # Return list of completion dates as strings
                else:
                    return None  # Return None if no completion dates are found

        except sqlite3.Error as e:
            print(f"Error retrieving completion dates for habit '{habit_name}': {e}")
            return None  # Return None in case of a database error
    def get_tracking_records_of_habit(self,habit_name):
        """
        Fetches all tracking records of a habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            list: A list of tuples containing tracking records.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM habit_completions WHERE habit_name = ?", (habit_name,))
                records=cursor.fetchall() #ist of tuples
                if records:
                    return records
                else:
                    return []
        except sqlite3.Error as e:
            print(f"Error retrieving tracking records: {e}")
            return []
    def delete_tracking_records_of_habit(self, habit_name):
        """
        Deletes all tracking records for a specific habit.

        Args:
            habit_name (str): The name of the habit whose tracking records are to be deleted.

        Returns:
            None if no records exist; otherwise, the records are deleted.
        """
    
        try:
            with self.connection:
                cursor = self.connection.cursor()
                 # Check if there are tracking records for the habit
                records = self.get_tracking_records_of_habit(habit_name)
                if records:
                    cursor.execute("DELETE FROM habit_completions WHERE habit_name = ?", (habit_name,))    
                else:
                    return None
        except sqlite3.Error as e:
            print(f"Error deleting habit tracking records: {e}")
    def get_habits_by_periodicity(self, periodicity):
        """
        Fetches all habits with a specific periodicity.

        Args:
            periodicity (str): The periodicity to filter habits by (e.g., "daily", "weekly").

        Returns:
            list: A list of tuples representing habits with the given periodicity.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM habit WHERE periodicity = ?", (periodicity,))
                return cursor.fetchall()  # Example: [(1, 'dancing', 'party', 'daily', '2024-01-01'), ...]
        except sqlite3.Error as e:
            print(f"Error retrieving habits by periodicity: {e}")
            return []
    def get_habit_completions_last_month(self):
        """
        Fetches all habit completions from the previous calendar month.

        Returns:
            list: A list of tuples (habit_name, completion_date) for completions in the last month,
                  or None if no completions are found.
        """
        try:
            # Get the current date
            today = datetime.today().date()

            # Get the first day of the current month
            first_day_of_current_month = today.replace(day=1)

            # Get the last day of the previous month
            last_day_of_last_month = first_day_of_current_month - timedelta(days=1)

            # Get the first day of the previous month
            first_day_of_last_month = last_day_of_last_month.replace(day=1)
            # Fetch completions within the date range
            completions= self._execute_query("""
                SELECT habit_name, completion_date 
                FROM habit_completions 
                WHERE completion_date BETWEEN ? AND ?
            """, (first_day_of_last_month.isoformat(), last_day_of_last_month.isoformat()))
            if not completions:
                #No habit completions found for the last month.
                return None
            return completions
        except sqlite3.Error as e:
            print(f"Error retrieving habit completions: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
