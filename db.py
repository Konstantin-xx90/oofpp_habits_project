import sqlite3
from datetime import date


def get_db(name="main.db"):
    """
    Initializes the sqlite3 database connection
    :param name: The name of the database
    :return: Builds a database in sqlite3 and connects to the database
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    """
    Creates the required tables in the database
    :param db: An initialized sqlite3 database connection
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS counter (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        counterName TEXT,
        FOREIGN KEY (counterName) REFERENCES counter(name))""")

    db.commit()


def add_counter(db, name, description, periodicity):
    """
    Adds new counters to existing counters in the database
    :param db: An initialized sqlite3 database connection
    :param name: The name of the existing counter
    :param description: A short description of the counter
    :param periodicity: The periodicity of the counter
    """
    cur = db.cursor()
    cur.execute("INSERT OR REPLACE INTO counter VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()

def increment_retrospective(db, name, date):
    """
    Increments retrospectively an existing counter in the database
    :param db: An initialized sqlite3 database connection
    :param name: The name of the existing counter
    """
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (name, date))
    db.commit()


def increment_counter(db, name, event_date=None):
    """
    Increments a existing counter by one
    :param db: An initialized sqlite3 database connection
    :param name: The name of the existing counter
    :param event_date: The date of the increment
    """
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()


def delete_increment(db, name):
    """
    Resets the count of a current counter
    :param db: An initialized sqlite3 database connection
    :param name: The name of the counter
    """
    cur = db.cursor()
    cur.execute("DELETE FROM tracker WHERE counterName=?", (name,))
    db.commit()


def get_counter_data(db, name):
    """
    Select Statement to retrieve tracked counts for an existing counter
    :param db: An initialized sqlite3 database connection
    :param name: The name of the existing counter
    :return: The number of counts belonging to an existing counter
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM counter")
    cur.execute("SELECT * FROM tracker")
    cur.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()

def get_tracker_data(db):
    """
    Returns all habits and their respective increments
    :param db: An initialized sqlite3 database connection
    :return: A list of all tracking entries of all counters
    """
    cur = db.cursor()
    cur.execute("SELECT name, date FROM counter INNER JOIN tracker ON tracker.counterName = counter.name")
    return cur.fetchall()


def get_tracker_data_spec(db, name):
    """
    Returns one concrete habit and it's respective increments
    :param db: An initialized sqlite3 database connection
    :param name: The name of the existing counter
    :return: The name of the counter and it's specific count.
    """
    cur = db.cursor()
    cur.execute("SELECT date FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()


def get_all_data(db):
    """
    Select Statement to retrieve all current counters in the counter table
    :param db: An initialized sqlite3 database connection
    :return: A list of all counters in the database
    """
    cur = db.cursor()
    cur.execute("SELECT name, periodicity FROM counter")
    return cur.fetchall()


def delete_counter(db, name):
    """
    Delete Statement to delete all data for a named counter
    :param db: An initialized sqlite3 database connection
    :param name: The name of the counter
    """
    cur = db.cursor()
    cur.execute("DELETE FROM counter WHERE name=?", (name,))
    cur.execute("DELETE FROM tracker WHERE counterName=?", (name,))
    db.commit()


def check_if_exists(db, name):
    """

    Checks if a certain counter is already in the database
    :param db: An initialized sqlite3 database connection
    :param name: The name of the counter
    :return: True, if the counter already exists in the database
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM counter WHERE name=?", (name,))
    result_exists = cur.fetchall()
    #Check if the list is empty (True = Empty)
    if not result_exists:
        return True
    else:
        return False


def get_habits_periodicity(db, periodicity):
    """
    Returns the periodicity of a certain habit
    :param db: An initialized sqlite3 database connection
    :param periodicity: The periodicity of the counter
    :return: The periodicity of a given habit
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM counter WHERE periodicity=?", (periodicity,))
    return cur.fetchall()