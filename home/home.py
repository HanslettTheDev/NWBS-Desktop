import sys

from PyQt6.QtWidgets import (QMainWindow)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import (Qt)
import logging

from interface.home import Ui_MainWindow as HomeWindow
from home.models import PublisherModel
from home.scheduler.utils import SchedulerUtils

class BaseHomeWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(BaseHomeWindow, self).__init__(*args, **kwargs)
        self.ui = HomeWindow()
        self.ui_tweaks = InterfaceTweaks
        self.logger = logging.getLogger(__name__)
        self.congregation = Congregation
        self.scheduler = Scheduler
        self.sutils = SchedulerUtils()
        self.reports = Reports
        self.table_model = PublisherModel()

        self.setWindowIcon(QIcon(":/icons/logo.ico"))
    
        self.ui.setupUi(self)
        # self.ui.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        #set window defaults
        self.meeting_path = "meeting_parts"

        #set button checkable
        self.ui_tweaks.button_checkable(self)

        #load all interface tweaks
        # self.ui_tweaks.set_clone_widget_type(self)
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