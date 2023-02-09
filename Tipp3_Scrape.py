import requests
from bs4 import BeautifulSoup
from helium import *
# import datetime as dt
from selenium.webdriver.common.by import By
# import sqlite3
from Global_Classes import *
from Func_collection import *
import httpx
from selectolax.parser import HTMLParser
# Current version only today's and tomorrow's games

db_path = 'C:\\Users\\rudi\\Desktop\\Scrape\\odd_scrap.db'
bet_url_pre = 'https://www.tipp3.at/sportwetten/eventdetails?eventID='
bet_url_post = '&caller=PRO&frame'


class Tipp3Metadata:
    def __init__(self, global_event_id='', tipp3_event_id=-1, tipp3_sport_id=-1, tipp3_event_time_date='',
                 tipp3_home='', tipp3_away='', tipp3_league=''):
        self.global_event_id = global_event_id
        self.tipp3_event_id = tipp3_event_id
        self.tipp3_sport_id = tipp3_sport_id
        self.tipp3_event_time_date = tipp3_event_time_date
        self.tipp3_home = tipp3_home
        self.tipp3_away = tipp3_away
        self.tipp3_league = tipp3_league
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def load_with_tipp3_id(self, tipp3_event_id):
        self.cursor.execute("""
        SELECT * FROM tipp3_meta_data
        WHERE tipp3_event_id = {}
        """.format(tipp3_event_id))
        result = self.cursor.fetchone()

        if result is None:
            result = [-1, -1, -1, -1, -1, -1, -1]
        self.global_event_id = result[0]
        self.tipp3_event_id = tipp3_event_id
        self.tipp3_sport_id = result[2]
        self.tipp3_event_time_date = result[3]
        self.tipp3_home = result[4]
        self.tipp3_away = result[5]
        self.tipp3_league = result[6]

    def add_new(self):
        self.cursor.execute("""
        INSERT INTO tipp3_meta_data VALUES
        ('{}', {}, {}, '{}', '{}', '{}', '{}')
        """.format(self.global_event_id, self.tipp3_event_id, self.tipp3_sport_id, self.tipp3_event_time_date,
                   self.tipp3_home, self.tipp3_away, self.tipp3_league))
        self.connection.commit()
        self.connection.close()

    def load_all_ids(self):
        self.cursor.execute("""
               SELECT tipp3_event_id FROM tipp3_meta_data
               """)
        result = self.cursor.fetchall()
        return result


# Get sport identifier
def _identify_sport(url, identifier_url):
    sport_id_comparer = -1
    for index, filterItem in enumerate(identifier_url):
        subs = filterItem
        if url.find(subs) != -1:
            sport_id_comparer = index
    return sport_id_comparer


# Format Time
def _format_time(time_input, day_delta):
    date_value = dt.date.today() + dt.timedelta(days=day_delta)
    time_value = dt.datetime.strptime(time_input, '%H:%M')
    time_value_in_format = time_value.time()
    return dt.datetime.combine(date_value, time_value_in_format)


# Check if event is within time
def _hour_limit_check(date_time_list, max_delta):
    unchecked_times = []
    for each_time in date_time_list:
        splinter = each_time.split()
        if splinter[0] == "heute":
            unchecked_times.append(_format_time(splinter[1], 0))
        elif splinter[0] == "morgen":
            unchecked_times.append(_format_time(splinter[1], 1))
        else:
            break
    valid_times = max_time_delta_check(unchecked_times, max_delta)
    return valid_times


# Got to sitemap end get all url valid for scraping
def _get_url_for_scrape(identifier, sitemap_url):
    try:
        # Fetch XML
        html = requests.get(sitemap_url)
        soup = BeautifulSoup(html.text, "lxml")

        # Get url only. Urls have loc tag
        urls_from_xml = []
        loc_tags = soup.find_all('loc')
        for loc in loc_tags:
            urls_from_xml.append(loc.get_text())

        # if url contains an identifier write to res
        url_list = []
        for index, filterItem in enumerate(identifier):
            subs = filterItem
            for i in urls_from_xml:
                if i.find(subs) != -1:
                    url_list.append(i)
        return url_list

    except Exception as e:
        print('Error while producing the URL files: ' + str(e))
        return -1


