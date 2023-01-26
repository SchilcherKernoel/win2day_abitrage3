from Data_Structure_Name import *
import os
from Settings import *
import pandas as pd
import requests
from bs4 import BeautifulSoup


def make_url():
    try:
        working_name = get_working_directory()+url_file_name
        if os.path.isdir(working_name):
            print('Directory already exists')
            return 1

        # Fetch XML
        html = requests.get(tipp3_sitemap_url)
        soup = BeautifulSoup(html.text, "lxml")

        # Get url only. Urls have loc tag
        urls_from_xml = []
        loc_tags = soup.find_all('loc')
        for loc in loc_tags:
            urls_from_xml.append(loc.get_text())

        # Filter make a list with all urls that contain the  desired content
        filter_list = [identifier_football, identifier_tennis, identifier_basketball, identifier_icehockey,
                       identifier_volleyball, identifier_handball]

        # if url contains an identifier write to res
        res = []
        for index, filterItem in enumerate(filter_list):
            subs = filterItem
            for i in urls_from_xml:
                if i.find(subs) != -1:
                    res.append(i)

        # Save the Url List to csv
        df = pd.DataFrame(data={"Url": res})
        directory = get_working_directory()
        df.to_csv(directory + url_file_name, sep=',', index=False)

        print('Url files produced successfully')
        return 1

    except Exception as e:
        print('Error while producing the URL files: ' + str(e))
        return 'Error while producing the URL files: ' + str(e)

# make_url()