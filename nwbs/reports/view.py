from PyQt6.QtWidgets import (QMessageBox)

from nwbs import logCode
from nwbs.home import BaseHomeWindow
from nwbs.ui_functions import Tweakfunctions
from nwbs.utils import *
# from home.css import congregation_view_css
import logging
import random

from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=config.LOG_PATH + f"/__nwbs__{logCode()[0]}_{logCode()[1]}.log",
    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
    level=logging.ERROR
)


class Reports(BaseHomeWindow):
	def reports_view(self):
		return QMessageBox.information(self, "Reports |", "Currently this feature is still in development. Check for updates soon.")
		# self.ui_tweaks.toggle_title(self, self.ui.home_button.text())
		# self.ui_tweaks.remove_widget_children(self)
		# Tweakfunctions.check_ischecked(self, self.ui.navbar_frame)

		# # check if user has a congregation or test database
		# if database_exists():
		# 	pass
		# else:
		# 	QMessageBox.critical(None, "No Database Found!","You need to create a congregation database to proceed", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
		# 	return (self.ui_tweaks.congregation_view(self), self.ui.congregation_button.setStyleSheet("background-color: #006699;"))