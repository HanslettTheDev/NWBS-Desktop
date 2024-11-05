__author__ = "Hanslett"
'''
utils.py

database operations here
'''

import calendar
import json
import sys
import os
import nwbs.config as config
from datetime import date
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import qDebug


# GLOBALS

months = {
	'January': 1,
	'February': 2,
	'March': 3,
	'April': 4,
	'May': 5,
	'June': 6,
	'July': 7,
	'August': 8,
	'September': 9,
	'October': 10,
	'November': 11,
	'December': 12
}

def database_exists():
	'''Checks if the database exists.'''
	insert_cursor = QSqlQuery("SELECT congregation_name FROM congregation_database")
	if insert_cursor.isSelect() and insert_cursor.isActive():
		if not insert_cursor.seek(0):
			return False
	return True

def create_database(database_name):
	'''Creates and opens a database connection.'''
	connection = QSqlDatabase.addDatabase('QSQLITE')
	connection.setDatabaseName(os.path.join(config.FOLDER_REFERENCES["database"], database_name))

	if not connection.open():
		QMessageBox.critical(
			None, 
			"Database Error", 
			f"Unable to open database: {connection.lastError().text()}", 
		)
		return False

	_congregation_publishers_table()
	_congregation_database_table()
	return True

def _congregation_database_table():
	create_table_query = QSqlQuery()
	return create_table_query.exec('''
		CREATE TABLE IF NOT EXISTS congregation_database (
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
			congregation_name varchar(50) NOT NULL
		)''')

def _congregation_publishers_table():
	create_table_query = QSqlQuery()
	return create_table_query.exec('''
		CREATE TABLE IF NOT EXISTS congregation_publishers (
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
			first_name varchar(50) NOT NULL,
			middle_name varchar(50),
			last_name varchar(50) NOT NULL,
			role varchar(50) NOT NULL DEFAULT 'Publisher'
			)
		''')

def save_congname(congregation_name:str):
	insert_cursor = QSqlQuery()
	insert_cursor.prepare("INSERT INTO congregation_database (congregation_name) VALUES (:congregation_name)")
	insert_cursor.bindValue(":congregation_name", congregation_name)
	return insert_cursor.exec()

def show_records():
	pass

# def get_range(month:str, end_month:str):
# 	month_dict = {name: num for num, name in enumerate(calendar.month_name) if num}
#     month_int = month_dict[month]

# get_range("May", "June")
# create_months()
# check()