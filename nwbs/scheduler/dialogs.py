from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout,
QComboBox, QLabel, QFormLayout, QDialogButtonBox, QWidget, 
 QTextBrowser, QLineEdit, QCompleter)

from nwbs.utils import get_range

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtCore import (Qt)

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
	