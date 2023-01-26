from Data_Structure_Name import *
import os

# Makes the directory where all the scraping will take place


def make_data_structure():
    try:
        directory = get_working_directory()
        if os.path.isdir(directory):
            print('Directory already exists')
            return 1
        else:
            os.makedirs(directory)
            print('Directory created successfully:' + directory)
        return 1

    except Exception as e:
        print('Error while creating Directory:' + str(e))
        return 'Error while creating Directory:' + str(e)
