import asyncio
import time
import aiohttp
from ssl import SSLError
from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout,
QComboBox, QLabel, QFormLayout, QDialogButtonBox, 
QHBoxLayout, QTextBrowser, QScrollArea, QPushButton, QFrame, QLineEdit, QCompleter)
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
			QMessageBox.critical(self, "Unexpected Error", f"Current month selected {dialog.combo.currentText()} is yet to have a complete program or has a known bug")		
		except IndexError:
			QMessageBox.critical(self, "Unexpected Error", f"Current month selected {dialog.combo.currentText()} is yet to have a complete program or has a known bug")
		# self.scroll = QScrollArea()
		# self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		# self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		# self.scroll.setWidgetResizable(True)
		# self.scroll.setWidget(self.ui.clone_widget)

		def get_parts():
			parts = self.sutils.get_all_parts(dialog.combo.currentText())
			for p in parts:
				yield p
		
		self.cloop = get_parts()	
			
		def main():
			try:
				cloop = next(self.cloop)
				pdialog = ProgramDialog(self, dialog.combo.currentText(), cloop)
				if not pdialog.exec():
					return self.scheduler.scheduler_view(self)
				return main()
			except StopIteration:
				return
		
		main()
class ProgramDialog(QDialog):
	def __init__(self, parent=None, month="", _dict:dict={}):
		super().__init__(parent=parent)
		self.month = month
		self._dict = _dict

		self.setWindowTitle("Scheduler | " + self.month)
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.setup_ui(self._dict)

	def setup_ui(self, _dict):
		form = QFormLayout()

		month_label = QLabel(f"Week of {_dict['month']} | {_dict['reading']}")
		group_label = QLabel(f"Group:")
		chairman_label = QLabel(f"Chairman:")
		song_label = QLabel(f"{_dict['opening_song']} and Opening Prayer")
		fflesson_label = QLabel("Fine Fine Lesson from bible")
		fflesson_label.setStyleSheet("background-color: rgb(87,90,93);color: white;font-size: 20px")
		fflesson_label_2 = QLabel(f"Fine Fine Lesson from bible {_dict['fine_fine_lesson']}: (10 min.)")
		ffsee_bible = QLabel("Fine Fine things weh you see for inside bible: (10 min.)")
		bible_reading = QLabel(f"Bible Reading ({_dict['bible_reading']})")
		live_as = QLabel("DE USE ALL YOUR HEART PREACH")
		live_as.setStyleSheet("background-color: rgb(190,137,0);color: white;font-size: 20px")
		
		self.chairman_input = QLineEdit()
		self.chairman_input.setObjectName("chairman_input")
		self.group_label_input = QLineEdit()
		self.group_label_input.setObjectName("group_input")
		self.bible_reading_input = QLineEdit()
		self.bible_reading_input.setObjectName("bible_reading_input")
		self.ffsee_bible_input = QLineEdit()
		self.ffsee_bible_input.setObjectName("ffsee_bible")
		self.fflesson_input = QLineEdit()
		self.fflesson_input.setObjectName("fflesson_input")
		self.song_input = QLineEdit()
		self.song_input.setObjectName("song_input")

		form.addRow(month_label)
		form.addRow(group_label, self.group_label_input)
		form.addRow(chairman_label, self.chairman_input)
		form.addRow(song_label, self.song_input)
		form.addRow(fflesson_label)
		form.addRow(fflesson_label_2, self.fflesson_input)
		form.addRow(ffsee_bible, self.ffsee_bible_input)
		form.addRow(bible_reading, self.bible_reading_input)
		form.addRow(live_as)

		for index, parts in enumerate(_dict['preaching']):
			label = QLabel(parts)
			self.input_field = QLineEdit()
			self.input_field.setObjectName(f"input_preaching_{str(index)}")
		
			form.addRow(label, self.input_field)

		# create a label for the Live as christians section
		mid_part_label = QLabel("DE LIVE CHRISTIAN LIFE")
		mid_part_label.setStyleSheet("background-color: rgb(126,0,36);color: white;font-size: 20px")
		mid_song_label = QLabel(f"{_dict['middle_song']}")

		form.addRow(mid_part_label)
		form.addRow(mid_song_label)

		for index, parts in enumerate(_dict['middle_parts']):
			label = QLabel(parts)
			self.input_field = QLineEdit()
			self.input_field.setObjectName(f"input_middle_parts_{str(index)}")
			form.addRow(label, self.input_field)
		
		cong_bible_label = QLabel(f"Congregation Bible Study {_dict['book_study']}")
		conc_song_label = QLabel(f"{_dict['opening_song']} and Closing Prayer")
		self.cong_bible_input = QLineEdit()
		self.cong_bible_input.setObjectName("closing_song_input")
		self.conc_song_input = QLineEdit()
		self.conc_song_input.setObjectName("closing_song_input")

		form.addRow(cong_bible_label, self.cong_bible_input)
		form.addRow(conc_song_label, self.conc_song_input)
		
		self.layout.addLayout(form)
		self.button_box = QDialogButtonBox(self)
		self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		form.addWidget(self.button_box)

	def accept(self):
		for widget in self.findChildren(QLineEdit):
			if widget.text() == "":
				return (QMessageBox.warning(self, "Error", "Please fill in all fields"), widget.setFocus(Qt.FocusReason.PopupFocusReason))
		return True
		# '''Get all inputs and check if any required was empty'''
		# print(f'''
		# results:
		# 1. {self.group_label_input.text()}
		# 2. {self.chairman_input.text()}
		# 3. {self.bible_reading_input.text()}
		# 4. {self.ffsee_bible_input.text()}
		# 5. {self.fflesson_input.text()}
		# 6. {self.song_input.text()}
		# 7. {self.conc_song_input.text()}
		# ''')
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
		

