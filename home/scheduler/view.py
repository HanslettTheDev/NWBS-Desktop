import asyncio
from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout,
QComboBox, QLabel, QFormLayout, QDialogButtonBox, 
QHBoxLayout)

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
			weeklist=[]
			for i in range(data[0]+1, data[1]+1):
				weeklist.append(i)
			print(weeklist)
			basepath="https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/2022/{num}"
			jwizard = JWIZARD(basepath=basepath,weeklist=weeklist)
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
			asyncio.run(jwizard.main())
		except Exception as e:
			print(e)
		
		
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
		

