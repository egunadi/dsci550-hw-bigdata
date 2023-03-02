from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path 
import glob
import pandas as pd
from collections import defaultdict

sarc_directory_path = "../data/sarcasm/data-sarc-sample/sarc"
pixstory_filepath = "../data/pixstory/pixstory_hate.csv"

def get_terms(directory_path: str) -> list:
    text_files = glob.glob(f"{directory_path}/*.txt")
    text_titles = [Path(text).stem for text in text_files]

    tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english')
    tfidf_vector = tfidf_vectorizer.fit_transform(text_files)
    # all tokens converted to lowercase by default
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

    tfidf_df = pd.DataFrame(tfidf_vector.toarray(), 
                            index=text_titles, 
                            columns=tfidf_vectorizer.get_feature_names_out())

    tfidf_df =  tfidf_df.stack() \
                        .reset_index() \
                        .rename(columns={        0: 'score', 
                                        'level_0': 'document',
                                        'level_1': 'term', 
                                        'level_2': 'term'   })

    # scrub data
    tfidf_df = tfidf_df[(tfidf_df['score'] != 0) & (tfidf_df['score'] != 1)]

    # for every file, grab top 1 TF-IDF term with the best scores
    tfidf_df =  tfidf_df.sort_values(by=['document','score'], ascending=[True,False]) \
                        .groupby(['document']) \
                        .head(1)

    # remove all terms with TF-IDF scores less than 0.6
    tfidf_df = tfidf_df[tfidf_df['score'] >= 0.6]

    # payload
    tfidf_list = tfidf_df['term'].unique().tolist()

    with open('../data/sarcasm/sarc_keywords.txt', mode='w', encoding='utf-8') as file:
        for word in tfidf_list:
            file.write(f"{word}\n")

    return tfidf_list

def split_pixstory_words():
    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
    pixstory_df.columns = pixstory_df.columns.str.replace(' ', '')
    pixstory_df['Narrative'] = pixstory_df['Narrative'].astype(str)

    narrative_dict = defaultdict(dict)

    for pixstory in pixstory_df.itertuples():
        narrative_dict[pixstory.StoryPrimaryID] = pixstory.Narrative.split() 

    narrative_dict = dict(narrative_dict)
    return narrative_dict

def get_pixstory_sarc_mapping():
    sarc_terms = get_terms(sarc_directory_path)
    narrative_dict = split_pixstory_words()

    sarc_count_dict = defaultdict(dict)

    for StoryPrimaryID, words in narrative_dict.items():
        # if more than 1 sarcastic word is found, mark as sarcastic
        if len(set(sarc_terms).intersection(set(words))) > 1:
            sarc_count_dict[StoryPrimaryID] = True
        else:
            sarc_count_dict[StoryPrimaryID] = False

    return dict(sarc_count_dict)

def flag_pixstory_sarc():
    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
    
    sarc_count_dict = get_pixstory_sarc_mapping()

    sarc_count_df = pd.DataFrame(sarc_count_dict.items(), columns=['Story Primary ID', 'sarc'])

    # print(sarc_count_df.head(5))
    pixstory_df = pixstory_df.merge(sarc_count_df, on='Story Primary ID', how='left')

    pixstory_df.to_csv('../data/pixstory/pixstory_sarc.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    flag_pixstory_sarc()
