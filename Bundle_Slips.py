from Data_Structure_Name import *
import pandas as pd
from os import path


def bundle_slips():
    try:
        df = pd.read_csv(get_working_directory() + slip_file_name)
        data_list = df.values.tolist()

        if not path.exists(get_working_directory() + marked_bets_name):
            list_emtpy = []
            df1 = pd.DataFrame(list_emtpy, columns=['Event_Id'])
            df1.to_csv(get_working_directory() + marked_bets_name, index=False)

        df2 = pd.read_csv(get_working_directory() + marked_bets_name)
        marked_list = df2['Event_Id'].values.tolist()

        print_list = []
        for bet in data_list:
            if bet[0] not in marked_list:
                print_list.append(bet)
                marked_list.append(bet[0])

        df3 = pd.DataFrame(marked_list, columns=['Event_Id'])
        df3.to_csv(get_working_directory() + marked_bets_name, index=False)

        df4 = pd.DataFrame(print_list, columns=['Event_Id', 'League', 'Home_Team', 'AI_Home_Team', 'Away_Team',
                                                'AI_Away_Team', 'Quote_Home', 'Quote_Draw', 'Quote_Away',
                                                'Quote_1X', 'Quote_12', 'Quote_2X', 'Diff_Home', 'Diff_Draw',
                                                'Diff_Away', 'Diff_1X', 'Diff_12', 'Diff_2X', 'Ai_Quote_Home',
                                                'Ai_Quote_Draw_AI', 'Ai_Quote_Away', 'Ai_Quote_1X', 'Ai_Quote_12',
                                                'Ai_Quote_2X'])

        df4.to_csv(get_working_directory() + bundle_bet_name, index=False)
        return print_list
    except Exception as e:
        print('Error while trying to bundle slips:  ' + str(e))
