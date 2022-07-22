import sys
from datetime import date
from PyQt6.QtWidgets import (QApplication)
from home.home import BaseHomeWindow
import resources
# from login.login import BaseLoginWindow
from home.utils import create_database, create_months

import logging

class Launcher(QApplication):
    def __init__(self, *args, **kwargs):
        super(Launcher, self).__init__(*args, **kwargs)
        logging.basicConfig(filename='cartronic_log.log', level=logging.DEBUG, filemode="w", format='%(asctime)s: %(lineno)d: %(funcName)s: %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        
        self.the_json = f"{date.today().year}.json"
        if not create_database("congregation.sqlite"):
            sys.exit(1)
        
        if int(self.the_json.split(".")[0]) != date.today().year:
            create_months()
        
        try:
            self.home_window = BaseHomeWindow()
            self.home_window.show()
        except Exception:
            self.logger.critical("Application crashed. Below is why:", exc_info=True)
            sys.exit(1)

        # self.login_window = BaseLoginWindow()
        # self.login_window.show()


if __name__ == '__main__':
    app = Launcher(sys.argv)
    sys.exit(app.exec())