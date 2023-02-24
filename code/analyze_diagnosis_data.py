import pandas as pd

diagnosis_filepath = '../data/sex_age_diagnosis/sex_age_diagnosis_processed.json'
pixstory_filepath = '../data/pixstory/pixstory_clean.csv'

def get_pixstory_dx_mapping():
    # import data
    diagnosis_df = pd.read_json(diagnosis_filepath)
    diagnosis_df['sex'] = diagnosis_df['sex'].str.replace('M', 'male')
    diagnosis_df['sex'] = diagnosis_df['sex'].str.replace('F', 'female')

    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')

    # process data
    diagnosis_count_df = diagnosis_df.groupby(['sex', 'age_from', 'age_to', 'diagnosis'])['diagnosis'] \
                                        .count() \
                                        .reset_index(name = 'count')

    diagnosis_count_df['count_rank'] = diagnosis_count_df.groupby(['sex', 'age_from', 'age_to'])['count'] \
                                                            .rank(ascending = False, method = 'first') \
                                                            .astype('int')

    diagnosis_top_filter_df = diagnosis_count_df.groupby(['sex', 'age_from', 'age_to'])['count_rank'] \
                                                .nsmallest(3) \
                                                .reset_index() \
                                                .set_index('level_3') # retain original index

    diagnosis_count_df = diagnosis_count_df[diagnosis_count_df.index.isin(diagnosis_top_filter_df.index)]

    pixstory_diagnosis_df = pd.merge(   pixstory_df, diagnosis_count_df, 
                                        left_on='Gender', right_on='sex'    )

    pixstory_diagnosis_df = pixstory_diagnosis_df[  (pixstory_diagnosis_df['Age'] >= pixstory_diagnosis_df['age_from']) 
                                                    & (pixstory_diagnosis_df['Age'] <= pixstory_diagnosis_df['age_to']) ]

    pixstory_primary_diagnosis_df = pixstory_diagnosis_df[pixstory_diagnosis_df['count_rank'] == 1] \
                                        .set_index('Story Primary ID')
    
    pixstory_primary_diagnosis_df = pixstory_primary_diagnosis_df['diagnosis'].reset_index(name = 'diagnosis_1')

    pixstory_secondary_diagnosis_df = pixstory_diagnosis_df[pixstory_diagnosis_df['count_rank'] == 2] \
                                        .set_index('Story Primary ID')
    
    pixstory_secondary_diagnosis_df = pixstory_secondary_diagnosis_df['diagnosis'].reset_index(name = 'diagnosis_2')

    dx_1_and_2_df = pd.merge(   pixstory_primary_diagnosis_df, pixstory_secondary_diagnosis_df,
                                on='Story Primary ID' )

    pixstory_tertiary_diagnosis_df = pixstory_diagnosis_df[pixstory_diagnosis_df['count_rank'] == 3] \
                                        .set_index('Story Primary ID')
    
    pixstory_tertiary_diagnosis_df = pixstory_tertiary_diagnosis_df['diagnosis'].reset_index(name = 'diagnosis_3')

    dx_1_2_and_3_df = pd.merge( dx_1_and_2_df, pixstory_tertiary_diagnosis_df,
                                on='Story Primary ID' )

    # payload
    return dx_1_2_and_3_df

def flag_pixstory_dx():
    pixstory_df = pd.read_csv(pixstory_filepath, delimiter=',', encoding='utf-8')
    
    dx_1_2_and_3_df = get_pixstory_dx_mapping()

    pixstory_df = pixstory_df.merge(dx_1_2_and_3_df, on='Story Primary ID')

    pixstory_df.to_csv('../data/pixstory/pixstory_dx.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    flag_pixstory_dx()
