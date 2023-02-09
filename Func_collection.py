from fuzzywuzzy import fuzz
import datetime as dt
from selectolax.parser import HTMLParser
import httpx



def normalize_time():
    pass


# Convert Tulpe to string
def convert_tuple(tup):
    string_ = ''
    for item in tup:
        string_ = string_ + item
    return string_


def convert_tuple_list(tuple_list):
    result_list = []
    for each_tulpe in tuple_list:
        string_ = ''
        for item in each_tulpe:
            string_ = string_ + item
        result_list.append(string_)
    return result_list


# Makes a global ID for the Database
def make_global_id(home, away, date):
    home_cleaned = home.strip(", ")
    away_cleaned = away.strip(", ")
    global_id_system = home_cleaned + '_' + away_cleaned + '_' + str(date)
    return global_id_system


# Check if event is within the desired delta. returns list of time date
def max_time_delta_check(date_time_list, max_delta):
    valid_times = []
    for each_time in date_time_list:
        time_delta = each_time - dt.datetime.now()
        if time_delta.total_seconds() < max_delta:
            valid_times.append(each_time)
        else:
            break
    return valid_times


# Gets the index of list that most closely represents the string
def match_names(name, compare_list, min_score):
    max_score = -1
    max_name = -1
    for x in compare_list:
        score = fuzz.ratio(name, x)
        if (score > min_score) & (score > max_score):
            max_name = compare_list.index(x)
            max_score = score
    return max_name


# returns HTML of website
def get_html(url):
    resp = httpx.get(url)
    return HTMLParser(resp.text)