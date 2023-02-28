#import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

# parse websites
def web_parsing(URL, para, attr):

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    all_headers = soup.find_all(para, attr)

    hate_list = []
    for header in all_headers:
        header_contents = header.text
        hate_list.append(header_contents)

    return hate_list

# generate hate speech list
def gen_flagged_words():

    # generating from GLAAD
    URL = "https://www.glaad.org/hate-speech-listing"
    para = "h3"
    attr = ""
    hate_list = web_parsing(URL, para, attr)
    #remove first 2 because they are headers
    GLAAD_list = hate_list[2:]

    # generating from ADL
    para = "span"
    attr = {"class": "field field--name-title field--type-string field--label-hidden"}
    ADL_list = []

    # going through each page
    for i in range(0, 10):
        URL = "https://www.adl.org/resources/hate-symbols/search?keywords=&sort_by=title&page=" + str(i)
        hate_list = web_parsing(URL, para, attr)
        ADL_list.extend(hate_list)

    # removing all hand signs, as they are visual (not words)
    for i in ADL_list:
        if "hand sign" in i:
            ADL_list.remove(i)

    return GLAAD_list, ADL_list


def pixstory_data():
    # Import pixstory data
    pixstory_df = pd.read_csv('.../data/pixstory/pixstory.csv', delimiter=',', encoding='utf-8')
    narrative = pixstory_df.loc[:,"Narrative"]

    GLAAD_hate_speech = False

    i = 1

    GLAAD_list, ADL_list = gen_flagged_words()
    while i in narrative:
        if any(GLAAD_list) in i.getkey:
            GLAAD_hate_speech[i] = True
        else:
            GLAAD_hate_speech[i] = False

        i = i + 1

    return GLAAD_hate_speech

k = pixstory_data()
print(k)


