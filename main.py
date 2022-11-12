import questionary
from db import get_db, get_all_data, check_if_exists, increment_retrospective, increment_counter
from datetime import datetime
from counter import Counter
from analyze import calculate_count, streak_count_daily, streak_count_weekly


def cli():
    """
    Starts the main program to navigate through the habit tracking application
    """
    db = get_db()

    question = questionary.confirm("Are you ready").ask()
    print("This is the main menu of the habit tracker. Here, you can create, analyse and change your habits.")
    print("Here is an overview of the predefined habits and their periodicity:")
    result = get_all_data(db)
    print("Habit, Periodicity")
    for i in sorted(set(result)):
        print(','.join(i))

    while question is False:
        print("You were not ready! Please start again")
        break

    while question is True:
        choice = questionary.select(
            "What do you want to do?",
            choices=["1. Create a new habit",
                     "2. Increment an existing habit",
                     "3. Append Increment Retrospective",
                     "4. Analyse your habits",
                     "5. Reset a habit",
                     "6. Delete a habit",
                     "7. Exit"]
            ).ask()
        if choice == "7. Exit":
            print("Bye and thank you for using the habit tracker!")
            question = False


        elif choice == "4. Analyse your habits":
            select = questionary.select("What do you want to analyse?",
                                        choices=["One existing habit",
                                                 "Return all habits",
                                                 "Return current streaks",])\
                                        .ask()
            if select == "Return all habits":
                result = get_all_data(db)
                print("List of all created habits and their periodicity")
                print("Habit, Periodicity")
                for i in sorted(set(result)):
                    print(','.join(i))

            elif select == "One existing habit":
                name = (questionary.text("What's the name of your habit?").ask()).lower()
                if check_if_exists(db, name) == True:
                    print("The Habit does not exist, please create first!")
                else:
                    count = calculate_count(db, name)
                    print(f"{name} has been incremented {count} times")

            elif select == "Return current streaks":
                print("List of all current streaks for the habits:")
                print("--------------Daily habits--------------")
                streak_count_daily(db)
                print("-----------------------------------------")
                print("--------------Weekly habits--------------")
                streak_count_weekly(db)

        elif choice == "1. Create a new habit":
            name = (questionary.text("What's the name of your habit?").ask()).lower()
            if check_if_exists(db, name) == False:
                print("The Habit already exists, please select another name!")
            else:
                desc = (questionary.text("What's the description of your habit?").ask()).lower()
                period = questionary.select("What is the periodicity of your habit?",
                                        choices=["Daily", "Weekly"]).ask()
                counter = Counter(name, desc, period)
                counter.store(db)
                print(f"{name} has been successfully created!")
                question = True


        elif choice == "2. Increment an existing habit":
            name = (questionary.text("What's the name of your habit?").ask()).lower()
            if check_if_exists(db, name) == True:
                print("The Habit does not exist, please create first!")
            else:
                counter = Counter(name, "no description", "no periodicity")
                counter.increment()
                counter.add_event(db)
                print(f"{name} has been successfully incremented!")

        elif choice == "3. Append Increment Retrospective":
            name = (questionary.text("What's the name of your habit?").ask()).lower()
            if check_if_exists(db, name) == True:
                print("The Habit does not exist, please create first!")
            else:
                counterName = name
                print("Insert in the following notion: yyyy-mm-dd")
                event_date = (questionary.text("What's the date of the increment?").ask())
                event_date_format = datetime.strptime(event_date, '%Y-%m-%d')
                if event_date_format > datetime.today():
                    print("The inserted date is in the future, please try again")
                    question = True
                else:
                    increment_retrospective(db, name, event_date)
                    increment_counter(db, name, event_date)

                    print(f"{counterName} has been successfully incremented!")


        elif choice == "5. Reset a habit":
            name = str(questionary.text("What's the name of your habit?").ask()).lower()
            if check_if_exists(db, name) == True:
                print("The Habit does not exist, please create first!")
            else:
                counter = Counter(name, "no description", "no periodicity")
                counter.reset()
                counter.reset_count(db)
                print(f"{name} has been reset to 0")

        elif choice == "6. Delete a habit":
            name = (questionary.text("What's the name of your habit?").ask()).lower()
            if check_if_exists(db, name) == True:
                print("The Habit does not exist, please create first!")
            else:
                counter = (Counter(name, "no description", "no periodicity"))
                counter.clear_counter(db)
                print(f"{name} has been deleted")

        else:
            question = True


if __name__ == '__main__':
    cli()
