'''
Module to manage the nwbs module

Updater() >> Contains functions to check for updates and returns main window
if updates or not.
'''

import sys
import os
import resources
import random
import logging
import asyncio
import config

from datetime import date, datetime
from importlib import import_module
from PyQt6.QtWidgets import QApplication
from _updater import Updater

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def logCode() -> tuple[str, str]:
	t = datetime.now().strftime("%Y-%m-%d")
	log_code = random.randint(10000, 99999)
	return t, str(log_code)

if not os.path.exists(os.path.join(os.getcwd(), config.STORAGE_FOLDER)):
	'''Create the dir for app usage'''
	for sfn in config.STORAGE_FOLDER_NAMES:
		os.makedirs(os.path.join(os.getcwd(), config.STORAGE_FOLDER, sfn))

	for dfn in config.DEFAULT_FOLDER_NAMES:
		os.makedirs(os.path.join(os.getcwd(), config.DEFAULT_FOLDER, dfn)
)

logger = logging.getLogger(__name__)
logging.basicConfig(
	filename=config.LOG_PATH + f"/__main__{logCode()[0]}_{logCode()[1]}.log",
	format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
	level=logging.DEBUG
	)

if config.PRODUCTION:
	try:
		__version__ = getattr(import_module('scripts'), '__version__')
		home = getattr(import_module('scripts.nwbs.home'), 'BaseHomeWindow')
		create_database = getattr(import_module('scripts.nwbs.utils'), 'create_database')
		create_months = getattr(import_module('scripts.nwbs.utils'), 'create_months')
	except ModuleNotFoundError:
		logger.exception('Module Not Found. >> traceback erorr below', exc_info=True)
else:
	from nwbs.utils import create_database, create_months
	from nwbs.home import BaseHomeWindow as home


class Launcher(QApplication):
	def __init__(self, *args, **kwargs):
		super(Launcher, self).__init__(*args, **kwargs)
		self.update_day:int = config.CHECK_FOR_UPDATES_DAY
		self.user_time:int = date.today().day

		if self.user_time == self.update_day:
			updater = Updater()
			asyncio.run(updater.check_updates())
		
		self.the_json = f"{date.today().year}.json"
		if not create_database(config.DATABASE_NAME):
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
