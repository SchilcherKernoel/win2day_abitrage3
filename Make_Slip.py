import pandas as pd
from Settings import *
from Data_Structure_Name import *


def make_slip(min_diff, max_diff, min_qoute, max_qoute):
    try:
        # Get Scrape Date
        scrape_dataframe = pd.read_csv(get_working_directory() + scrape_file_name)
        scrape_list = scrape_dataframe.values.tolist()

        # Filter all that don't make the requirement
        for event_check in scrape_list:
            quote_i = 6
            while quote_i <= 11:
                if event_check[quote_i] < min_qoute or event_check[quote_i] > max_qoute:
                    event_check[quote_i], event_check[quote_i+6] = 0, 0

                if event_check[quote_i+6] < min_diff or event_check[quote_i+6] > max_diff:
                    event_check[quote_i], event_check[quote_i+6] = 0, 0
                quote_i = quote_i + 1

        # Delete empty rows
        remove_list = []
        for event_check_delete in scrape_list:
            quote_i = 6
            checker = False
            while quote_i <= 11:
                if event_check_delete[quote_i] > 1:
                    checker = True
                quote_i = quote_i + 1

            if not checker:
                remove_list.append(event_check_delete)

        for event_delete in remove_list:
            scrape_list.remove(event_delete)

        print_dataframe = pd.DataFrame(scrape_list, columns=['Event_Id', 'League', 'Home_Team', 'AI_Home_Team',
                                                             'Away_Team', 'AI_Away_Team', 'Quote_Home', 'Quote_Draw',
                                                             'Quote_Away', 'Quote_1X', 'Quote_12', 'Quote_2X',
                                                             'Diff_Home', 'Diff_Draw', 'Diff_Away', 'Diff_1X',
                                                             'Diff_12', 'Diff_2X', 'Ai_Quote_Home', 'Ai_Quote_Draw_AI',
                                                             'Ai_Quote_Away', 'Ai_Quote_1X', 'Ai_Quote_12',
                                                             'Ai_Quote_2X'])

        print_dataframe.to_csv(get_working_directory() + slip_file_name, index=False)
        return 'Slips made successfully'
    except Exception as e:
        print('Error writing scraping File:  ' + str(e))
        return 'Error writing scraping File:  ' + str(e)


# make_slip(2, 100, 1, 3)
