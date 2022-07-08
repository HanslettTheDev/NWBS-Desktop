import asyncio
from tkinter import Frame
import aiohttp
from ssl import SSLError
from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout,
QComboBox, QLabel, QFormLayout, QDialogButtonBox, 
QHBoxLayout, QTextBrowser, QScrollArea, QPushButton, QFrame, QLineEdit)
from PyQt6.QtCore import (Qt)

from home.home import BaseHomeWindow
from home.ui_functions import Tweakfunctions
from home.utils import *
from home.scheduler.scrapper import JWIZARD
# from home.css import congregation_view_css

class Scheduler(BaseHomeWindow):
	def scheduler_view(self):
		# set title and remove prevous children elements
		self.ui_tweaks.toggle_title(self, self.ui.home_button.text())
		self.ui_tweaks.remove_widget_children(self)
		Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		# check if user has a congregation or test database
		if database_exists():
			self.scheduler._after_scheduler_check(self)
		else:
			reply = QMessageBox.critical(None, "No Database Found!","You need to create a congregation database to proceed", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
			return (self.ui_tweaks.congregation_view(self), self.ui.congregation_button.setStyleSheet("background-color: #006699;"))

	def _after_scheduler_check(self):
		'''Call MonthDailog and get month and display'''
		dialog = MonthDialog(self)
		reply = dialog.exec()
		
		if not reply:
			return

		data = dialog.trange
		try:
			if not os.path.exists(os.path.join(os.getcwd(), self.meeting_path, f"{dialog.combo.currentText()}.json")):
				weeklist=[x for x in range(data[0]+1, data[1]+1)]
				basepath="https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/2022/{num}"
				jwizard = JWIZARD(basepath=basepath,weeklist=weeklist, pname=dialog.combo.currentText())
				asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
				asyncio.run(jwizard.main())
		except aiohttp.client_exceptions.ClientConnectorError:
			QMessageBox.critical(self, "Unexpected Error", "No Internet Connection. Please connect to the internet and try again")
			return
		except AttributeError:
			QMessageBox.critical(self, "Unexpected Error", f"Curren month selected {dialog.combo.currentText()} is yet to have a complete program or has a known bug")		
		
		# self.scroll = QScrollArea()
		# self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		# self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		# self.scroll.setWidgetResizable(True)
		# self.scroll.setWidget(self.ui.clone_widget)

		# get data from utils and create form
		frame = QFrame()
		frame.setObjectName("form_frame")

		form = QFormLayout()
		
		all_parts = self.sutils.get_all_parts(dialog.combo.currentText())
		for ap in all_parts:
			label = QLabel(ap)
			# label.setMaximumWidth(300)
			label.setWordWrap(True)

			input_field = QLineEdit()
			# input_field.setMaximumSize(200, 30)
			input_field.setStyleSheet("background-color: white;")
			input_field.setObjectName(ap.replace(" ", "_"))

			form.addRow(label, input_field)

		frame.setLayout(form)
		self.ui.clone_widget.layout().addWidget(frame)
		self.button_box = QDialogButtonBox(self)
		self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		# self.button_box.accepted.connect(self.accept)
		# self.button_box.rejected.connect(self.reject)
		self.ui.clone_widget.layout().addWidget(self.button_box)
		
class MonthDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
	
		self.setWindowTitle("Select a Month range")
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.setup_ui()
	
	def setup_ui(self):
		layout = QFormLayout()
		self.combo = QComboBox()
		self.combo.setObjectName("month_combo")
		self.combo.addItems(["January-February","March-April",
		"May-June", "July-August", "September-October", "November-December"])
		self.combo.setCurrentIndex(0)
		self.combo.setMinimumSize(100, 30)

		label = QLabel("Select a month range to display schedule:")
		layout.addRow(label, self.combo)
		self.layout.addLayout(layout)

		self.button_box = QDialogButtonBox(self)
		self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Yes)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.close)
		layout.addWidget(self.button_box)
	
	def accept(self):
		'''Get the months and split them up for processing'''
		selected_months = self.combo.currentText()
		
		selected_months = selected_months.split("-")
		self.trange = get_range(selected_months[0], selected_months[1])
		super().accept()
		

