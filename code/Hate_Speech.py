#import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

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

# the following code was done with Eben's guidance
def import_pixstory():
    pixstory_df = pd.read_csv('../data/pixstory/pixstory.csv', delimiter=',', encoding='utf-8')
    pixstory_df.columns = pixstory_df.columns.str.replace(' ', '')
    pixstory_df['Narrative'] = pixstory_df['Narrative'].astype(str)

    narrative_dict = defaultdict(dict)

    for pixstory in pixstory_df.itertuples():
        narrative_dict[pixstory.StoryPrimaryID] = pixstory.Narrative.split()

    narrative_dict = dict(narrative_dict)
    return narrative_dict


def get_pixstory_hate():
    GLAAD_list, ADL_list = gen_flagged_words()
    narrative_dict = import_pixstory()

    GLAAD_count_dict = defaultdict(dict)

    for StoryPrimaryID, words in narrative_dict.items():
        if len(set(GLAAD_list).intersection(set(words))) >= 1:
            GLAAD_count_dict[StoryPrimaryID] = True
        else:
            GLAAD_count_dict[StoryPrimaryID] = False

    ADL_count_dict = defaultdict(dict)

    for StoryPrimaryID, words in narrative_dict.items():
        if len(set(ADL_list).intersection(set(words))) >= 1:
            ADL_count_dict[StoryPrimaryID] = True
        else:
            ADL_count_dict[StoryPrimaryID] = False

    return dict(GLAAD_count_dict), dict(ADL_count_dict)


def flag_pixstory_hate():
    pixstory_df = pd.read_csv('../data/pixstory/pixstory.csv', delimiter=',', encoding='utf-8')

    GLAAD_count_dict, ADL_count_dict = get_pixstory_hate()

    GLAAD_count_df = pd.DataFrame(GLAAD_count_dict.items(), columns=['Story Primary ID', 'GLAAD'])
    ADL_count_df = pd.DataFrame(ADL_count_dict.items(), columns=['Story Primary ID', 'ADL'])

    pixstory_df = pixstory_df.merge(GLAAD_count_df, on='Story Primary ID')
    pixstory_df = pixstory_df.merge(ADL_count_df, on='Story Primary ID')

    pixstory_df.to_csv('../data/pixstory/pixstory_hate.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    flag_pixstory_hate()

flag_pixstory_hate()


