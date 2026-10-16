# Development Log: Python Activity Logger

**Date:** 16 October 2026  
**Project:** Python Activity Logger  
**Technologies:** Python 3, SQLite3, Git, GitHub  
**Development Environment:** macOS, VS Code, Terminal

## 1. Project Overview

The Python Activity Logger is a command-line application designed to record time spent on activities such as coding, gym, CCNA study, university work, and guitar practice.

The application allows users to select an activity from a numbered menu, enter the duration in minutes, and optionally provide notes. The information is then stored in a local SQLite database.

The project is designed to work on both macOS and Windows without requiring external Python libraries.

### Project Requirements

- Display a numbered list of activities.
- Accept user input to select an activity.
- Reject invalid activity selections and prompt again.
- Accept only positive integer durations.
- Allow optional notes.
- Save activity records to SQLite.
- Automatically generate a unique, incrementing primary key.
- Automatically record the date and time of each entry.
- Maintain the source code through GitHub.

## 2. Repository Setup

Created a GitHub repository named `python-activity-logger` and cloned it onto the local machine.

Commands used:

```bash
git clone https://github.com/kraigjoel/python-activity-logger.git
cd python-activity-logger
code .
```

### Project Structure

```text
python-activity-logger/
├── main.py
├── database.py
├── activities.db
├── .gitignore
└── README.md
```

**main.py:** Handles the command-line interface, user input, and input validation.

**database.py:** Handles database creation and SQL operations.

**activities.db:** Stores activity records locally and is generated automatically.

**.gitignore:** Prevents unnecessary files and personal database records from being committed to Git.

**README.md:** Contains general project documentation.

### GitHub and SQLite

The SQLite database is excluded from version control using `.gitignore`.

This means cloning the repository onto another computer will download the application code but not the existing activity records. Each computer can generate its own local database.

GitHub is used for source-code version control, not live database synchronisation.

## 3. Activity Selection

A Python dictionary stores the available activities.

```python
activities = {
    1: "Coding",
    2: "CCNA",
    3: "University",
    4: "Gym",
    5: "Guitar"
}
```

### Displaying Activities

Instead of manually writing a print statement for every activity, a `for` loop iterates through the dictionary.

```python
for number, name in activities.items():
    print(f"{number}. {name}")
```

**Concepts learned:**

- Dictionaries store key-value pairs.
- `.items()` returns the dictionary's key-value pairs for iteration.
- A `for` loop can unpack each pair into two variables.
- F-strings allow variables to be inserted into formatted strings.

This approach makes the activity menu easier to maintain. Adding another dictionary entry automatically adds another menu option.

### Validating Activity Selection

```python
while True:
    selection = input("Select activity: ")

    if selection.isdigit():
        selection = int(selection)

        if selection in activities:
            break

    print("Invalid activity. Please try again.")
```

**Concepts learned:**

- `input()` always returns a string.
- `.isdigit()` checks whether the input contains digits.
- `int()` converts a valid numeric string into an integer.
- The `in` operator checks whether a key exists in the dictionary.
- `while True` repeats a block of code until it is explicitly terminated.
- `break` exits the loop when a valid selection is entered.

Invalid selections, including unavailable numbers and non-numeric input, cause the program to ask again.

## 4. Duration Validation

The duration must be a positive whole number representing minutes.

```python
while True:
    try:
        duration = int(input("Duration (minutes): "))

        if duration > 0:
            break

        print("Duration must be greater than 0.")

    except ValueError:
        print("Please enter a valid whole number.")
```

### Concepts Learned

**Exception handling:** `try` and `except` allow the application to recover from invalid input without crashing.

**ValueError:** Occurs when Python cannot convert a supplied value into the requested type, such as converting `"hello"` into an integer.

**Conditional validation:** `if duration > 0` ensures that zero and negative values are rejected.

**Input loops:** The program continues requesting input until the supplied duration satisfies the requirements.

## 5. Optional Notes

The user can enter a description or leave the notes field empty.

```python
notes = input("Notes (optional): ").strip()

if notes == "":
    notes = None
```

### Concepts Learned

- `.strip()` removes leading and trailing whitespace.
- An empty string is represented by `""`.
- `None` represents the absence of a value in Python.
- When passed to SQLite through `sqlite3`, Python's `None` is stored as SQL `NULL`.

This allows the database to distinguish between an actual description and a missing note.

## 6. SQLite Database Integration

SQLite is a lightweight relational database system that stores information in a local file.

Python includes the `sqlite3` module in its standard library.

### Database File Location

```python
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "activities.db"
```

**`__file__`:** Refers to the current Python script's file path.

**`Path()`:** Creates a path object that can be manipulated using `pathlib`.

**`.resolve()`:** Produces an absolute path and resolves symbolic links.

**`.parent`:** Returns the parent directory of the path.

**`/ "activities.db"`:** Appends the database filename to the directory path.

This ensures the database is stored alongside `database.py`, regardless of the directory from which the program is executed.

## 7. Database Schema

