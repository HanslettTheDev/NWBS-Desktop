import asyncio
import time
import random
import aiohttp
import logging
from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout,
QComboBox, QLabel, QFormLayout, QDialogButtonBox, QWidget, 
QHBoxLayout, QTextBrowser, QScrollArea, QPushButton, QFrame, QLineEdit, QCompleter)
from PyQt6.QtCore import (Qt, pyqtSignal, pyqtSlot)

from nwbs.home import BaseHomeWindow
from nwbs.ui_functions import Tweakfunctions
from nwbs.utils import *
from nwbs.scheduler.scrapper import JWIZARD
# from home.css import congregation_view_css

import logging
import random
from datetime import datetime

now = datetime.now()
t = now.strftime("%Y-%m-%d")
log_code = random.randint(10000, 99999)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(funcName)s: %(levelname)s: %(message)s')

file_handler = logging.FileHandler(f'logs/scheduler/log_{t}_{log_code}.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

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
			return (self.congregation.congregation_view(self), self.ui.congregation_button.setStyleSheet("background-color: #006699;"))

	def _after_scheduler_check(self):
		'''Call MonthDailog and get month and display else return reports'''
		if os.listdir(os.path.join(os.getcwd(), "_programs")):
			return self.scheduler.show_previous_programs(self)
		
		self.scheduler_popup(self)
		
	
	'''
	Functions Listed here are organized in a FirstCome FirstServe
	Each function written that contains any click events or slots to other functions 
	are directly written after it. check the documentation to see more details
	'''
	def show_previous_programs(self):
		files = os.listdir(os.path.join(os.getcwd(), "_programs"))
		# create a frame and a Horizontal layout and add items inside
		random_colors = ["#1F4690", "#937DC2", "#377D71", "#2C3639", "#06283D", "#495C83", "#513252"]

		button = QPushButton("Create New Program")
		button.setObjectName("create_button")
		button.setMinimumHeight(50)
		button.setStyleSheet(f"background-color: {random.choice(random_colors)}; font-size: 20px;color:white;")
		button.clicked.connect(lambda: self.scheduler.scheduler_popup(self))
		self.ui.main_frame.layout().addWidget(button)
		
		for file in files:	
			frame = QFrame()
			frame.setLayout(QVBoxLayout())
			frame.setObjectName("frame_" + str(files.index(file)))
			frame.setMinimumSize(300,200)
			frame.setStyleSheet('''
			QPushButton {
				background-color: #006699;
				color: white;
				font-size: 20px;
			}
			''')

			label = QLabel(f"{file.split(' program.')[0]} program")
			label.setWordWrap(True)
			label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			label.setMinimumHeight(200)
			label.setStyleSheet(f"background-color: {random.choice(random_colors)}; color: white; text-align:center; font-size: 25px;")
			
			preview_button = QPushButton("Preview")
			preview_button.setMinimumHeight(40)
			preview_button.setCheckable(True)
			preview_button.setObjectName("preview_button_{index}".format(index=files.index(file)))
			preview_button.clicked.connect(lambda: self.scheduler.preview_program(self))
			download_button = QPushButton("Download")
			download_button.setMinimumHeight(40)
			download_button.clicked.connect(lambda: self.scheduler.open_page(self))

			frame.layout().addWidget(label)
			frame.layout().addWidget(preview_button)
			frame.layout().addWidget(download_button)

			self.ui.clone_widget.layout().addWidget(frame)
	
	def preview_program(self):
		text = ""
		for button in self.ui.clone_widget.findChildren(QPushButton):
			if button.isChecked():
				button.setCheckable(False)
				# get the QLabel from the parent widget
				text += button.parent().findChild(QLabel).text()
				# display the preview
				break
		# Launch the preview 
		self.preview = Preview(None, text.split(" program")[0], 
		self.sutils.create_program(text.split(" program")[0]))

		# make the buttons checkable
		for button in self.ui.clone_widget.findChildren(QPushButton):
			button.setCheckable(True)
	
	def open_page(self):
		text = ""
		for button in self.ui.clone_widget.findChildren(QPushButton):
			if button.isChecked():
				button.setCheckable(False)
				text = button.parent().findChild(QLabel).text()
				break
		
		if text != "":
			output = self.sutils.create_program(text.split(" program")[0])
			self.sutils.open_page(text.split(" program")[0], output)
			QMessageBox.information(self, "Downloading", "You will view this program in your web browser and then save it using the print function", QMessageBox.StandardButton.Ok)

		# make the buttons checkable
		for button in self.ui.clone_widget.findChildren(QPushButton):
			button.setCheckable(True)		

	def scheduler_popup(self):
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
		# self.scroll.setWidgetResizable(True)
		# self.scroll.setWidget(self.ui.clone_widget)

		def get_parts():
			parts = self.sutils.get_all_parts(dialog.combo.currentText())
			for p in parts:
				yield p
		
		self.cloop = get_parts()
		self.month_programs = []
			
		def main():
			try:
				cloop = next(self.cloop)
				pdialog = ProgramDialog(self, dialog.combo.currentText(), cloop)
				if not pdialog.exec():
					self.month_programs = []
					return QMessageBox.information(self, "Program Cancelled", "Program Cancelled!")
				self.month_programs.append(pdialog.form_data)
				return main()
			except StopIteration:
				return
		main()
		
		if len(self.month_programs) != [] and len(self.month_programs) == len([x for x in self.sutils.get_all_parts(dialog.combo.currentText())]):
			self.sutils.save_program(dialog.combo.currentText()+" program.json", self.month_programs)
		
		return self.scheduler.scheduler_view(self)	

class ProgramDialog(QDialog):
	def __init__(self, parent=None, month="", _dict:dict={}):
		super().__init__(parent=parent)
		self.month = month
		self._dict = _dict
		self.elders = []
		self.all_publishers = []
		self.ms_elders = []
		self.elders_query = QSqlQuery()
		self.publishers_query = QSqlQuery()
		self.ms_elders_query = QSqlQuery()

		# prepare all the queries needed
		'''Prepare and launch all queries'''
		try:
			self.elders_query.prepare('''
				SELECT first_name, middle_name, last_name, role FROM congregation_publishers WHERE role = 'Elder' 
			''')
			self.elders_query.exec()
			while self.elders_query.next():
				self.elders.append(" ".join(self.elders_query.value(i) for i in range(0,3)))

			self.publishers_query.prepare('''
				SELECT first_name, middle_name, last_name, role FROM congregation_publishers
			''')
			self.publishers_query.exec()
			while self.publishers_query.next():
				self.all_publishers.append(" ".join(self.publishers_query.value(i) for i in range(3)))
			
			self.ms_elders_query.prepare('''
				SELECT first_name, middle_name, last_name, role FROM congregation_publishers WHERE role = 'Elder' OR role = ''
			''')
			self.ms_elders_query.exec()
			while self.ms_elders_query.next():
				self.ms_elders.append(" ".join(self.ms_elders_query.value(i) for i in range(3)))
		except Exception as e:
			return QMessageBox.critical(self, "Unexpected Error", f"Error: {e}")	

		self.setWindowTitle("Scheduler | " + self.month)
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.setup_ui(self._dict)

	def setup_ui(self, _dict):
		''' Create different completers after inheriting from the lists gotten from the sql query '''
		completer = QCompleter(self.elders)
		completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		completer.setFilterMode(Qt.MatchFlag.MatchContains)
		completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

		completer2 = QCompleter(self.all_publishers)
		completer2.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		completer2.setFilterMode(Qt.MatchFlag.MatchContains)
		completer2.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

		completer3 = QCompleter(self.ms_elders)
		completer3.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		completer3.setFilterMode(Qt.MatchFlag.MatchContains)
		completer3.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

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
		self.chairman_input.setCompleter(completer)
		self.group_label_input = QLineEdit()
		self.group_label_input.setObjectName("group_input")
		self.bible_reading_input = QLineEdit()
		self.bible_reading_input.setObjectName("bible_reading_input")
		self.bible_reading_input.setCompleter(completer2)
		self.ffsee_bible_input = QLineEdit()
		self.ffsee_bible_input.setObjectName("ffsee_bible")
		self.ffsee_bible_input.setCompleter(completer3)
		self.fflesson_input = QLineEdit()
		self.fflesson_input.setObjectName("fflesson_input")
		self.fflesson_input.setCompleter(completer3)
		self.song_input = QLineEdit()
		self.song_input.setObjectName("song_input")
		self.song_input.setCompleter(completer2)

		form.addRow(month_label)
		form.addRow(group_label, self.group_label_input)
		form.addRow(chairman_label, self.chairman_input)
		form.addRow(song_label, self.song_input)
		form.addRow(fflesson_label)
		form.addRow(fflesson_label_2, self.fflesson_input)
		form.addRow(ffsee_bible, self.ffsee_bible_input)
		form.addRow(bible_reading, self.bible_reading_input)
		form.addRow(live_as)
		note = QLabel(f"Use (Student/Participant) format or (Student) if it's a talk or a First time video. e.g First Time: John Parker/Parker Smith")
		note.setStyleSheet("color: #EB1D36;font-size: 12px")
		form.addRow(note)

		for index, parts in enumerate(_dict['preaching']):
			label = QLabel(parts)
			self.input_field = QLineEdit()
			self.input_field.setObjectName(f"input_preaching_{str(index)}")
			self.input_field.setCompleter(completer2)
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
			self.input_field.setCompleter(completer)
			form.addRow(label, self.input_field)
		
		cong_bible_label = QLabel(f"Congregation Bible Study {_dict['book_study']}: E.G (Conductor/Reader)")
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
		
		self.form_data = {
			f"{self._dict['month']}": {
				"group": self.group_label_input.text(),
				"chairman": self.chairman_input.text(),
				"opening_prayer": self.song_input.text(),
				"fine_fine_lesson": self.fflesson_input.text(),
				"fine_fine_things_weh_you_see": self.ffsee_bible_input.text(),
				"bible_reading": self.bible_reading_input.text(),
				"preaching": [widget.text() for widget in self.findChildren(QLineEdit) if widget.objectName().startswith("input_preaching_")],
				"middle_parts": [widget.text() for widget in self.findChildren(QLineEdit) if widget.objectName().startswith("input_middle_parts_")],
				"cong_bible_study": self.cong_bible_input.text(),
				"closing_prayer": self.conc_song_input.text()
			}
		}
		
		super().accept()

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
		
class Preview(QWidget):
	def __init__(self, parent=None, month="", html=""):
		super().__init__(parent=parent)
		self.setWindowTitle(f"NWBS Scheduler | {month} Preview")
		self.html = html
		self.setLayout(QVBoxLayout())
		self.setMinimumSize(1000,700)
		self.setup_ui()

		self.show()
		
	def setup_ui(self):
		self.preview = QTextBrowser()
		self.preview.setHtml(self.html)
		self.layout().addWidget(self.preview)
		
		
	

