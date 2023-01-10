VERSION_NUMBER = "V1.0.4"
DATABASE_NAME = "congregation.sqlite"

API_LINK = "https://api.github.com/repos/hanslettthedev/nwbs-desktop/releases/latest"
SCRAPPER_LINK = "https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/{year}/{num}"

PRODUCTION = False

CHECK_FOR_UPDATES_DAY = 15

DEFAULT_FOLDER = "usr"
STORAGE_FOLDER = "bin"

LOG_PATH = STORAGE_FOLDER + "/" + "logs"

DEFAULT_FOLDER_NAMES = ["generated_programs", "modified_programs"]

STORAGE_FOLDER_NAMES = ["meeting_parts", "templates", 
"years", "local_storage", "logs"]

FOLDER_REFERENCES = {
    "database": STORAGE_FOLDER + "/local_storage",
    "templates": STORAGE_FOLDER + "/templates",
    "meeting_parts": STORAGE_FOLDER + "/meeting_parts",
    "years": STORAGE_FOLDER + "/years",
    "generated_programs": DEFAULT_FOLDER + "/generated_programs",
    "modified_programs": DEFAULT_FOLDER + "/modified_programs",
}

