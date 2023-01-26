from Data_Structure_Name import *
import pandas as pd
from Settings import *
from helium import *
import datetime as dt
from selenium.webdriver.common.by import By
# seq[start:end:step]
from Odd_Ai import *
from fuzzywuzzy import fuzz

# Tennis names nicht vergessen


# Format Time
def format_time(time_input, day_delta):
    date_value = dt.date.today() + dt.timedelta(days=day_delta)
    time_value = dt.datetime.strptime(time_input, '%H:%M')
    time_value_in_format = time_value.time()
    return dt.datetime.combine(date_value, time_value_in_format)


# Check if event is within time
def hour_limit_check(date_time_list, max_delta):
    unchecked_times = []
    valid_times = []
    for each_time in date_time_list:
        splinter = each_time.split()
        if splinter[0] == "heute":
            unchecked_times.append(format_time(splinter[1], 0))
        elif splinter[0] == "morgen":
            unchecked_times.append(format_time(splinter[1], 1))
        else:
            break

    for each_time in unchecked_times:
        time_delta = each_time - dt.datetime.now()
        if time_delta.total_seconds() < max_delta:
            valid_times.append(each_time)
        else:
            break

    return valid_times


# Get sport identifier
def identify_sport(url):
    sub_url_list = ['xXXspace holderXXx', identifier_football, identifier_tennis, identifier_basketball,
                    identifier_icehockey, identifier_volleyball, identifier_handball]

    sport_id_comparer = -1
    for index, filterItem in enumerate(sub_url_list):
        subs = filterItem
        if url.find(subs) != -1:
            sport_id_comparer = index

    return sport_id_comparer


# match team names
def match_names(name_of_team, list_ai_names, sport_type, ai_sport_type_list, min_score=0):
    max_score = -1
    max_name = -1

    for x in list_ai_names:
        id_index = list_ai_names.index(x)
        compare = int(ai_sport_type_list[id_index])
        if compare == sport_type:
            score = fuzz.ratio(name_of_team, x)
            if (score > min_score) & (score > max_score):
                max_name = list_ai_names.index(x)
                max_score = score
    return max_name


# reverse Tennis last Name
def reverse_name_tennis(player_name):
    name_in_parts = []
    new_player_name = player_name
    for line in player_name.split(','):
        name_in_parts.append(line)

    if len(name_in_parts) >= 2:
        new_player_name = name_in_parts[1] + name_in_parts[0]

    return new_player_name


def calculate_diff(ai_value, tipp3_value):
    diff = 0
    if ai_value != 0 and tipp3_value != 0:
        diff = round((tipp3_value - ai_value) / ai_value * 100, 2)
        if diff < 0:
            diff = 0
    else:
        return diff
    return diff


