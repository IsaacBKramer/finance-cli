# Overview 

I'm addicted to Quicken. I hate that Quicken costs money and sort of sucks. I also know how to write (a little bit of) Python. So for those of you who are command line inclined, this tool is meant to be a free Quicken alternative.

This program uses sqlite3 to store transactions in a register. The database file is saved locally at the root of the repo. It will be created the first time you run the program if it does not already exist.

# Setup

First set up a virtual environment in the root of the repo `python3 -m venv <environment-name>`.

Active the environment with `source <environment-name>/bin/activate`.

Install the required dependencies with the virtual environment active `pip install -r requirements.txt`.

Run the program with `python3 main.py`

# Importing Transactions from CSV

Transactions can be bulk imported from csv. The csv currently expects the following format:

**`year YYYY`,`month MM`,`day DD`,`value XX.YY`,`account STRING`,`category STRING`,`TAG STRING`**

`year`, `month`, `day`, and `value` are required fields.

