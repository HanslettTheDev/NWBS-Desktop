import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
QWidget, QLabel, QLineEdit,)

import sys

from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, 
QWidget, QLabel, QLineEdit)

from interface.login import Ui_MainWindow as LoginWindow

class BaseLoginWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(BaseLoginWindow, self).__init__(*args, **kwargs)
        self.ui = LoginWindow()
        self.ui.setupUi(self)
        
        #set window defaults
        self.setWindowTitle("NWB SCHEDULER - LOGIN")