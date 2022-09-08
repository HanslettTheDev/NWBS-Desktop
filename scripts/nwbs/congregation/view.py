from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QLabel, 
QFrame, QMessageBox, QDialog, QDialogButtonBox, 
QHBoxLayout, QLineEdit, QTableView, QAbstractItemView, QComboBox, 
QFormLayout, QHeaderView)

from scripts.nwbs.home import BaseHomeWindow
from scripts.nwbs.ui_functions import Tweakfunctions
from scripts.nwbs.utils import *
from scripts.nwbs import css

import logging
import random
from datetime import datetime

log_code = random.randint(10000, 99999)

# create a variable to show current date and time in the log file

now = datetime.now()
t = now.strftime("%Y-%m-%d")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(funcName)s: %(levelname)s: %(message)s')

file_handler = logging.FileHandler(f'logs/congregation/log_{t}_{log_code}.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Congregation(BaseHomeWindow):
	def congregation_view(self):
		# Set title and remove previous children elements and miscellaneous tweaks
		self.ui_tweaks.toggle_title(self, self.ui.congregation_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		if database_exists():
			self.congregation._after_congregation_check(self)
			return 
		
		# add two buttons to the view
		bframe = QFrame(self.ui.clone_widget)
		bframe.setFrameShape(QFrame.Shape.StyledPanel)
		bframe.setFrameShadow(QFrame.Shadow.Raised)
		bframe.setLayout(QVBoxLayout())
		bframe.setStyleSheet(css.congregation_view_css)
		bframe.setMaximumHeight(200)

		cong_button_1 = QPushButton("New Congregation Database")
		cong_button_1.setObjectName("cong_button_1")
		cong_button_1.setMaximumHeight(50)
		cong_button_2 = QPushButton("Test Congregation Database")
		cong_button_2.setObjectName("cong_button_2")
		cong_button_2.setMaximumHeight(50)
		try:
			cong_button_1.clicked.connect(lambda: self.congregation.real_database(self))
			cong_button_2.clicked.connect(lambda: self.congregation.fake_database(self))
		except Exception as e:
			logger.exception("Application crashed. Here is the traceback:", exc_info=True)
			sys.exit(1)
		
		# add to layout
		bframe.layout().addWidget(cong_button_1)
		bframe.layout().addWidget(cong_button_2)
		self.ui.clone_widget.layout().addWidget(bframe)
	
	def real_database(self):
		self.congregation._after_home_view_load(self)

	def fake_database(self):
		QMessageBox.information(None, "Notification", "These feature is disabled for the moment")
		# header = "Do you want to proceed with a test database?"
		# message = "This is not a real congregation database."
		# detail = "This is just for testing purposes! You can change to a real congregation database later."
		# window_title = "Beta Congregation Database"

		# reply = Tweakfunctions.toggle_message_box(self, header, message, window_title, detail)

		# if reply == QMessageBox.StandardButton.Yes:
		# 	pass
		# 	# create_database
		# else:
		# 	pass
	
	# List of functions that work after database is created and still under the InterfaceTweaks scope
	def _after_home_view_load(self):
		# create a small input to receive data
		dialog = QDialog(self)
		dialog_buttons = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
		buttons = QDialogButtonBox(dialog_buttons)
		buttons.accepted.connect(dialog.accept)
		buttons.rejected.connect(dialog.reject)
		
		hlayout = QVBoxLayout()
		input_ = QLineEdit()
		input_.setObjectName("cong_name_input")
		input_.setMinimumSize(300,30)
		input_.setStyleSheet("font-size: 15px")

		
		hlayout.addWidget(input_)
		hlayout.addWidget(buttons)
		dialog.setLayout(hlayout)
		dialog.setWindowTitle("Enter your Congregation Name")
		reply = dialog.exec()
		
		if reply and input_.text() != "":
			# remove elements since is the users first time
			self.ui_tweaks.remove_widget_children(self)
			save_name = save_congname(input_.text())
			if not save_name:
				return QMessageBox.warning(None, "Unexpected Error", "Something went wrong!")
			self.congregation._after_congregation_check(self)
		else:
			QMessageBox.information(None, "Notification", "You need to enter a congregation name to proceed")
			return self.congregation._after_home_view_load(self)
	
	def _after_congregation_check(self):
		'''After congregation checks are done, display data'''
		self.table  = QTableView()
		self.table.setObjectName("cong_table")
		self.table.setModel(self.table_model.model)
		self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) #selects only rows
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) #resizes columns to fit content
		self.table.setStyleSheet("font-size: 15px;")
		self.ui.clone_widget.layout().addWidget(self.table)
		self.table.hideColumn(0)

		add_button = QPushButton("Add Publisher")
		add_button.setObjectName("add_publisher_button")
		add_button.setMinimumHeight(55)
		add_button.setStyleSheet("background-color: white;")
		add_button.clicked.connect(lambda: self.congregation.add_publisher(self))
		self.ui.clone_widget.layout().addWidget(add_button)


		delete_button = QPushButton("Delete Publisher")
		delete_button.setObjectName("delete_publisher_button")
		delete_button.clicked.connect(lambda: self.congregation.delete_publisher(self))
		delete_button.setMinimumHeight(55)
		delete_button.setStyleSheet("background-color: white;")
		self.ui.clone_widget.layout().addWidget(delete_button)

		label = QLabel("Edit any publisher record by double clicking on it. When done, hit enter to save")
		label.setObjectName("publisher_label")
		label.setStyleSheet("color: #006699; font-size: 15px;")
		self.ui.clone_widget.layout().addWidget(label)

		frame = QFrame()
		frame.setObjectName("button_frame")
		frame.setFrameShape(QFrame.Shape.StyledPanel)
		frame.setFrameShadow(QFrame.Shadow.Raised)
		frame.setStyleSheet(css.button_frame)

		layout = QHBoxLayout()
		layout.setSpacing(25)
		frame.setLayout(layout)
		frame.layout().addWidget(add_button)
		frame.layout().addWidget(delete_button)
		self.ui.clone_widget.layout().addWidget(frame)
	
	def add_publisher(self):
		dialog  = addDialog(self)
		# print(dialog.accepted) 
		if dialog.exec():
			self.table_model.add_publisher(dialog.data)
			self.table.resizeColumnsToContents()
			print(self.table_model.model.lastError().text())
	
	def delete_publisher(self):
		row = self.table.currentIndex().row()

		if row < 0:
			return QMessageBox.information(self, "Notification", "You need to select a publisher to delete!")
		
		reply = QMessageBox.warning(self,"Warning!", "Do you want to remove the selected Publisher?", 
		QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

		if reply == QMessageBox.StandardButton.Yes:
			self.table_model.delete_publisher(row)
			print(self.table_model.model.lastError().text())


class addDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Add Publisher")
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.setup_ui()
	
	def setup_ui(self):
		'''Setup the add publishers'''
		self.fname_input = QLineEdit()
		self.fname_input.setObjectName("name_input")
		self.fname_input.setMinimumSize(300, 30)
		self.mname_input = QLineEdit()
		self.mname_input.setObjectName("mname_input")
		self.mname_input.setMinimumSize(300, 30)
		self.lname_input = QLineEdit()
		self.lname_input.setObjectName("lname_input")
		self.lname_input.setMinimumSize(300, 30)
		self.role = QComboBox()
		self.role.setObjectName("role_input")
		self.role.setMinimumSize(300, 30)
		self.role.addItems(["Publisher","Ministerial Servant", "Elder"])

		layout = QFormLayout()
		layout.addRow("First Name", self.fname_input)
		layout.addRow("Middle Name (Optional)", self.mname_input)
		layout.addRow("Last Name", self.lname_input)
		layout.addRow("Role", self.role)

		self.layout.addLayout(layout)
		self.button_box = QDialogButtonBox(self)
		self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		self.layout.addWidget(self.button_box)
	
	def accept(self):
		'''Accept data and cary validations'''
		self.data = []
		for publisher in (self.fname_input, self.mname_input, self.lname_input):
			if not publisher.text():
				if publisher.objectName() == "mname_input":
					self.data.append(publisher.text())
					continue
				QMessageBox.critical(self, "Notification", f"You need to enter {publisher.objectName()} field")
				self.data = None # reset data
				return
			self.data.append(publisher.text())

		if not self.role.currentText():
			QMessageBox.critical(self, "Notification", "You need to select a role")
			self.data = None
		
		self.data.append(self.role.currentText())

		if not self.data:
			return

		super().accept()