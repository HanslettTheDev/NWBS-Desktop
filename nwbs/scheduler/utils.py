import os
import json
import webbrowser
import logging
import nwbs.config as config
import calendar
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from nwbs.html import default_program_html, program_setup

logger = logging.getLogger(__name__)

def get_weeks(month: str, year: int):
    month_dict = {name: num for num, name in enumerate(calendar.month_name) if num}
    month_int = month_dict[month]
    
    all_weeks = calendar.Calendar().monthdayscalendar(year, month_int)
    weeks = [f"{week[0]}-{week[-1]}" for week in all_weeks if 0 not in week]
    last_week = all_weeks[-1]
        
    if last_week[-1] == 0:
        non_zero_weeks = [x for x in last_week if x != 0]
        # grab the id of the current month and add 1 on the id to get
        # the next month and append to the string
        #if the month id is 12 = december, just reset it back to 1 = January 
        next_month_id = month_int + 1 if month_int != 12 else 1
        next_month_name = [
            key for key, value in month_dict.items() if next_month_id == value
        ][-1]
        weeks.append(f"{non_zero_weeks[0]}-{next_month_name}-{len(last_week)-len(non_zero_weeks)}")
            
    return weeks


def get_all_urls(weeklist: dict, basepath: str, xmonth: str):
    urls = []
    for month, weeks in weeklist.items():
        for week in weeks:
            urls.append(basepath.format(
                week=week, 
                year=str(datetime.now().year),
                monthx=xmonth.lower().strip(),
                current_month=month.lower()
            ))
    return urls


class MeetingParser:
    def __init__(self, program: dict, week_range: str):
        self.program = program
        self.week_range = week_range

    def capitalize(self, name: str) -> str:
        """ It automatically uppercases the first name and capitalizes the
        the other names
        """
        if name == "" or name == " ":
            return name

        
        splitted_name = name.split(" ")
        cap_name = []
        for sn in splitted_name:
            if splitted_name.index(sn) == 0:
                cap_name.append(sn.upper())
                continue
            cap_name.append(sn.capitalize())
        return " ".join(cap_name)

    def preaching_capitalize(self, name: str) -> dict:
        """Handles capitalizing cases only with strings from preaching section"""
        if name == "" or name == " ": 
            return {"student": "", "assistant": ""}
        
        splitted_name = name.split("/")
        
        if len(splitted_name) <= 1:
            return {
                "student": self.capitalize(splitted_name[0]),
                "assistant": ""
            }
        
        return {
            "student": self.capitalize(splitted_name[0]),
            "assistant": self.capitalize(splitted_name[1])
        }
        
    
    def start_parsing(self):
        """ Initiates the parser """
        # set the chairman name
        self.program[self.week_range]["chairman"] = self.capitalize(
            self.program[self.week_range]["chairman"]
        )
        # set the auxillary class counsellor
        self.program[self.week_range]["counsellor"] = self.capitalize(
            self.program[self.week_range]["counsellor"]
        )
        # set the opening prayer
        self.program[self.week_range]["opening_prayer"] = self.capitalize(
            self.program[self.week_range]["opening_prayer"]
        )
        # set fine fine lesson
        self.program[self.week_range]["fine_fine_lesson"] = self.capitalize(
            self.program[self.week_range]["fine_fine_lesson"]
        )
        # set fine fine things wey you See
        self.program[self.week_range]["fine_fine_things_weh_you_see"] = self.capitalize(
            self.program[self.week_range]["fine_fine_things_weh_you_see"]
        )
        # set bible reading main hall
        self.program[self.week_range]["bible_reading"] = self.capitalize(
            self.program[self.week_range]["bible_reading"]
        )
        # set bible reading second hall
        self.program[self.week_range]["bible_reading_secondhall"] = self.capitalize(
            self.program[self.week_range]["bible_reading_secondhall"]
        )
        # set preaching section
        self.preaching()
        # set di live christian life
        self.christian_life()

        return self.program

    def preaching(self):
        """ Capitalizes the names but returns a new dict object 
        for easier manipulation in the jinja template
        """
        
        # Main hall
        participants = list()

        for participant in self.program[self.week_range]["preaching"]:
            participants.append(self.preaching_capitalize(participant))

        # Second hall
        participants_sh = list()

        for participant in self.program[self.week_range]["preaching_secondhall"]:
            participants_sh.append(self.preaching_capitalize(participant))

        # replace the existing list with the new format
        self.program[self.week_range]["preaching"] = participants
        self.program[self.week_range]["preaching_secondhall"] = participants_sh

    def christian_life(self):
        """Capitalize names found in di live christian life section"""

        speakers = list()

        for speaker in self.program[self.week_range]["middle_parts"]:
            speakers.append(self.capitalize(speaker))

        # replace the existing list with the parsed names
        self.program[self.week_range]["middle_parts"] = speakers

        # Congregation bible study
        self.program[self.week_range]["cong_bible_study"] = self.preaching_capitalize(
            self.program[self.week_range]["cong_bible_study"]
        )

        # Closing prayer
        self.program[self.week_range]["closing_prayer"] = self.capitalize(
            self.program[self.week_range]["closing_prayer"]
        )



