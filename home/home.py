import sys

from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, 
QWidget, QLabel, QLineEdit)

from interface.home import Ui_MainWindow as HomeWindow
from home.models import PublisherModel

class BaseHomeWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(BaseHomeWindow, self).__init__(*args, **kwargs)
        self.ui = HomeWindow()
        self.ui_tweaks = InterfaceTweaks
        self.congregation = Congregation
        self.scheduler = Scheduler
        self.reports = Reports
        self.table_model = PublisherModel()
    
        self.ui.setupUi(self)

        #set window defaults

        #set button checkable
        self.ui_tweaks.button_checkable(self)

        #load all interface tweaks
        self.ui_tweaks.set_clone_widget_type(self)
        self.ui_tweaks.toggle_title(self, "V1.0.0")
        self.ui_tweaks.home_view(self) # Load the home view by default


        self.ui.home_button.clicked.connect(lambda: self.ui_tweaks.home_view(self))
        self.ui.congregation_button.clicked.connect(lambda: Congregation.congregation_view(self))
        self.ui.scheduler_button.clicked.connect(lambda: Scheduler.scheduler_view(self))
        self.ui.reports_button.clicked.connect(lambda: Reports.reports_view(self))

from home.ui_functions import InterfaceTweaks
from home.congregation.view import Congregation
from home.scheduler.view import Scheduler
from home.reports.view import Reports