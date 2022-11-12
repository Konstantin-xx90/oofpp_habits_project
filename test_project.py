from counter import Counter
from db import get_db, add_counter, increment_counter, get_counter_data, get_tracker_data_spec, get_habits_periodicity
from analyze import calculate_count, streak_count_daily, streak_count_weekly
import os

class TestCounter:

    def setup_method(self):
        """
        Creates test cases

        :return: Increments the created habits in the test database
        """
        self.db = get_db("test_db")

        add_counter(self.db, "running", "test_description", "Daily")

        increment_counter(self.db, "running", "2022-10-08")
        increment_counter(self.db, "running", "2022-10-09")
        increment_counter(self.db, "running", "2022-10-10")
        increment_counter(self.db, "running", "2022-10-11")
        increment_counter(self.db, "running", "2022-10-12")
        increment_counter(self.db, "running", "2022-10-13")
        increment_counter(self.db, "running", "2022-10-27")
        increment_counter(self.db, "running", "2022-11-10")
        increment_counter(self.db, "running", "2022-11-11")
        increment_counter(self.db, "running", "2022-11-11")
        increment_counter(self.db, "running", "2022-11-11")
        increment_counter(self.db, "running", "2022-11-12")

        add_counter(self.db, "learning", "test_description_2", "Weekly")

        increment_counter(self.db, "learning", "2022-09-29")
        increment_counter(self.db, "learning", "2022-10-10")
        increment_counter(self.db, "learning", "2022-10-16")
        increment_counter(self.db, "learning", "2022-10-22")
        increment_counter(self.db, "learning", "2022-11-01")
        increment_counter(self.db, "learning", "2022-11-06")
        increment_counter(self.db, "learning", "2022-11-11")

    def test_counter(self):
        """
        Tests the functionality of the counter
        :return:
        """
        counter = Counter("running", "to run", "Daily")

        counter.store(self.db)

        counter.increment()
        counter.add_event(self.db)
        counter.reset()
        counter.increment()

    def test_db_counter(self):
        """
        Tests, if habits are counted corretly
        :return: Runs through, if the count equals the number of inserted increments
        """
        data = get_counter_data(self.db, "running")
        assert len(data) == 12

        count = calculate_count(self.db, "running")
        assert count == 12

        data = get_counter_data(self.db, "learning")
        assert len(data) == 7

        count = calculate_count(self.db, "learning")
        assert count == 7

    def test_streak_count_daily(self):
        """
        Tests the correct calculation of the current streak of daily habits
        :return: Runs through, if the streak equals the current streak
        """
        daily_streak = streak_count_daily(self.db)
        assert daily_streak == 2

    def test_streak_count_weekly(self):
        """
        Tests the correct calculation of the current streak of weekly habits
        :return: Runs through, if the streak equals the current streak
        """
        weekly_streak = streak_count_weekly(self.db)
        assert weekly_streak == 2

    def teardown_method(self):
        self.db.close()
        os.remove("test_db")

