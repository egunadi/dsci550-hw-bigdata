import pandas as pd

def scrub_pixstory_data():
    pixstory_filepath = "../data/pixstory/pixstory.csv"

    # import data
    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
    indexed_pixstory_df = pixstory_df.set_index(['Story Primary ID', 'Story ID'])
        
    # scrub data
    pk_counts_df = pixstory_df.groupby(['Story Primary ID', 'Story ID'])['Narrative'] \
                                .nunique() \
                                .reset_index(name = 'count') 
    pk_duplicates_df = pk_counts_df[pk_counts_df['count'] > 1].set_index(['Story Primary ID', 'Story ID'])

    # only 3 [Story Primary ID]-[Story ID] combinations have more than one [Narrative]
    # these seem to be outliers and can probably be removed to clean the data
    pixstory_clean_df = indexed_pixstory_df[~indexed_pixstory_df.index.isin(pk_duplicates_df.index)].reset_index()

    # per data exploration, no [Story Primary ID] has more than one distinct [Story ID]
    # hence duplicate [Story IDs] can be dropped and [Story Primary ID] can be the sole PK 
    pixstory_clean_df.drop_duplicates(subset='Story Primary ID', keep="last")

    # export data
    pixstory_clean_df.to_csv('../data/pixstory/pixstory_clean.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    scrub_pixstory_data()
