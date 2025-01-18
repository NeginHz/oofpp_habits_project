# Habit Tracking App

A simple habit tracking application that allows users to monitor their daily habits, analyze progress, and gain insights through analytics.

## Introduction

Tracking habits is essential for building consistency, achieving personal goals, and encouraging positive behaviors over time. This application, built with Python 3.7+ and following object-oriented programming principles, provides a structured yet user-friendly way to manage habits. It integrates habit management, analytics, and persistent storage while ensuring a smooth command-line experience.

## Installation

### Using Virtual Environment (venv)

1. Clone the repository:
   ```bash
   git clone https://github.com/NeginHz/oofpp_habits_project.git
   cd oofpp_habits_project
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python -m src.main
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t oofpp_habits_project .
   ```
2. Run the application:
   ```bash
   docker run -it --rm oofpp_habits_project
   ```
3. Run tests inside Docker:
   ```bash
   docker run --rm oofpp_habits_project python -m pytest
   ```

## Usage

### Command Line Interface (CLI)

The application provides an interactive Command Line Interface (CLI) using `questionary`. Users can manage their habits through a menu-driven interface.

Example CLI usage:

```bash
python -m src.cli
```

Users will be presented with a menu where they can:

- Create new habits
- Modify existing habits
- Remove habits
- Add tracking records
- View analytics reports

### Analytics

The analytics module calculates key insights such as:

- Current streaks for habits
- Longest streaks
- Struggling habits
- Habit tracking trends

## Development Guide

1. Ensure you have Python 3.10+ installed.
2. Use a virtual environment (`venv`) for development.
3. Follow PEP8 coding standards.
4. Run tests before committing changes:
   ```bash
   pytest test/
   ```

## Project Structure

```
oofpp_habits_project/
│
├── src/
│   ├── __init__.py       # Package initializer
│   ├── main.py           # Entry point of the application
│   ├── cli.py            # Command-line interface for user interaction
│   ├── analytics.py      # Habit analytics and reporting
│   ├── habit.py          # Habit tracking logic
│   ├── database.py       # Database management
│   └── database.db       # SQLite database
│
├── test/
│   ├── __init__.py       # Test package initializer
│   ├── test_main.py      # Tests for main.py
│   ├── test_cli.py       # Tests for cli.py
│   ├── test_habit.py     # Tests for habit.py
│   ├── test_analytics.py # Tests for analytics.py
│   ├── test_database.py  # Tests for database.py
│   ├── conftest.py       # Pytest configuration
│
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container setup
├── README.md             # Project documentation
```

## Challenges

During development, several challenges were addressed:

- **Efficient database queries:** The SQLite schema was carefully designed to ensure fast retrieval and data consistency.
- **Accurate streak calculations:** Weekly streak tracking was implemented using the ISO calendar to ensure correctness.
- **Database structure revision:** Initially, habit IDs were used as primary keys, but this was changed to unique habit names for better usability and simplified operations.

## Achievements

- **Real-time streak tracking and analytics**
- **Clear data presentation with `tabulate`**
- **Well-structured, modular, and scalable design**
- **Thorough testing with `pytest` for reliable performance**
- **Comprehensive documentation and README for ease of use**

## Future Improvements

While the current version is strong, there are several exciting opportunities for future improvements:

- **Graphical User Interface (GUI):** Making the app more user-friendly and visually appealing.
- **Trend predictions:** Providing users with personalized insights into their habits.
- **Cloud-based storage:** Enabling cross-device accessibility.
- **Monthly habit tracking:** Offering more flexibility in tracking long-term goals.

## Technologies Used

- **Python**
- **SQLite3**
- **Tabulate**
- **Questionary**
- **Object-Oriented Design (OOP)**

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributors

- Negin Hezarjaribi - [GitHub Repository](https://github.com/NeginHz/oofpp_habits_project)
