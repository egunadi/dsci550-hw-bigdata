import pandas as pd

def joinHobbiesToPix():
    hobby_df = pd.read_csv('../data/multipart_data/clean_assignment1_data.csv')
    pixstory_df = pd.read_csv('../data/pixstory/pixstory_dx.csv')
    
    # dropping unneeded columns
    hobby_df = hobby_df.drop(columns=['Unnamed: 0', 'year'])
    
    #grouping activities by sex and age, then finding the most likely, median activity, and least likely activity
    grouped = hobby_df.groupby(['age', 'sex'])['activity']
    most_likely = grouped.apply(lambda x: x.mode()[0]).reset_index(name='most_likely_activity')
    median_activity = grouped.apply(lambda x: x.value_counts().idxmax() if len(x) > 1 else x.unique()[0]).reset_index(name='median_activity')
    least_likely = grouped.apply(lambda x: x.value_counts().idxmin()).reset_index(name='least_likely_activity')
    
    # Merge the most likely, median, and least likely activities with the original dataframe based on age and sex columns
    merged_df = pd.merge(most_likely, median_activity, on=['age', 'sex'])
    merged_df = pd.merge(merged_df, least_likely, on=['age', 'sex'])
    
    merged_df = merged_df.rename(columns={'age': 'Age'})
    merged_df = merged_df.rename(columns={'sex': 'Gender'})
    
    merged_df['Gender'] = merged_df['Gender'].str.replace('M', 'male')
    merged_df['Gender'] = merged_df['Gender'].str.replace('F', 'female')
    
    pixstory_df = pixstory_df.merge(merged_df, on=['Age','Gender'], how='left')
    
    pixstory_df.to_csv('../data/pixstory/pixstory_hobby.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    joinHobbiesToPix()


