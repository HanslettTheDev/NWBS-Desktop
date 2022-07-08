import os
import json

class SchedulerUtils:
	def __init__(self):
		self.meeting_path = "meeting_parts"
		self.keys = ("preaching_points", "preaching_time", "middle_parts_time", "book_study_box")
	
	def get_all_parts(self, filename:str) -> list:
		with open(os.path.join(os.getcwd(), self.meeting_path, f"{filename}.json"), "r") as f:
			blob = json.load(f)
		full_program = list()
		for dat, _dict in blob.items():
			for title, part in _dict.items():
				if title == "preaching":
					for p in part:
						full_program.append(p)
					continue
				if title == "middle_parts":
					for p in part:
						full_program.append(p)
					continue
				if title in self.keys:
					continue
				full_program.append(part)
		return full_program