class SchedulerUtils:
    def __init__(self):
        self.paths = config.FOLDER_REFERENCES
        self.keys = ("preaching_points", "preaching_time", "middle_parts_time", "book_study_box")
    
    def get_all_parts(self, filename:str) -> list:
        with open(os.path.join(os.getcwd(), self.paths["meeting_parts"], f"{filename}.json"), "r") as f:
            blob = json.load(f)
        full_program = list()
        for _dict in blob.values():
            full_program.append(_dict)
        return full_program
    
    def save_program(self, filename:str, _dict:list) -> bool:
        blob = {}
        for _d in _dict:
            for key in _d.keys():
                blob[key] = MeetingParser(program=_d, week_range=key).start_parsing()[key]
                with open(os.path.join(os.getcwd(), self.paths["generated_programs"], filename), "w") as f:
                    json.dump(blob, f, indent=4)
        logger.info(f"Program saved: FileName > {filename}")
        return True
    
    def create_program(self, program_name: str, is_schedule: bool = False) -> str:
        """Generate a program template using the given program name and data."""
        program_data_path = os.path.join(
            os.getcwd(), self.paths["generated_programs"], f"{program_name} program.json"
        )
        meeting_parts_path = os.path.join(
            os.getcwd(), self.paths["meeting_parts"], f"{program_name}.json"
        )

        with open(program_data_path, "r", encoding="utf-8") as f:
            program_data = json.load(f)

        with open(meeting_parts_path, "r", encoding="utf-8") as f:
            meeting_parts = json.load(f)

        template_paths = {
            "program": os.path.join(
                os.getcwd(), self.paths["templates"], f"{program_name}.html"
            ),
            "schedule": os.path.join(
                os.getcwd(), self.paths["templates"], f"{program_name} scheduler.html"
            ),
        }

        for path, content in (
            (template_paths["program"], default_program_html),
            (template_paths["schedule"], program_setup),
        ):
            with open(path, "w") as f:
                f.write(content)

        preaching_time_stands = []
        middle_parts_time_stands = []
        for meeting_part in meeting_parts.values():
            preaching_time, middle_parts_time = {}, {}
            preaching_time[meeting_part["month"]], middle_parts_time[
                meeting_part["month"]
            ] = self.update_time(
                meeting_part["preaching_time"], meeting_part["middle_parts_time"]
            )
            preaching_time_stands.append(preaching_time)
            middle_parts_time_stands.append(middle_parts_time)

        try:
            template_env = Environment(
                loader=FileSystemLoader(self.paths["templates"])
            )
            template_object = template_env.get_template(
                f"{program_name}{' scheduler' if is_schedule else ''}.html"
            )
            output = template_object.render(
                programs=program_data,
                data=meeting_parts,
                zip=zip,
                zip2=enumerate,
                length=len,
                preachingt=preaching_time_stands,
                middlepartst=middle_parts_time_stands,
                tostring=str,
                toint=int,
            )
            return output
        except Exception as e:
            raise e

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
