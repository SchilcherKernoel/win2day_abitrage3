import urllib.request
import json


# Get Data of Ai
def get_ai_data(url):
    # Open url and get data as json
    with urllib.request.urlopen(url) as url:
        ai_site_json = json.load(url)

    # iterate through all json items and save to list
    ai_data = []
    for items in ai_site_json['pageProps']['data']:
        temp_list = [items['sport_id'], items['home'], items['away'], float(items['odds_moneyline']['away'])]
        try:
            temp_list.append(float(items['odds_moneyline']['draw']))
        except:
            temp_list.append(0)
        temp_list.append(float(items['odds_moneyline']['home']))
        ai_data.append(temp_list)
    return ai_data

# a = ai_odds('https://www.sports-ai.dev/_next/data/5ApUmg_Xnzl-7Z3cAGbVH/predictions.json')
