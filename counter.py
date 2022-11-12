from db import add_counter, increment_counter, delete_increment, delete_counter


class Counter:

    def __init__(self, name: str, description: str, periodicity: str):
        """
        Counter class, to count events
        :param name: The name of the counter
        :param description: A short description of the counter
        :param periodicity: The periodicity of the counter
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.count = 0

    def increment(self):
        """
        Counter is incremented by +1
        """
        self.count += 1

    def reset(self):
        """
        Counter is reset to 0
        """
        self.count = 0

    def __str__(self):
        """
        Gives back a counter and the respective count

        :return: Name of the counter and the belonging current count
        """
        return f"{self.name}: {self.count}"

    def store(self, db):
        """
        Stores a new counter in the database

        :param db: An initialized sqlite3 database connection
        """
        add_counter(db, self.name, self.description, self.periodicity)

    def add_event(self, db, event_date: str = None):
        """
        Adds an event in the database

        :param db: An initialized sqlite3 database connection
        :param event_date: The current date of the increment event
        """
        increment_counter(db, self.name, event_date)


    def reset_count(self, db):
        """
        Resets the count of a respective counter to zero in the database

        :param db: An initialized sqlite3 database connection
        """
        delete_increment(db, self.name)

    def clear_counter(self, db):
        """
        Deletes the complete counter

        :param db: An initialized sqlite3 database connection
        """
        delete_counter(db, self.name)