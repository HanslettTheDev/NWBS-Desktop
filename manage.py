import sys

from PyQt6.QtWidgets import (QApplication)
from home.home import BaseHomeWindow
from login.login import BaseLoginWindow
from home.utils import create_database

class Launcher(QApplication):
    def __init__(self, *args, **kwargs):
        super(Launcher, self).__init__(*args, **kwargs)
        if not create_database("congregation.sqlite"):
            sys.exit(1)
        self.home_window = BaseHomeWindow()
        self.home_window.show()
        self.login_window = BaseLoginWindow()
        # self.login_window.show()


if __name__ == '__main__':
    app = Launcher(sys.argv)
    sys.exit(app.exec())