import os
import json
import webbrowser
import logging
import config

from jinja2 import Environment, FileSystemLoader
from nwbs import logCode
from nwbs.html import default_program_html, program_setup

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=config.LOG_PATH + f"/_utils_{logCode()[0]}_{logCode()[1]}.log",
    format='%(asctime)s: %(funcName)s: %(levelname)s: %(message)s',
    level=logging.ERROR
)


class SchedulerUtils:
	def __init__(self):
		self.paths = config.FOLDER_REFERENCES
		self.keys = ("preaching_points", "preaching_time", "middle_parts_time", "book_study_box")
	
	def get_all_parts(self, filename:str) -> list:
		with open(os.path.join(os.getcwd(), self.paths["meeting_parts"], f"{filename}.json"), "r") as f:
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
	
	def create_program(self, program_name, is_schedule:bool = False) -> str:
		# Get the data and programs from the json and pass it as objects to the txt
		with open(os.path.join(os.getcwd(), self.paths["generated_programs"], program_name + " program.json"), "r", encoding="utf-8") as f:
			blob = json.load(f)
		
		with open(os.path.join(os.getcwd(), self.paths["meeting_parts"], program_name + ".json"), "r", encoding="utf-8") as f:
			blob2 = json.load(f)

		# create the file and write the defaults to it
		with open(os.path.join(os.getcwd(), self.paths["templates"], program_name + ".html"), "w") as f:
			f.write(default_program_html)
		
		if is_schedule:
			with open(os.path.join(os.getcwd(), self.paths["templates"], program_name + " scheduler.html"), "w") as f:
				f.write(program_setup)
		
		# get only the dicts from the json
		data = [value for key, value in blob.items()]
		programs = [value for key, value in blob2.items()]

		# do clean checks to get time for middle parts and preaching
		time_stands_1 = []
		time_stands_2 = []
		for d in programs:
			pt_time, mp_time = {},{}
			s = self.update_time(d["preaching_time"], d["middle_parts_time"])
			pt_time[d["month"]], mp_time[d["month"]] = s[0], s[1]
			time_stands_1.append(pt_time)
			time_stands_2.append(mp_time)
		
		for d in data:
			global vid
			vid = [x for x in d['preaching'][0].strip(":")]

		try:
			template_env = Environment(loader=FileSystemLoader(f'{os.path.join(os.getcwd(), self.paths["templates"])}'))
			template_object = None
			if not is_schedule:
				template_object = template_env.get_template(f'{program_name}.html')
			else:
				template_object = template_env.get_template(f'{program_name} scheduler.html')
			output = template_object.render(
				programs=blob, data=blob2, zip=zip, zip2=enumerate, 
				length=len, preachingt=time_stands_1, middlepartst=time_stands_2, 
				vid=vid, tostring=str, toint=int
			)
			logger.debug("Templates successfully generated")
			return output
		except Exception as e:
			logger.exception(f"An error occured while generating a program. See Error >>", exc_info=True)

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
	
	def preview_page(self, filename:str, html):
		file_path = os.path.join(os.getcwd(), self.paths["templates"], filename+".html")
		with open(file_path, "w", encoding="utf-8") as f:
			f.write(html)
		webbrowser.open(file_path)
		logger.debug(f"Program created: Location >> {file_path}")

	def test_pdf(self, html=""):
		pass