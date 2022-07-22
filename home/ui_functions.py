from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, 
QTextBrowser, QWidget, QMessageBox)

from home.home import BaseHomeWindow
from home.html import html_home
from home.utils import *

class InterfaceTweaks(BaseHomeWindow):
	def button_checkable(self):
		self.ui.home_button.setCheckable(True)
		self.ui.congregation_button.setCheckable(True)
		self.ui.scheduler_button.setCheckable(True)
		self.ui.reports_button.setCheckable(True)
	
	def remove_widget_children(self, type=(QWidget)):
		if self.ui.clone_widget.findChildren(type):
			for widgets in self.ui.clone_widget.findChildren(type):
				widgets.deleteLater()
		special_button = self.ui.main_frame.findChild(QPushButton, "create_button")
		if special_button:
			special_button.deleteLater()

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
	
class Tweakfunctions:
	def toggle_message_box(self, header:str, message:str, window_title:str="Warning", details:str=None,):
		message_box = QMessageBox()
		message_box.setText(header)
		message_box.setInformativeText(message)
		message_box.setDetailedText(details)
		message_box.setWindowTitle(window_title)
		message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
		message_box.setDefaultButton(QMessageBox.StandardButton.Cancel)
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