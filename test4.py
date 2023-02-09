from Tipp3_Scrape import *
# from Global_Classes import *

import sqlite3

db_path = 'C:\\Users\\rudi\\Desktop\\Scrape\\odd_scrap.db'


class Odds:
    def __init__(self, odd_id='', global_event_id='', bookmaker='', odd_type='', odd_value=-1):
        self.odd_id = odd_id
        self.global_event_id = global_event_id
        self.bookmaker = bookmaker
        self.odd_type = odd_type
        self.odd_value = odd_value
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def insert_obj(self):
        self.cursor.execute(""" 
        INSERT INTO odds_data (odd_id, global_event_id, bookmaker, odd_type, odd) VALUES ('{}', '{}', '{}', '{}', {}) 
        ON CONFLICT(odd_id) DO UPDATE SET odd=EXCLUDED.odd""".format(self.odd_id, self.global_event_id, self.bookmaker,
                                                                     self.odd_type, self.odd_value))
        self.connection.commit()
        self.connection.close()


# clean strings
def _string_list_clean(list_dirty):
    list_clean = []
    for each in list_dirty:
        list_clean.append(each.strip())
    return list_clean


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
        bet_odds = []
        bet_labels = []
        for item in bets:
            bet_type = []
            bet_label = []
            bet_odd = []
            temp = [item.css_first("div.t3-match-details__entry-header").text()]
            for a in temp:
                bet_types.append(_string_list_clean(temp))
            label = item.css("div.t3-bet-element__label")
            for a in label:
                temps = [a.text()]
                bet_label.append(_string_list_clean(temps))
            bet = item.css("div.t3-bet-element__field")
            for a in bet:
                temps = [a.text()]
                bet_odd.append(_string_list_clean(temps))
            bet_types.append(bet_type)
            bet_odds.append(bet_odd)
            bet_labels.append(bet_label)
        print(bet_types)
        print(bet_odds)
        print(bet_labels)


def _odd_handler_tipp3(bet_type, bet_label, bet_odd):
    pass


def main():
    _get_odds()


if __name__ == '__main__':
    main()
