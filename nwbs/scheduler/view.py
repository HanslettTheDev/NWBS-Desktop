import asyncio
import os
import time
import random
import aiohttp
import logging
import config
from PyQt6.QtWidgets import (QMessageBox, QVBoxLayout,
QLabel, QPushButton, QFrame)
from PyQt6.QtCore import (Qt)

from nwbs import logCode
from nwbs.home import BaseHomeWindow
from nwbs.ui_functions import Tweakfunctions
from nwbs.utils import database_exists
from nwbs.scheduler.scrapper import JWIZARD
from nwbs.scheduler.dialogs import *
# from home.css import congregation_view_css

import logging
import random

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=config.LOG_PATH + f"/__nwbs__{logCode()[0]}_{logCode()[1]}.log",
    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
    level=logging.DEBUG
)

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
		if os.listdir(os.path.join(os.getcwd(), config.FOLDER_REFERENCES["generated_programs"])):
			return self.scheduler.show_previous_programs(self)
		
		self.scheduler.scheduler_popup(self)
		
	
	'''
	Functions Listed here are organized in a FirstCome FirstServe
	Each function written that contains any click events or slots to other functions 
	are directly written after it. check the documentation to see more details
	'''
	def show_previous_programs(self):
		files = os.listdir(os.path.join(os.getcwd(), config.FOLDER_REFERENCES["generated_programs"]))
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
		'''Opens a browser to download the full program'''
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
		'''Contains the pop up for a first time user when the need to create their first program'''
		dialog = MonthDialog(self)
		reply = dialog.exec()
		
		if not reply:
			return self.congregation.congregation_view(self)

		data = dialog.trange
		try:
			if not os.path.exists(os.path.join(os.getcwd(), self.meeting_path, f"{dialog.combo.currentText()}.json")):
				weeklist=[x for x in range(data[0]+1, data[1]+1)]
				basepath=config.SCRAPPER_LINK
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
		
	

