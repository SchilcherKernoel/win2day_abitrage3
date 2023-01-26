from datetime import datetime
from Settings import *

# returns the Name of today's Scraping directory


def get_working_directory():
    now = datetime.now()
    directory = working_directory + working_folder_name + now.strftime("%Y") + now.strftime("%m") + now.strftime("%d")
    return directory
