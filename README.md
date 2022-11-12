# Habit Tracking Application - Python Project 

## Table of Contents
1. Purpose
2. Installation
3. Usage
4. Tests
5. Contribution

## Purpose
This application supports tracking personal habits on a regular basis and helps \
to keep an overview about habits. Also, it comes with some analysis \
of the defined habits, It is a simple solution to create, track and analyse personal habits.

This application was created due as a part of a university project (Data Science) and \
focuses on the backend processes in Python. 

##Requirements & Installation

###Requirements
- Python 3.8 or higher
- questionary module
- pytest module

###Installation
1. Install Python (at least Python 3.8) on your computer
(Find the latest version [here](https://www.python.org/downloads/)).
2. Install the module ```questionary``` by typing ```pip install questionary``` into the console.
3. Install the module ```pytest``` by entering ```pip install pytest``` into the console.


**The Program is ready to run now**

## Usage

1. Download all the documents in folder habit tracker and save in a folder on your computer.
2. Start the document ```main.py```.
3. Type in your Terminal ```python main.py```.
4. Follow the instruction on your screen.
5. When the program starts, a list of all currently created habits is displayed.
6. In the main menu, habits can be created, deleted, changed and incremented.
7. In the analysis tool, current streaks and a list of created habits can be viewed.
8. The program is not case-sensitive.
9. To check a habit, it has to be incremented in the respective time interval (daily / weekly).
10. If you forgot to submit a check, it can also be done retrospectively.


## Tests

The test module ```pytest``` is used to test the most relevant functions of the habit tracker.

Therefore, test cases can be tested typing ```pytest .``` in the Terminal.
For proofing the functionality of the application, \
the basic functionalities including the counting
of the current streak are presented in the test_project.py file.

##Contribution
This was my first Python Project. Any improvements or remarks from your side can help me. \
Feel free to help me to improve the application or reporting any detected bug. Thank you :)