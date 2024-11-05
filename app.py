'''
Module to manage the nwbs module

Updater() >> Contains functions to check for updates and returns main window
if updates or not.
'''

import sys
import os
import resources
import logging
import asyncio
import nwbs.config as config

from importlib import import_module
from PyQt6.QtWidgets import QApplication
from _updater import Updater



asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if not os.path.exists(os.path.join(os.getcwd(), config.STORAGE_FOLDER)):
	'''Create the dir for app usage'''
	for sfn in config.STORAGE_FOLDER_NAMES:
		os.makedirs(os.path.join(os.getcwd(), config.STORAGE_FOLDER, sfn))
		logging.debug(f"Created Storage Folder: {os.path.join(os.getcwd(), config.STORAGE_FOLDER, sfn)}")
	logging.info("Storage Folders created successfully")

logger = logging.getLogger(__name__)
logging.basicConfig(
	filename=os.path.join(os.getcwd(), config.LOG_PATH, config.LOG_FILE),
	encoding="utf-8",
	format='%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s',
	level=logging.DEBUG
)

if config.PRODUCTION:
	try:
		__version__ = getattr(import_module('nwbs'), '__version__')
		# nwbs = getattr(import_module('nwbs'), 'nwbs')
		home = getattr(import_module('nwbs.home'), 'BaseHomeWindow')
		create_database = getattr(import_module('nwbs.utils'), 'create_database')
		logger.info(f'Successfully imported: Application version: {__version__}')
	except ModuleNotFoundError:
		logger.critical('Module Not Found. >> traceback erorr below', exc_info=True)
		sys.exit(1)
else:
	from nwbs.utils import create_database
	from nwbs.home import BaseHomeWindow as home


class Launcher(QApplication):
	def __init__(self, *args, **kwargs):
		super(Launcher, self).__init__(*args, **kwargs)
		self.update_day:int = config.CHECK_FOR_UPDATES_DAY
		self.user_time:int = 2024

		if self.user_time == self.update_day:
			updater = Updater()
			asyncio.run(updater.check_updates())
		
		if not create_database(config.DATABASE_NAME):
			sys.exit(1)
		
		try:
			self.home_window = home()
			self.home_window.show()
			logger.debug('Main Window Running >>')
		except Exception:
			logger.critical("Application crashed. Below is why:", exc_info=True)
			sys.exit(1)


if __name__ == '__main__':
	app = Launcher(sys.argv)
	sys.exit(app.exec())
