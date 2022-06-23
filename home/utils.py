__author__ = "Hanslett"
'''
Utility functions for the home package
Functions here are used to handle all the database operations. Check if
the database exists. If not, create it.
'''

import sqlite3

class Utils:
    def __init__(self):
        pass

    def database_exists(self):
        return False