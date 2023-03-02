import pandas as pd

anxiety_depression_path = '../data/Anxiety_Depression_Index/Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv'

def read_AD_data():
    results = pd.read_csv(anxiety_depression_path)
    anxiety_depression = results
    return anxiety_depression

def clean_AD_data():
    anxiety_depression = read_AD_data()
    anxiety_depression = anxiety_depression.query('State == "United States" & Group == ["By Age", "By Sex"]')
    anxiety_depression = anxiety_depression[['Indicator', 'Group', 'Subgroup', 'Value']]
    anxiety_depression['Value'] = anxiety_depression['Value'].astype(float)
    anxiety_depression = anxiety_depression.groupby(['Indicator', 'Group', 'Subgroup']).agg({'Value': 'mean'}).reset_index()
    pivot_anxiety_depression = pd.pivot_table(anxiety_depression, values='Value', index=['Group', 'Subgroup'], columns=['Indicator'], aggfunc=sum).reset_index()

    # Separate into 2 dfs
    anxiety_depression_age = pivot_anxiety_depression[pivot_anxiety_depression['Group']=="By Age"].iloc[:,1:].reset_index(drop=True)
    anxiety_depression_sex = pivot_anxiety_depression[pivot_anxiety_depression['Group']=="By Sex"].iloc[:,1:].reset_index(drop=True)

    ## data cleaning
    # anxiety_depression_age
    anxiety_depression_age[['start_age', 'end_age']] = anxiety_depression_age['Subgroup'].str.split(" - ", expand=True)
    anxiety_depression_age[['end_age', 'x']] = anxiety_depression_age['end_age'].str.split(" ", expand=True)
    anxiety_depression_age = anxiety_depression_age.iloc[:,1:6]
    anxiety_depression_age.iloc[-1,3] = '80'
    anxiety_depression_age.iloc[-1,4] = '200'
    anxiety_depression_age.loc['mean'] = anxiety_depression_age.mean(numeric_only=True) #set the index of 0-18 year-range to be the average value of all
    anxiety_depression_age.iloc[-1,3] = '0'
    anxiety_depression_age.iloc[-1,4] = '17'
    adindex_age = anxiety_depression_age.rename(columns={"Symptoms of Anxiety Disorder": "ADI_age", "Symptoms of Anxiety Disorder or Depressive Disorder": "ADDI_age", "Symptoms of Depressive Disorder": "DDI_age"}).reset_index(drop=True)

    # anxiety_depression_sex
    anxiety_depression_sex.loc['mean'] = anxiety_depression_sex.mean(numeric_only=True) #set the index of 'Others' to be the average value of all
    anxiety_depression_sex.iloc[-1,0] = 'others' 
    adindex_sex = anxiety_depression_sex.rename(columns={"Subgroup": "sex", "Symptoms of Anxiety Disorder": "ADI_sex", "Symptoms of Anxiety Disorder or Depressive Disorder": "ADDI_sex", "Symptoms of Depressive Disorder": "DDI_sex"}).reset_index(drop=True)
    adindex_sex['sex'] = adindex_sex['sex'].str.replace('Male', 'male')
    adindex_sex['sex'] = adindex_sex['sex'].str.replace('Female', 'female')
    return adindex_age, adindex_sex

## Merge pixstory dataset w/ adindex_age (anxiety & depression index on age)
def merge_AD_indexes():
    # Import pixstory data
    pixstory_df_path = '../data/pixstory/pixstory_hobby.csv'
    pixstory_df = pd.read_csv(pixstory_df_path)
    
    # Change the format of 'Account Created Date' to '%Y-%m-%d'
    pixstory_df['Account Created Date'] = pd.to_datetime(pixstory_df['Account Created Date'])
    pixstory_df['Account Created Date'] = pixstory_df['Account Created Date'].dt.strftime('%Y-%m-%d')

    adindex_age, adindex_sex = clean_AD_data()

    # First, merge with indexes on age
    df = pd.DataFrame()
    for age in pixstory_df['Age']:
        for i in range(len(adindex_age)):
            if age >= int(adindex_age.loc[i, "start_age"]) and age <= int(adindex_age.loc[i, "end_age"]):
                lst_age = list(adindex_age[["ADI_age", "DDI_age", "ADDI_age"]].iloc[i])
                df_age = pd.DataFrame([lst_age])
                df = pd.concat([df, df_age])
                break
    
    df.columns = ["ADI_age", "DDI_age", "ADDI_age"]
    df_concat = pd.concat([pixstory_df , df.set_index(pixstory_df.index)], axis=1)

    # Secondly, merge with indexes on sex
    df = pd.DataFrame()
    for gender in df_concat['Gender']:
        for i in range(len(adindex_sex)):
            if gender == adindex_sex.loc[i, "sex"]:
                lst_sex = list(adindex_sex[["ADI_sex", "DDI_sex", "ADDI_sex"]].iloc[i])
                df_sex = pd.DataFrame([lst_sex])
                df = pd.concat([df, df_sex])
                break
            elif i == 2 and pd.isnull(gender):
                lst_sex = list(adindex_sex[["ADI_sex", "DDI_sex", "ADDI_sex"]].iloc[2])
                df_sex = pd.DataFrame([lst_sex])
                df = pd.concat([df, df_sex])
                break

    df.columns = ["ADI_sex", "DDI_sex", "ADDI_sex"]
    pixstory_adindex_age_sex = pd.concat([df_concat , df.set_index(df_concat.index)], axis=1)

    pixstory_adindex_age_sex.to_csv('../data/pixstory/pixstory_adindex.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    merge_AD_indexes()