from db import get_counter_data, get_tracker_data_spec, get_habits_periodicity
from datetime import date, datetime, timedelta


def calculate_count(db, name):
    """
    Calculate the count of the counter.

    :param db: An initialized sqlite3 database connection
    :param name: The name of the counter present in the DB
    :return: Length of the counter increment events
    """
    data = get_counter_data(db, name)
    return len(data)

def streak_count_daily(db):
    """
    Calculate the current and record streak of a daily habit

    :param db: An initialized sqlite3 database connection
    :return: The current, record and overall record streak for daily habits
    """
    # Returns the daily habits that were created and saves the data in a list.
    periodicity = "Daily"
    list_daily = get_habits_periodicity(db, periodicity)
    lower_periodicty = str.lower(periodicity)
    dict_overall = {}

    # Only gives back the currently created names of the habits
    # Selecting only the incremented dates of a specific habit
    for i in list_daily:
        name = (','.join(i))
        data_1 = sorted(get_tracker_data_spec(db, name))
        count = calculate_count(db, name)
        counter = 0
        streak = 0
        list_streak_habit = []
        if count == 0:
            continue
        else:
            # Analyzes the dates for the habits and calculates the current streaks for each habit.
            while counter < len(data_1)-1:
                date_0 = datetime.strptime((','.join(data_1[counter])), '%Y-%m-%d').date()
                date_1 = datetime.strptime((','.join(data_1[counter+1])), '%Y-%m-%d').date()
                date_last = datetime.strptime((','.join(data_1[len(data_1) - 1])), '%Y-%m-%d').date()

                # A habit is not checked if the habit is completed twice on the same day
                if date_0 == date_1:
                    streak += 0
                # Calculates the time difference between two habits and increments the current streak
                elif date_0 + timedelta(days=1) == date_1 and date_last >= date.today() - timedelta(days=1):
                    streak += 1
                else:
                    streak = 0
                counter += 1
                list_streak_habit.append(streak)

            print(f" {name}: Current streak of {streak} ({lower_periodicty})!")
            print(f" {name} All-time record: {max(list_streak_habit)} ({lower_periodicty})!")
            print("")

        dict_overall[name] = max(list_streak_habit)
        # returns the current streak for the test module
        return streak

        #returns the highest overall streak for each habit for the test module
        return dict_overall.get(max(dict_overall, key=dict_overall.get))
    print(f" Overall record streak: "
          f"{dict_overall.get(max(dict_overall, key=dict_overall.get, default=0))} for "
          f"{max(dict_overall, key=dict_overall.get, default=0)}! ({lower_periodicty})!")

def streak_count_weekly(db):
    """
    Calculate the current and record streak of a weekly habit

    :param db: An initialized sqlite3 database connection
    :return: The current, record and overall record streak for weekly habits
    """
    list_streak_overall = []
    # Returns the daily habits that were created and saves the data in a list.
    periodicity = "Weekly"
    list_weekly = get_habits_periodicity(db, periodicity)
    lower_periodicty = str.lower(periodicity)
    dict_overall = {}

    # Only gives back the currently created names of the habits
    # Selecting only the incremented dates of a specific habit
    for i in list_weekly:
        name = (','.join(i))
        data_1 = sorted(get_tracker_data_spec(db, name))
        count = calculate_count(db, name)
        counter = 0
        streak = 0
        list_streak_habit = []
        if count == 0:
            continue
        else:
            # Analyzes the dates for the habits and calculates the current streaks for each habit.
            while counter < len(data_1)-1:
                date_0 = datetime.strptime((','.join(data_1[counter])), '%Y-%m-%d').date()
                date_1 = datetime.strptime((','.join(data_1[counter+1])), '%Y-%m-%d').date()
                date_last = datetime.strptime((','.join(data_1[len(data_1) - 1])), '%Y-%m-%d').date()

                # A habit is not checked if the habit is completed twice on the same day
                if date_0 == date_1:
                    streak += 0
                # Calculates the time difference between two habits and increments the current streak
                elif date_1 - date_0 <= timedelta(days=7):
                    streak += 1
                elif date_0 + timedelta(days=7) == date_1 and date_last >= date.today() - timedelta(days=7):
                    streak += 1
                else:
                    streak = 0
                counter += 1
            else:
                # Only completed weeks are counted as succeeded streaks
                if date.today() - (datetime.strptime((','.join(data_1[0])), '%Y-%m-%d').date()) <= timedelta(days=7):
                    streak += 0
                else:
                    overall_weeks = ((date.today() - datetime.strptime(
                        (','.join(data_1[0])), '%Y-%m-%d').date())/7).days
                    if overall_weeks < streak:
                        streak = overall_weeks
                    else:
                        streak += 0
                list_streak_habit.append(streak)
                list_streak_overall.append(streak)
            max_habit_streak = max(list_streak_habit)

            print(f" {name}: Current streak of {streak} ({lower_periodicty})!")
            print(f" {name} All-time record: {max_habit_streak} ({lower_periodicty})!")
            print("")
        dict_overall[name] = max(list_streak_habit, default=0)
        # returns the current streak for the test module
        return streak

        # returns the highest overall streak for each habit for the test module
        return dict_overall.get(max(dict_overall, key=dict_overall.get))
    print(f" Overall record streak: "
          f"{dict_overall.get(max(dict_overall, key=dict_overall.get, default=0))} for "
          f"{max(dict_overall, key=dict_overall.get, default=0)}! ({lower_periodicty})!")