# Make the operations for adding to database
def _write_to_database(event_id, home, away, sport_type, date_time, league):
    obj_t3 = Tipp3Metadata()
    obj_t3.load_with_tipp3_id(event_id)

    if obj_t3.global_event_id == -1:
        obj_glob = GlobalMetadata()
        home_list_glob = convert_tuple_list(obj_glob.load_home_with_date_sportid(date_time, sport_type))
        away_list_glob = convert_tuple_list(obj_glob.load_away_with_date_sportid(date_time, sport_type))

        index_glob = match_names(home, home_list_glob, 70)
        if index_glob == -1:
            index_glob = match_names(away, away_list_glob, 70)
            if index_glob == -1:
                # no matches in databases new global and tipp3 database entry
                new_global_id = make_global_id(home, away, date_time)

                obj_t3 = Tipp3Metadata(new_global_id, event_id, sport_type, date_time, home, away, league)
                obj_t3.add_new()

                obj_glob = GlobalMetadata(new_global_id, league, sport_type, date_time, home, away)
                obj_glob.add_new()
                return

        # a match in the database make only bew tipp 3 entry
        global_id = obj_glob.load_eventid_with_home_away_date_sport(home_list_glob[index_glob],
                                                                    away_list_glob[index_glob],
                                                                    date_time, sport_type)

        obj_t3 = Tipp3Metadata(convert_tuple(global_id), event_id, sport_type, date_time, home, away,
                               league)
        obj_t3.add_new()


# Get all the bet metadata
def _get_bet_metadata(max_time_till_event, identifier_url, sitemap_url):
    url_list = _get_url_for_scrape(identifier_url, sitemap_url)
    if type(url_list) != list:
        return -1

    driver = start_firefox()
    for url in url_list:
        try:
            go_to(url)
        except Exception as e:
            print('Error while trying to open url for ID Scrape:  ' + str(e))

        try:
            # Get all games within the next 12h
            date_time_items = find_all(S('.t3-list-entry__date'))
            date_time_list = _hour_limit_check([item.web_element.text for item in date_time_items], max_time_till_event)
            if not date_time_list:
                continue

            # Get Event IDs
            event_id_tags = driver.find_elements(By.CSS_SELECTOR, 'a.t3-list-entry__more-link')
            if not event_id_tags:
                continue

            # Get Teams and split them
            teams = find_all(S('.t3-list-entry__player'))
            team_all = [item.web_element.text for item in teams]
            home_list = team_all[::2]
            away_list = team_all[1::2]

            # Get liga
            league = find_all(S('.t3-list-header__title-text'))
            league_list = [item.web_element.text for item in league]

            # Get Sport type
            sport_type = _identify_sport(url, identifier_url)

            # Check if Bet is valid and in Database. If not write to database
            for i in range(len(date_time_list)):
                event_ID_link = event_id_tags[i].get_attribute('href')
                event_ID_string = event_ID_link.replace("www.tipp3.at", "")
                event_ID_numeral = int(''.join(filter(str.isdigit, event_ID_string)))
                _write_to_database(event_ID_numeral, home_list[i], away_list[i], sport_type, str(date_time_list[i]),
                                   league_list[0])
        except Exception as e:
            print('Error while trying to scrape for ID Scrape:  ' + str(e))
    kill_browser()


# Get all odds
def _get_odds():

    tipp3_obj = Tipp3Metadata()
    event_id_list = tipp3_obj.load_all_ids()

    # loads each detailed betting site corresponding to id
    for event_id in event_id_list:
        bet_id = ''.join(map(str, event_id))
        url = bet_url_pre+bet_id+bet_url_post
        html = get_html(url)

        bets = html.css("div.t3-match-details__entry")
        bet_types = []
        bet_dsic = []
        beT_odd = []
        for item in bets:
            bet_types.append(item.css_first("div.t3-match-details__entry-header").text())
            dsic = item.css("div.t3-bet-element__label")
            for a in dsic:
                bet_dsic.append(a.text())
            bet = item.css("div.t3-bet-element__field")
            for a in bet:
                beT_odd.append(a.text())
        print(bet_types)


# Scrapes Data of Tipp3 Bets to database (max time in seconds)
def scrape_tipp_3(sitemap_url, identifier_url, max_time_till_event):
    try:
        _get_bet_metadata(max_time_till_event, identifier_url, sitemap_url)
    except Exception as e:
        print('Critical Error while trying to scrape metadata:  ' + str(e))

    try:
        _get_odds()
    except Exception as e:
        print('Critical Error while trying to scrape odds:  ' + str(e))


def main():
    # pass
    # Url list has to be in right oder
    sub_url_list = ['xXXspace holderXXx', 'https://www.tipp3.at/sport/fussballX/', 'https://www.tipp3.at/sport/tennisX/',
                    'https://www.tipp3.at/sport/basketballX/', 'https://www.tipp3.at/sport/eishockeyX/',
                    'https://www.tipp3.at/sport/volleyballX/', 'https://www.tipp3.at/sport/handballX/']
    scrape_tipp_3('https://www.tipp3.at/sitemap.xml', sub_url_list, 43200)


if __name__ == '__main__':
    main()
