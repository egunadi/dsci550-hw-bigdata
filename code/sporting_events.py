# Import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

pixstory_df_path = '../data/pixstory/pixstory_clean.csv'

# Import pixstory data
def pixstory_data():
    pixstory_df = pd.read_csv(pixstory_df_path)

    # Change the format of 'Account Created Date' to '%Y-%m-%d'
    pixstory_df['Account Created Date'] = pd.to_datetime(pixstory_df['Account Created Date'])
    pixstory_df['Account Created Date'] = pixstory_df['Account Created Date'].dt.strftime('%Y-%m-%d')

    return pixstory_df

# Parse the website
def web_parsing(url):
    # Parse the table from the website
    page = requests.get(url)
    page.encoding = 'UTF-8'
    soup = BeautifulSoup(page.text, 'lxml')
    table1 = soup.find('table')

    # Use loop to create the column names
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)

    parsed_df = pd.DataFrame(columns=headers)

    # Use for-loop to create the content rows 
    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(parsed_df)
        parsed_df.loc[length] = row

    return parsed_df


# Parse pages of sporting events from 2020 to 2022
def sport_event_parsing(start_year, end_year):
    end_year += 1
    sport_event_all = pd.DataFrame()

    for i in range(start_year, end_year):
        url = 'https://www.topendsports.com/events/calendar-' + str(i) + '.htm'
        sport_event = web_parsing(url)
        sport_event['year'] = i
        sport_event_all = pd.concat([sport_event_all, sport_event], sort=False)

    return sport_event_all.reset_index(drop=True)

start_year = 2020
end_year = 2022

# Data cleaning for the 'Date(s)' column
def sport_event_dates():
    sport_event_all = sport_event_parsing(start_year, end_year)

    # Data cleaning
    sport_event_all['Date(s)'] = sport_event_all['Date(s)'].str.strip()
    sport_event_all = sport_event_all[sport_event_all['Date(s)'].str.contains("canceled|pos") == False]

    # Split the date into 2 columns and do data cleaning
    sport_event_all[['start_date', 'end_date']] = sport_event_all['Date(s)'].str.split("–|-", expand=True)
    sport_event_all['start_date'] = sport_event_all['start_date'].str.strip()
    sport_event_all['end_date'] = sport_event_all['end_date'].str.strip()

    # Tunring 'None' to the same date as start date
    sport_event_all['end_date'] = ['None' if v is None else v for v in sport_event_all['end_date']]
    sport_event_all.loc[sport_event_all['end_date'] == "None", 'end_date'] = sport_event_all['start_date']

    # Append Month for end_dates without Month
    sport_event_all.loc[sport_event_all['end_date'].str.isnumeric(), 'end_date'] = sport_event_all['start_date'].str[0:3] + ' ' +sport_event_all['end_date']

    # Change the date format
    sport_event_all['start_date'] = sport_event_all['year'].astype(str) + ' ' + sport_event_all['start_date'].astype(str)
    sport_event_all['end_date'] = sport_event_all['year'].astype(str) + ' ' + sport_event_all['end_date'].astype(str)
    sport_event_all[['start_date', 'end_date']] = sport_event_all[['start_date', 'end_date']].apply(pd.to_datetime)

    # Create event_date column to indicate all the dates with sport events
    sport_event_all = sport_event_all.assign(event_date=[pd.date_range(start, end, freq='1d') for start, end in zip(
        sport_event_all['start_date'], sport_event_all['end_date'])]).explode('event_date')
    
    return sport_event_all


# Join pixstory dataset with sport event dataset
def post_event_date_match():
    # Prepare for the two data to be merged
    pixstory_date = pixstory_data()['Account Created Date'].unique()
    pixstory_date = pd.DataFrame({'Account Created Date': pixstory_date})
    sport_event_df = sport_event_dates()[['event_date', 'Event']]

    # Merge the data (post date - event date)
    pixstory_date = pixstory_date.astype('datetime64[ns]')
    joined_df = pd.merge(pixstory_date, sport_event_df, left_on=['Account Created Date'], right_on=['event_date'], how='left')
    new_joined_df = joined_df[['Account Created Date', 'Event']].dropna()

    # Create the column listing all corresponding events on the dates
    df = new_joined_df.groupby(['Account Created Date']).agg({'Event': lambda x: x.tolist()}).reset_index(level=0)
    
    # Merge the corresponding table with the original pixstory dataset
    pixstory_df = pixstory_data()
    pixstory_df['Account Created Date'] = pixstory_df['Account Created Date'].astype('datetime64[ns]')
    post_event_date_match = pd.merge(pixstory_df, df, on=['Account Created Date'], how='left')
    post_event_date_match = post_event_date_match.rename(columns={"Event": "sport_event"})

    post_event_date_match.to_csv('../data/pixstory/pixstory_sports.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    post_event_date_match()