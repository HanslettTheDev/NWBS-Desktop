import config
import aiohttp
import logging
import sys
import aiofiles
import os
import zipfile

from PyQt6.QtWidgets import (QApplication, QMessageBox)

from nwbs import logCode

logger = logging.getLogger(__name__)
logging.basicConfig(
	filename=config.LOG_PATH + f"/__main__{logCode()[0]}_{logCode()[1]}.log",
	format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
	level=logging.DEBUG
)

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
			return UpdaterMessages(sys.argv).error()
		
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
		NWBS Client will work normally. Try again later to update. Check the logs
		''')

	def install_error(self):
		return QMessageBox.critical(None, "Unexpected Error!", "An error Occured while installing the update! No changes were made!")