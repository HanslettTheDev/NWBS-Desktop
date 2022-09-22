import os
import json
import webbrowser
import logging
import config

from jinja2 import Environment, FileSystemLoader
from nwbs import logCode
from nwbs.html import default_program_html

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=config.LOG_PATH + f"/_utils_{logCode()[0]}_{logCode()[1]}.log",
    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
    level=logging.DEBUG
)


class SchedulerUtils:
	def __init__(self):
		self.paths = config.FOLDER_REFERENCES
		self.keys = ("preaching_points", "preaching_time", "middle_parts_time", "book_study_box")
	
	def get_all_parts(self, filename:str) -> list:
		with open(os.path.join(os.getcwd(), self.paths["meeting_path"], f"{filename}.json"), "r") as f:
			blob = json.load(f)
		full_program = list()
		for dat, _dict in blob.items():
			full_program.append(_dict)
		return full_program
	
	def save_program(self, filename:str, _dict:list) -> bool:
		blob = {}
		for _d in _dict:
			for key, value in _d.items():
				blob[key] = value
				with open(os.path.join(os.getcwd(), self.paths["generated_programs"], filename), "w") as f:
					json.dump(blob, f, indent=4)
		logger.debug(f"Program saved: FileName > {filename}.json")
		return True
	
	def create_program(self, program_name) -> str:
		# Get the data and programs from the json and pass it as objects to the txt
		with open(os.path.join(os.getcwd(), self.paths["generated_programs"], program_name + " program.json"), "r", encoding="utf-8") as f:
			blob = json.load(f)
		
		with open(os.path.join(os.getcwd(), self.paths["meeting_parts"], program_name + ".json"), "r", encoding="utf-8") as f:
			blob2 = json.load(f)

		# create the file and write the defaults to it
		with open(os.path.join(os.getcwd(), self.paths["templates"], program_name + ".html"), "w") as f:
			f.write(default_program_html)
		
		# get only the dicts from the json
		data = [value for key, value in blob.items()]
		programs = [value for key, value in blob2.items()]

		# do clean checks to get time for middle parts and preaching
		for d in programs:
			global time_stands
			time_stands = self.update_time(d["preaching_time"], d["middle_parts_time"])
			
		for d in data:
			global vid
			vid = [x for x in d['preaching'][0].strip(":")]

		try:
			template_env = Environment(loader=FileSystemLoader('templates'))
			template_object = template_env.get_template(f'{program_name}.html')
			output = template_object.render(programs=blob, data=blob2, zip=zip, zip2=enumerate, length=len,
			preachingt=time_stands[0], middlepartst=time_stands[1], vid=vid)
		except Exception as e:
			logger.exception(f"An error occured while generating a program. See Error >>", exc_info=True)
		else:
			logger.debug("Templates successfully generated")
			return output

	def update_time(self, preaching_time:list, middle_time:list) -> tuple:
		default_time = 2
		default_middle_time = 21
		pt_time = []
		mt_time = []
		# Get the evaluated time of each preaching part
		for p in preaching_time: 
			default_time += int(p)
			pt_time.append(default_time)
		for m in middle_time:
			default_middle_time += int(m)
			mt_time.append(default_middle_time)
		# pt_time.pop()
		# mt_time.pop()
		return pt_time,mt_time
	
	def open_page(self, filename:str, html):
		file_path = os.path.join(os.getcwd(), self.paths["templates"], filename+".html")
		with open(file_path, "w", encoding="utf-8") as f:
			f.write(html)
		webbrowser.open(file_path)
		logger.debug(f"Program created: Location >> {file_path}")

	def test_pdf(self, html=""):
		pass