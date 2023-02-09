import sqlite3

db_path = 'C:\\Users\\rudi\\Desktop\\Scrape\\odd_scrap.db'


class Odds:
    def __init__(self, global_event_id='', bookmaker='', odd_type='', odd=-1):
        self.global_event_id = global_event_id
        self.bookmaker = bookmaker
        self.odd_type = odd_type
        self.odd = odd
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor

    def insert_obj(self):
        self.cursor.execute("""INSERT OR REPLACE INTO odds VALUES
                ('{}', '{}', '{}', {})
                """.format(self.global_event_id, self.bookmaker, self.odd_type, self.odd))
        self.connection.commit()
        self.connection.close()


class GlobalMetadata:
    def __init__(self, global_event_id='', league_name='', global_sport_id=-1, event_time_date=-1,
                 home_name='', away_name=''):
        self.global_event_id = global_event_id
        self.league_name = league_name
        self.global_sport_id = global_sport_id
        self.event_time_date = event_time_date
        self.home_name = home_name
        self.away_name = away_name
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def load_all(self):
        self.cursor.execute("""
               SELECT * FROM global_meta_data
               """)
        result = self.cursor.fetchall()
        return result

    def load_all_with_date_sportid(self, date, sport_id):
        self.cursor.execute("""
                SELECT * FROM global_meta_data
                WHERE event_time_date = '{}' AND global_sport_id = {}
                """.format(date, sport_id))
        result = self.cursor.fetchall()
        return result

    def load_obj_with_eventid(self, global_event_id):
        self.cursor.execute("""
               SELECT * FROM global_meta_data
               WHERE global_event_id = {}
               """.format(global_event_id))

        result = self.cursor.fetchone()
        if result is None:
            result = [-1, -1, -1, -1, -1, -1, -1]
        self.global_event_id = result[0]
        self.league_name = global_event_id
        self.global_sport_id = result[2]
        self.event_time_date = result[3]
        self.home_name = result[4]
        self.away_name = result[5]

    def load_home_with_date_sportid(self, date, sport_id):
        self.cursor.execute("""
                SELECT home_name FROM global_meta_data
                WHERE event_time_date = '{}' AND global_sport_id = {}
                """.format(date, sport_id))
        result = self.cursor.fetchall()
        return result

    def load_away_with_date_sportid(self, date, sport_id):
        self.cursor.execute("""
                SELECT away_name FROM global_meta_data
                WHERE event_time_date = '{}' AND global_sport_id = {}
                """.format(date, sport_id))
        result = self.cursor.fetchall()
        return result

    def load_eventid_with_home_away_date_sport(self, home, away, date, sport_id):
        self.cursor.execute("""
                       SELECT global_event_id FROM global_meta_data
                       WHERE home_name = '{}' AND away_name = '{}' AND event_time_date = '{}' AND global_sport_id = {}
                       """.format(home, away, date, sport_id))
        result = self.cursor.fetchone()
        return result

    def add_new(self):
        self.cursor.execute("""
               INSERT INTO global_meta_data VALUES
               ('{}', '{}', {}, '{}', '{}', '{}')
               """.format(self.global_event_id, self.league_name, self.global_sport_id, self.event_time_date,
                          self.home_name, self.away_name))
        self.connection.commit()
        self.connection.close()
