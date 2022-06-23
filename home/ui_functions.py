from PyQt6.QtWidgets import (QMainWindow, QSizePolicy, QPushButton, QVBoxLayout, 
QLabel, QTextBrowser, QWidget, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QSize
# from PyQt6.QtGui import 

# local imports (lol)
from home.home import BaseHomeWindow
from home.html import html_home
from home.css import congregation_view_css
from home.utils import Utils

class InterfaceTweaks(BaseHomeWindow):
	# Global Variable here
	def button_checkable(self):
		self.ui.home_button.setCheckable(True)
		self.ui.congregation_button.setCheckable(True)
		self.ui.scheduler_button.setCheckable(True)
		self.ui.reports_button.setCheckable(True)
	
	def remove_widget_children(self, type=(QWidget)):
		if self.ui.clone_widget.findChildren(type):
			for widgets in self.ui.clone_widget.findChildren(type):
				widgets.deleteLater()

	def set_clone_widget_type(self):
		if not self.ui.clone_widget.layout():
			self.ui.clone_widget.setLayout(QVBoxLayout())
	
	def toggle_title(self, text:str="V1.0.0"):
		self.setWindowTitle(f"NWB SCHEDULER - {text}")

	def home_view(self):
		# Set title and remove previous children elements
		self.ui_tweaks.toggle_title(self, self.ui.home_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)
		self.ui.home_button.setStyleSheet("background-color: #006699;")

		# set main header to the center of the screen
		main_text = QTextBrowser()
		main_text.setText(html_home)
		self.ui.clone_widget.layout().addWidget(main_text)

	def congregation_view(self):
		# Set title and remove previous children elements and miscellaneous tweaks
		self.ui_tweaks.toggle_title(self, self.ui.congregation_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		# add two buttons to the view
		bframe = QFrame(self.ui.clone_widget)
		bframe.setFrameShape(QFrame.Shape.StyledPanel)
		bframe.setFrameShadow(QFrame.Shadow.Raised)
		bframe.setLayout(QVBoxLayout())
		bframe.setStyleSheet(congregation_view_css)
		bframe.setMaximumHeight(200)

		cong_button_1 = QPushButton("New Congregation Database")
		cong_button_1.setObjectName("cong_button_1")
		cong_button_1.setMaximumHeight(50)
		cong_button_2 = QPushButton("Test Congregation Database")
		cong_button_2.setObjectName("cong_button_2")
		cong_button_2.setMaximumHeight(50)
		cong_button_1.clicked.connect(self.ui_tweaks.real_database)
		cong_button_2.clicked.connect(self.ui_tweaks.fake_database)

		# add to layout
		bframe.layout().addWidget(cong_button_1)
		bframe.layout().addWidget(cong_button_2)
		self.ui.clone_widget.layout().addWidget(bframe)

	def scheduler_view(self):
		# set title and remove prevous children elements
		self.ui_tweaks.toggle_title(self, self.ui.home_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		# check if user has a congregation or test database
		if self.utils.database_exists():
			pass
		else:
			reply = QMessageBox.critical(None, "No Database Found!","You need to create a congregation database to proceed", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
			return (self.ui_tweaks.congregation_view(self), self.ui.congregation_button.setStyleSheet("background-color: #006699;"))

	def reports_view(self):
		self.ui_tweaks.toggle_title(self, self.ui.home_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		# check if user has a congregation or test database
		if self.utils.database_exists():
			pass
		else:
			reply = QMessageBox.critical(None, "No Database Found!","You need to create a congregation database to proceed", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
			return (self.ui_tweaks.congregation_view(self), self.ui.congregation_button.setStyleSheet("background-color: #006699;"))
	
	def fake_database(self):
		print("Button clicked")
		header = "Do you want to proceed with a test database?"
		message = "his is not a real congregation database."
		detail = "This is just for testing purposes! You can change to a real congregation database later."
		window_title = "Beta Congregation Database"

		reply = Tweakfunctions.toggle_message_box(self, header, message, window_title, detail)

		if reply == QMessageBox.StandardButton.Yes:
			pass
			# self.create_test_database()
		else:
			pass
	
	def real_database(self):
		print("Button clicked")
		header = "Do you want to proceed with a real database?"
		message = "This is a real congregation database."
		detail = "This is the real database that will be used for the scheduler. You can't own more than one congregation database."
		window_title = "Congregation Database"
		reply = Tweakfunctions.toggle_message_box(self, header, message, window_title, detail)

		if reply == QMessageBox.StandardButton.Yes:
			pass
			# self.create_real_database()
		else:
			pass

class Tweakfunctions:
	def toggle_message_box(self, header:str, message:str, window_title:str="Warning", details:str=None,):
		message_box = QMessageBox()
		message_box.setText(header)
		message_box.setInformativeText(message)
		message_box.setDetailedText(details)
		message_box.setWindowTitle(window_title)
		message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
		message_box.setDefaultButton(QMessageBox.StandardButton.Cancel)
		# message_box.setIcon(QMessageBox.StandardButton.Warning)
		reply = message_box.exec()
		return reply
	
	def check_ischecked(self, widget:QWidget):
		all_buttons = widget.findChildren(QPushButton)
		for button in all_buttons:
			if button.isChecked():
				button.setStyleSheet("background-color: #006699;")
				button.setCheckable(False)
			else:
				button.setStyleSheet("background-color: transparent;")
				button.setCheckable(True)