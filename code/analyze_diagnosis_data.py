import pandas as pd

diagnosis_filepath = '../data/sex_age_diagnosis/sex_age_diagnosis_processed.json'
pixstory_filepath = '../data/pixstory/pixstory_clean.csv'

# import data
diagnosis_df = pd.read_json(diagnosis_filepath)

pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
pixstory_df.columns = pixstory_df.columns.str.replace(' ', '')
pixstory_df['Gender'] = pixstory_df['Gender'].str.replace('male', 'M')
pixstory_df['Gender'] = pixstory_df['Gender'].str.replace('female', 'F')

# print(diagnosis_df)

# process data
diagnosis_count_df = diagnosis_df.groupby(['sex', 'age_from', 'age_to', 'diagnosis'])['diagnosis'] \
                                    .count() \
                                    .reset_index(name = 'count')

# print(diagnosis_count_df.to_string())

diagnosis_count_df['count_rank'] = diagnosis_count_df.groupby(['sex', 'age_from', 'age_to'])['count'] \
                                                        .rank(ascending = False, method = 'first') \
                                                        .astype('int')

# print(diagnosis_count_df)

diagnosis_top_filter_df = diagnosis_count_df.groupby(['sex', 'age_from', 'age_to'])['count_rank'] \
                                            .nsmallest(3) \
                                            .reset_index() \
                                            .set_index('level_3') # retain original index

# print(diagnosis_top_filter_df)

diagnosis_count_df = diagnosis_count_df[diagnosis_count_df.index.isin(diagnosis_top_filter_df.index)]

# print(diagnosis_count_df.to_string())

# pixstory_diagnosis_df = pd.merge(pixstory_df.assign(key=0), diagnosis_count_df.assign(key=0), on='key').drop('key', axis=1)
pixstory_diagnosis_df = pd.merge(   pixstory_df, diagnosis_count_df, 
                                    left_on='Gender', right_on='sex'    )

# print(pixstory_diagnosis_df.columns)

pixstory_diagnosis_df = pixstory_diagnosis_df[  (pixstory_diagnosis_df['Age'] >= pixstory_diagnosis_df['age_from']) 
                                                & (pixstory_diagnosis_df['Age'] <= pixstory_diagnosis_df['age_to']) ]

# print(pixstory_diagnosis_df.head(5).to_string())

pixstory_primary_diagnosis_df = pixstory_diagnosis_df[pixstory_diagnosis_df['count_rank'] == 1].set_index('StoryPrimaryID')

print(pixstory_primary_diagnosis_df.head(5))

# if __name__ == '__main__':
#     analyze_data()