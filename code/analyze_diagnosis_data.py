import pandas as pd

diagnosis_filepath = '../data/sex_age_diagnosis/sex_age_diagnosis_processed.json'
pixstory_filepath = '../data/pixstory/pixstory_clean.csv'

# import data
diagnosis_df = pd.read_json(diagnosis_filepath)
pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
pixstory_df.columns = pixstory_df.columns.str.replace(' ', '')

# process data
diagnosis_agg_df = diagnosis_df.groupby(['sex', 'age_group', 'diagnosis'])['diagnosis'] \
                                .count() \
                                .reset_index(name = 'count') \
                                .sort_values(['sex', 'age_group', 'count'], ascending = False)

diagnosis_agg_df['count_rank'] = diagnosis_agg_df.groupby(['sex', 'age_group'])['count'] \
                                                    .rank(ascending = False, method = 'first') \
                                                    .astype('int')

diagnosis_top_filter_df = diagnosis_agg_df.groupby(['sex', 'age_group'])['count_rank'] \
                                            .nsmallest(3) \
                                            .reset_index() \
                                            .set_index('level_2')

diagnosis_agg_df = diagnosis_agg_df[diagnosis_agg_df.index.isin(diagnosis_top_filter_df.index)]

print(diagnosis_agg_df.to_string())


# if __name__ == '__main__':
#     analyze_data()