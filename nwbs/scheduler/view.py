import asyncio
from datetime import datetime
import json
import os
import random
import aiohttp
import logging
import config
from PyQt6.QtWidgets import (QMessageBox, QVBoxLayout,
QLabel, QPushButton, QFrame)
from PyQt6.QtCore import (Qt)

from nwbs import logCode
from nwbs.home import BaseHomeWindow
from nwbs.scheduler.utils import get_weeks, get_all_urls
from nwbs.ui_functions import Tweakfunctions
from nwbs.utils import database_exists
from nwbs.scheduler.scrapper import JWIZARD
from nwbs.scheduler.dialogs import *
from config import FOLDER_REFERENCES
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
        
    # Functions Listed here are organized in a FirstCome FirstServe
    # Each function written that contains any click events or slots to other functions 
    # are directly written after it. check the documentation to see more details
    
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
            output2 = self.sutils.create_program(text.split(" program")[0], is_schedule=True)
            self.sutils.preview_page(text.split(" program")[0], output)
            self.sutils.preview_page(text.split(" program")[0] + " scheduler", output2) # for the schedule to fill names
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

        try:
            if not os.path.exists(os.path.join(os.getcwd(), config.FOLDER_REFERENCES["meeting_parts"], f"{dialog.combo.currentText()}.json")):
                month = dialog.combo.currentText()
                monthx = get_weeks(month.split("-")[0].strip(), datetime.now().year)
                monthy = get_weeks(month.split("-")[1].strip(), datetime.now().year)
                weeklist = {
                    month.split("-")[0]: monthx,
                    month.split("-")[-1]: monthy
                }
                jwizard = JWIZARD(
                    basepath=config.NEW_LINK, 
                    weeklist=weeklist, 
                    pname=month,
                    links=get_all_urls(weeklist, config.NEW_LINK, month)
                )
                asyncio.run(jwizard.main())
        except aiohttp.client_exceptions.ClientConnectorError:
            QMessageBox.critical(self, "Unexpected Error", "No Internet Connection. Please connect to the internet and try again")
            return
        except AttributeError:
            logging.error("Unexpected error occured while fetching for a program:", exc_info=True)
            QMessageBox.critical(self, "Unexpected Error", f"Current month selected {dialog.combo.currentText()} is yet to have a complete program or has a bug")		
            return
        except IndexError:
            logging.error("Unexpected error occured while fetching for a program:", exc_info=True)
            QMessageBox.critical(self, "Unexpected Error", f"Current month selected {dialog.combo.currentText()} is yet to have a complete program or has a bug")
            return 
        
        parts = self.sutils.get_all_parts(dialog.combo.currentText())
        self.month_programs = []
        self.backup = [] # stores the data to use for the previous items
        self.count = 0

        def main(has_pre_data:dict = {}):
            try:
                pdialog = ProgramDialog(self, dialog.combo.currentText(), parts[self.count], self.count, has_pre_data)
                if not pdialog.exec():
                    if pdialog.previous_clicked:
                        self.count -= 1
                        return main(self.backup[self.count])
                    # reset the counter and list
                    self.month_programs = []
                    self.count = 0
                    return QMessageBox.information(self, "Program Cancelled", "Program Cancelled!")
                
                self.month_programs.insert(self.count, pdialog.form_data)
                # Blah blah blah I know I duplicated It but I'm being safe here
                # I don't want the month_programs variable to be tampered with before time
                # This is a safety measure
                self.backup.insert(self.count, pdialog.form_data)
                self.count += 1
                return main()
            except StopIteration:
                return
            except IndexError:
                return

        # Call the recursive function 
        main()
        
        if len(self.month_programs) != [] and len(self.month_programs) == len([x for x in self.sutils.get_all_parts(dialog.combo.currentText())]):
            self.sutils.save_program(dialog.combo.currentText()+" program.json", self.month_programs)
        
        return self.scheduler.scheduler_view(self)		
        
    

