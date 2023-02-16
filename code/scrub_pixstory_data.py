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

    pixstory_clean_df = indexed_pixstory_df[~indexed_pixstory_df.index.isin(pk_duplicates_df.index)]

    # export data
    pixstory_clean_df.to_csv('../data/pixstory/pixstory_clean.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    scrub_pixstory_data()