The `initialize_database()` function creates the table if it does not already exist.

```python
def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT NOT NULL,
                duration INTEGER NOT NULL CHECK (duration > 0),
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
```

### Table Structure

| Column | Type | Constraint |
|---|---|---|
| log_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| activity | TEXT | NOT NULL |
| duration | INTEGER | NOT NULL, CHECK > 0 |
| notes | TEXT | Nullable |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

### SQL Concepts Learned

**CREATE TABLE IF NOT EXISTS:** Creates a table only when it does not already exist.

**PRIMARY KEY:** Uniquely identifies each record.

**AUTOINCREMENT:** Ensures automatically generated row IDs increase and previously issued IDs are not reused.

**NOT NULL:** Prevents a column from containing SQL NULL.

**CHECK:** Enforces a condition at the database level.

**DEFAULT CURRENT_TIMESTAMP:** Automatically stores the insertion timestamp in UTC when no value is provided.

### Database Connections

```python
with sqlite3.connect(DB_PATH) as connection:
```

`sqlite3.connect()` opens a connection to the SQLite database.

The `with` statement provides transaction management, committing successful transactions and rolling back transactions when an exception occurs.

The connection should also be closed when database operations are finished.

## 8. Inserting Activity Records

Created a function that accepts the activity name, duration, and optional notes.

```python
def insert_activity(activity, duration, notes):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            INSERT INTO activity_logs (activity, duration, notes)
            VALUES (?, ?, ?)
        """, (activity, duration, notes))

        return cursor.lastrowid
```

### Concepts Learned

**INSERT INTO:** Adds a new row to a database table.

**SQL placeholders (`?`):** Allow values to be supplied separately from the SQL statement, preventing SQL injection and safely handling user-provided text.

**Cursor:** Provides access to information about an executed SQL operation.

**`lastrowid`:** Returns the row ID generated by the most recent successful insertion through that cursor.

The primary key and timestamp do not need to be provided manually because SQLite generates them.

## 9. Connecting the CLI to the Database

The database functions are imported into `main.py`.

```python
from database import initialize_database, insert_activity
```

The database is initialised when the application starts.

```python
initialize_database()
```

After the user provides valid activity information, the program saves it:

```python
log_id = insert_activity(
    activities[selection],
    duration,
    notes
)

print(f"Activity logged successfully! ID: {log_id}")
```

This separates user-interface logic from database operations.

## 10. Inspecting the Database

The SQLite command-line interface can be used to inspect stored records.

Open the database:

```bash
sqlite3 activities.db
```

Display tables:

```sql
.tables
```

Inspect the table schema:

```sql
.schema activity_logs
```

Display stored records:

```sql
.headers on
.mode column

SELECT * FROM activity_logs;
```

Exit:

```sql
.quit
```

### Example Records

| log_id | activity | duration | notes |
|---|---|---|---|
| 1 | Coding | 90 | Python SQLite practice |
| 2 | Gym | 60 | Bench press |
| 3 | CCNA | 45 | NULL |

These are illustrative records rather than a verified export of the local database.

## 11. Testing

The implementation includes validation for the following scenarios:

| Test | Expected Behaviour |
|---|---|
| Valid activity selection | Accepted |
| Unavailable activity number | Prompt again |
| Non-numeric activity | Prompt again |
| Positive integer duration | Accepted |
| Zero duration | Prompt again |
| Negative duration | Prompt again |
| Non-numeric duration | Prompt again |
| Empty notes | Store NULL |
| Successful insertion | Generate record ID |
| Restart application | Existing records remain stored |

These are the intended test cases. Actual test results should be recorded separately after execution.

## 12. Key Takeaways

Today's work introduced several important software development concepts:

1. **Separation of concerns:** Keeping terminal interactions and database operations in separate Python modules.
2. **Input validation:** Preventing invalid user input from reaching the database.
3. **Exception handling:** Managing runtime errors without terminating the program unexpectedly.
4. **Relational databases:** Creating structured tables with constraints and primary keys.
5. **SQL queries:** Using `CREATE TABLE`, `INSERT INTO`, and `SELECT`.
6. **Persistent storage:** Saving data that remains available after the application terminates.
7. **Version control:** Using Git and GitHub to manage source code across devices.

## 13. Next Steps

- [ ] Add a main menu with options to log an activity, view history, and exit.
- [ ] Implement a function to retrieve stored activity records.
- [ ] Display activity history in a readable terminal format.
- [ ] Add the ability to delete records by ID.
- [ ] Add summaries of total time spent on each activity.
- [ ] Clone the repository onto a Windows PC and test compatibility.
- [ ] Investigate safe database backup and synchronisation between devices.

## Conclusion

The Python Activity Logger now has the core components needed for a terminal-based activity tracking application: a numbered activity menu, input validation, optional notes, and SQLite database persistence.

The project provides practical experience with Python programming, SQL, filesystem paths, modular software design, and Git version control.

The next development stage will focus on retrieving and managing existing records through the command-line interface.