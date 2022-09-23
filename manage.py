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
import zipfile
import aiohttp
import aiofiles
import config

from datetime import date, datetime
from PyQt6.QtWidgets import (QApplication, QMessageBox)
from importlib import import_module

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


class Updater():
	def __init__(self):
		self.api = config.API_LINK
		self.current_version = config.VERSION_NUMBER

	async def check_updates(self):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(self.api) as response:
					blob = await response.json()
		except Exception as e:
			logger.debug("Unexpected Error Occured While Checking For Updates! >> traceback", exc_info=True)
			return sys.exit(Launcher(sys.argv).exec())
		
		latest_version = blob["tag_name"]
		url = blob['assets'][0]["browser_download_url"] if  blob['assets'][0]["browser_download_url"] else None
		# Check version numbers
		if self.check_version_numbers(latest_version):
			updates = await self.download_updates(url)
			
			if not updates:
				return UpdaterMessages(sys.argv).error()

			if not self.install_updates(url.split("/")[-1]):
				return UpdaterMessages(sys.argv).install_error()
			
			logger.debug(f"NWBS Client updated: Version Number: {self.current_version}")
			
			UpdaterMessages(sys.argv).success()
			return True
		else:
			return False

	def check_version_numbers(self, latest_version:str):
		cv = self.current_version.split("V")[1].split('.')
		lv = latest_version.split("V")[1].split('.')

		for i in range(1,4):
			if int(lv[-i]) > int(cv[-i]):
				return True
		return False

	async def download_updates(self, url):
		if url == None:
			return False
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				assert response.status == 200
				data = await response.read()
		
		async with aiofiles.open(os.path.join(os.getcwd(),url.split("/")[-1]), mode="wb") as f:
			await f.write(data)
		return True

	def install_updates(self, filename):
		path_to_file = os.path.join(os.getcwd(), filename)
		if os.path.isfile(path_to_file) and zipfile.is_zipfile(path_to_file):
			try:
				zipfile.ZipFile(path_to_file).extractall()
			except Exception as e:
				logger.exception("Something went wrong when decompressing >> traceback", exc_info=True)
				return False
		self.delete_update_file(path_to_file)
		return True

	def delete_update_file(self, file):
		os.remove(file)

class UpdaterMessages(QApplication):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def success(self):
		return QMessageBox.information(None, "NWBS Updated!", "NWBS Client Was Updated Succesfully!")
	
	def error(self):
		return QMessageBox.critical(None, "Unexpected Error!", '''An error Occured while trying to download updates! No changes have been made.
		NWBS Client will work normally. Try again later to update...
		''')

	def install_error(self):
		return QMessageBox.critical(None, "Unexpected Error!", "An error Occured while installing the update! No changes were made!")

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