# Make csv file with valid bets
def make_bet():
    driver = start_firefox(headless=start_browser_headless)
    namematch_fail = 0
    namematch_tried = 0
    name_failed = []
    URL_list = []
    bet_data = []

    # check_time, kelly

    try:
        meta_url_data = pd.read_csv(get_working_directory() + url_file_name)
        current_url_list = meta_url_data['Url'].values.tolist()
        ai_data = ai_odds(url_ai_json)

        for url in current_url_list:
            go_to(url)

            # Get Type of Sport
            sport_type = identify_sport(url)

            # Get all games within the next 12h
            date_time_items = find_all(S('.t3-list-entry__date'))
            date_time_list = hour_limit_check([item.web_element.text for item in date_time_items], time_filter)
            if not date_time_list:
                continue
            URL_list.append(url)

            # Get Event IDs
            event_id_tags = driver.find_elements(By.CSS_SELECTOR, 'a.t3-list-entry__more-link')

            # Get liga
            league = find_all(S('.t3-list-header__title-text'))
            league_list = [item.web_element.text for item in league]

            # Get Teams and split them
            teams = find_all(S('.t3-list-entry__player'))
            team_all = [item.web_element.text for item in teams]
            home_list = team_all[::2]
            away_list = team_all[1::2]

            # Get Base Odds
            odds = driver.find_elements(By.CSS_SELECTOR, 'div.t3-list-entry__bet-group')
            home_odds, away_odds, draw_odds = [], [], []
            if sport_type == 1 or sport_type == 2 or sport_type == 5 or sport_type == 6:
                bet_keyword = 'TXT_BASICBET'

            if sport_type == 3 or sport_type == 4:
                bet_keyword = 'TXT_2WAY_OT_PEN'

            for item in odds:
                bet_type = item.get_attribute('data-bettypekey')
                if bet_type == bet_keyword:
                    odd_text = item.text
                    odds = []
                    for text_line in odd_text.split('\n'):
                        if not isinstance(text_line, int):
                            text_line = float(text_line.replace(",", "."))
                        odds.append(text_line)

                    if len(odds) == 3 and bet_keyword == 'TXT_BASICBET':
                        home_odds.append(odds[0])
                        away_odds.append(odds[2])
                        draw_odds.append(odds[1])
                    elif len(odds) == 2 and bet_keyword == 'TXT_2WAY_OT_PEN':
                        home_odds.append(odds[0])
                        draw_odds.append(0)
                        away_odds.append(odds[1])
                    elif len(odds) == 2 and sport_type == 2:
                        home_odds.append(odds[0])
                        draw_odds.append(0)
                        away_odds.append(odds[1])
                    else:
                        home_odds.append(0)
                        away_odds.append(0)
                        draw_odds.append(0)
                        print('unequal odds')
                        continue

            # Check if Bet is valid
            for i in range(len(date_time_list)):

                event_ID_string = event_id_tags[i].get_attribute('href')
                event_ID_numeral = ''.join(filter(str.isdigit, event_ID_string))

                home_name = home_list[i]
                away_name = away_list[i]
                if sport_type == 2:
                    home_name = reverse_name_tennis(home_name)
                    away_name = reverse_name_tennis(away_name)

                ai_home_team_list, ai_away_team_list, ai_id_list = [], [], []
                ai_home_quote, ai_draw_quote, ai_away_quote = [], [], []
                for each_ai in ai_data:
                    ai_home_team_list.append(each_ai[1])
                    ai_away_team_list.append(each_ai[2])
                    ai_id_list.append(each_ai[0])
                    ai_home_quote.append(each_ai[5])
                    ai_draw_quote.append(each_ai[4])
                    ai_away_quote.append(each_ai[3])

                index_AI = -1
                namematch_tried = namematch_tried + 1
                index_AI_home = match_names(home_name, ai_home_team_list, sport_type, ai_id_list,
                                            minimum_fuzzy_accuracy)
                if index_AI_home != -1:
                    index_AI = index_AI_home
                else:
                    index_AI_away = match_names(away_name, ai_away_team_list, sport_type, ai_id_list,
                                                minimum_fuzzy_accuracy)
                    if index_AI_away != -1:

                        index_AI = index_AI_away

                if index_AI == -1:
                    namematch_fail = namematch_fail + 1
                    name_failed.append(home_name)
                    continue

                diff_home = calculate_diff(ai_home_quote[index_AI], home_odds[i])
                diff_draw = calculate_diff(ai_draw_quote[index_AI], draw_odds[i])
                diff_away = calculate_diff(ai_away_quote[index_AI], away_odds[i])

                if diff_home > 0 or diff_draw > 0 or diff_away > 0:
                    bet_data.append([sport_type, event_ID_numeral, date_time_list[i], league_list[0], home_list[i],
                                    ai_home_team_list[index_AI],  away_list[i], ai_away_team_list[index_AI], home_odds[i],
                                    draw_odds[i], away_odds[i], diff_home, diff_draw, diff_away, ai_home_quote[index_AI],
                                    ai_draw_quote[index_AI], ai_away_quote[index_AI]])
    except Exception as e:
        print('Error while scraping Data:  ' + str(e))

    try:
        kill_browser()
        dataframe_bet = pd.DataFrame(bet_data, columns=['Sport_Type', 'Event_Id', 'Date', 'League', 'Home_Team',
                                                        'AI_Home_Team', 'Away_Team', 'AI_Away_Team', 'Odds_Home',
                                                        'Odds_Draw', 'Odds_Away', 'Diff_Home', 'Diff_Draw', 'Diff_Away',
                                                        'Ai_Quote_Home', 'Ai_Quote_Draw_AI', 'Ai_Quote_Away'])

        dataframe_bet.to_csv(get_working_directory() + scrape_file_name, index=False)
        dataframe_failed = pd.DataFrame(name_failed, columns=['name'])
        dataframe_failed.to_csv(get_working_directory() + '\\failed.csv', index=False)
        if URL_list:
            dataframe_url = pd.DataFrame({'Url': URL_list})
            dataframe_url.to_csv(get_working_directory() + url_file_name, index=False)
        print(namematch_fail, namematch_tried)
    except Exception as e:
        print('Error writing scraping File:  ' + str(e))

    return namematch_fail, namematch_tried
