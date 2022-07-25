__version__ = "V1.0.0"

import sys
import resources
import random
import logging

from datetime import date, datetime
from PyQt6.QtWidgets import (QApplication)
from importlib import import_module



now = datetime.now()
t = now.strftime("%Y-%m-%d")
log_code = random.randint(10000, 99999)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(funcName)s: %(levelname)s: %(message)s')

file_handler = logging.FileHandler(f'logs/imports/_import_{t}_{log_code}.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

file_handler2 = logging.FileHandler(f'logs/__main__log_{t}_{log_code}.log')
file_handler2.setLevel(logging.DEBUG)
file_handler2.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(file_handler2)

PRODUCTION = True

if PRODUCTION:
    try:
        home = getattr(import_module('scripts.nwbs.home'), 'BaseHomeWindow')
        create_database = getattr(import_module('scripts.nwbs.utils'), 'create_database')
        create_months = getattr(import_module('scripts.nwbs.utils'), 'create_months')
    except ModuleNotFoundError:
        logger.exception('Module Not Found. >> traceback erorr below', exc_info=True)
else:
    from nwbs.utils import create_database, create_months
    from nwbs.home import BaseHomeWindow as home


class Updater():
    def __init__(self):
        pass

    def check_updates(self):
        pass

    def install_updates(self):
        pass
class Launcher(QApplication):
    def __init__(self, *args, **kwargs):
        super(Launcher, self).__init__(*args, **kwargs)
        
        self.the_json = f"{date.today().year}.json"
        if not create_database("congregation.sqlite"):
            sys.exit(1)
        
        if int(self.the_json.split(".")[0]) != date.today().year:
            create_months()
        
        try:
            self.home_window = home()
            self.home_window.show()
            logger.debug('Main Window Running >>')
        except Exception:
            logger.exception("Application crashed. Below is why:", exc_info=True)
            sys.exit(1)

if __name__ == '__main__':
    app = Launcher(sys.argv)
    sys.exit(app.exec())