import pandas as pd
from Settings import *
from Data_Structure_Name import *


def demark_bets():
    try:
        list_emtpy = []
        df1 = pd.DataFrame(list_emtpy, columns=['Event_Id'])
        df1.to_csv(get_working_directory() + marked_bets_name, index=False)
    except Exception as e:
        print('Error while trying to bundle slips:  ' + str(e))