__author__ = "Hanslett"
'''
utils.py

database operations here
'''
import sys
import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import qDebug


# GLOBALS

def database_exists():
	'''Checks if the database exists.'''
	cursor = QSqlQuery()
	return cursor.exec("SELECT name FROM sqlite_master WHERE type='table' AND name='congregation_database'")

def create_database(database_name):
	'''Creates and opens a database connection.'''
	connection = QSqlDatabase.addDatabase('QSQLITE')
	connection.setDatabaseName(os.path.join("./debug", database_name))

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


# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	create_database()
