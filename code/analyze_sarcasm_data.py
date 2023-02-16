from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path 
import glob
import pandas as pd

sarc_directory_path = "data/sarcasm/data-sarc-sample/sarc"
notsarc_directory_path = "data/sarcasm/data-sarc-sample/notsarc"
pixstory_filepath = "data/pixstory/pixstory_clean.csv"

def get_terms(directory_path: str) -> list:
    text_files = glob.glob(f"{directory_path}/*.txt")
    text_titles = [Path(text).stem for text in text_files]

    tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english')
    tfidf_vector = tfidf_vectorizer.fit_transform(text_files)

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

    # for every file, grab top 3 TF-IDF terms with the best scores
    tfidf_df =  tfidf_df.sort_values(by=['document','score'], ascending=[True,False]) \
                        .groupby(['document']) \
                        .head(3)
    
    return tfidf_df['term'].unique().tolist()

def flag_pixstory_sarc():
    sarc_terms = get_terms(sarc_directory_path)
    notsarc_terms = get_terms(notsarc_directory_path)

    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')

    return pixstory_df

df = flag_pixstory_sarc()

print(df)







