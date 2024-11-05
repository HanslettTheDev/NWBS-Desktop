VERSION_NUMBER = "V1.0.7"
DATABASE_NAME = "congregation.sqlite"

API_LINK = "https://api.github.com/repos/hanslettthedev/nwbs-desktop/releases/latest"

NEW_LINK = "https://www.jw.org/wes-x-pgw/library/jw-meeting-workbook/{monthx}-{year}-mwb/Life-and-Preaching-Meeting-Workbook-for-{current_month}-{week}-{year}/"

PRODUCTION = True

CHECK_FOR_UPDATES_DAY = 15

STORAGE_FOLDER = "app_data"

LOG_FILE = "nwbs.log"

LOG_PATH = STORAGE_FOLDER + "/" + "logs"

STORAGE_FOLDER_NAMES = [
    "meeting_parts", 
    "templates",
    "local_storage", 
    "logs", 
    "generated_programs", 
    "modified_programs"
]

FOLDER_REFERENCES = {
    "database": STORAGE_FOLDER + "/local_storage",
    "templates": STORAGE_FOLDER + "/templates",
    "meeting_parts": STORAGE_FOLDER + "/meeting_parts",
    "generated_programs": STORAGE_FOLDER + "/generated_programs",
    "modified_programs":  STORAGE_FOLDER + "/modified_programs",
}

