import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

# Film Festivals 2022
def ff2022():
    # Web scraping film festivals 2022
    soup = BeautifulSoup('../data/ff2022.html', "html.parser")
    all_2022 = []
    for word in soup.find_all('p'):  
        find_all_festival_2022 = word.get_text()
        all_2022.append(find_all_festival_2022)

    # removing incorrect data and stripping spaces
    all_2022 = all_2022[4:-6]
    all_2022 = [string for string in all_2022 if string.strip()]
    all_2022.remove('Follow our coverage of Sundance 2022 here!')
    all_2022.remove('Get us to cover your film festival: contact us!')

    # seperating festivals and dates
    festivals = []
    dates = []
    for i in range(len(all_2022)):
        if i % 2 == 0:
            festivals.append(all_2022[i])
        else:
            dates.append(all_2022[i])

    # spliting original date format to start date and end date
    dates2 = [i.split('-') for i in dates]

    for i in dates2:
        for j in range(0,2):
            i[j] = i[j].strip()
        if len(i[0]) > 3:
            i[0] = str(i[0] + ' 2022')
        elif len(i[0]) < 3:
            i[1] = datetime.strftime(datetime.strptime(i[1], '%d %B %Y'), '%d %B %Y')
            i[0] = str(i[0] + i[1][2:])

    start_date = []
    end_date = []
    for i in range(len(dates2)):
        for j in (0,1):
            if j % 2 == 0:
                start_date.append(dates2[i][j])
            else:
                end_date.append(dates2[i][j])

    ff2022 = pd.DataFrame(list(zip(festivals, start_date, end_date)), columns =['Festivals', 'Start_Date', 'End_Date']) 

    return ff2022


# Film Festivals 2021
# FEBRUARY 2021
def ff2021_feb():
    # web scraping
    soup = BeautifulSoup('../data/ff2021_feb.html', "html.parser")
    all_2021_feb = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_feb = word.get_text()
        all_2021_feb.append(find_all_festival_2021_feb)

    # brief cleaning all_2021_feb
    all_2021_feb = all_2021_feb[3:-4]
    all_2021_feb = [string for string in all_2021_feb if string.strip()]
    all_2021_feb = [i for i in all_2021_feb if i != 'Learn more']
    all_2021_feb = [i for i in all_2021_feb if i != '\xa0Learn more']
    all_2021_feb = [i for i in all_2021_feb if i != '\xa0\xa0Learn more']
    all_2021_feb = [i for i in all_2021_feb if i != 'Learn more\xa0']

    # seperating festivals and dates
    festivals_2021_feb = []
    dates_2021_feb = []
    for i in range(len(all_2021_feb)):
        if i % 2 == 0:
            festivals_2021_feb.append(all_2021_feb[i])
        else:
            dates_2021_feb.append(all_2021_feb[i])

    # spliting original date format to start date and end date
    for i in range(len(dates_2021_feb)):
        dates_2021_feb[i] = dates_2021_feb[i].replace(' – ', '-') 

    dates2_2021_feb = [i.split('-') for i in dates_2021_feb]

    # deleting irrelevant data
    for i in range(len(dates2_2021_feb)):
        if len(dates2_2021_feb[i]) == 1:
            dates2_2021_feb[i].append(dates2_2021_feb[i][0])
        for j in (0,1):
            dates2_2021_feb[i][j] = dates2_2021_feb[i][j].strip()
            dates2_2021_feb[i][j] = dates2_2021_feb[i][j].replace(' (hybrid)', '') 
            dates2_2021_feb[i][j] = dates2_2021_feb[i][j].replace(' (online)', '')
            dates2_2021_feb[i][j] = dates2_2021_feb[i][j].replace('th', '') 

    for i in dates2_2021_feb:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')
    
    return festivals_2021_feb, dates2_2021_feb


# MARCH 2021
def ff2021_mar():
    # web scraping
    soup = BeautifulSoup('../data/ff2021_mar.html', "html.parser")
    all_2021_mar = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_mar = word.get_text()
        all_2021_mar.append(find_all_festival_2021_mar)

    # cleaning data all_2021_mar
    all_2021_mar = all_2021_mar[3:-6]
    all_2021_mar = [string for string in all_2021_mar if string.strip()]
    all_2021_mar = [i for i in all_2021_mar if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_mar = []
    dates_2021_mar = []
    for i in range(len(all_2021_mar)):
        if i % 2 == 0:
            festivals_2021_mar.append(all_2021_mar[i])
        else:
            dates_2021_mar.append(all_2021_mar[i])

    # spliting original date format to start date and end date
    dates2_2021_mar = [i.split('-') for i in dates_2021_mar]

    # deleting irrelevant data
    for i in range(len(dates2_2021_mar)):
        if len(dates2_2021_mar[i]) == 1:
            dates2_2021_mar[i].append(dates2_2021_mar[i][0])
        for j in (0,1):
            dates2_2021_mar[i][j] = dates2_2021_mar[i][j].strip()
            dates2_2021_mar[i][j] = dates2_2021_mar[i][j].replace(' (hybrid)', '') 
            dates2_2021_mar[i][j] = dates2_2021_mar[i][j].replace(' (online)', '')
            dates2_2021_mar[i][j] = dates2_2021_mar[i][j].replace(' (for industry members only)', '') 

    for i in dates2_2021_mar:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_mar, dates2_2021_mar


# APRIL 2021
def ff2021_apr():
    # web scraping
    soup = BeautifulSoup('../data/ff2021_apr.html', "html.parser")
    all_2021_apr = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_apr = word.get_text()
        all_2021_apr.append(find_all_festival_2021_apr)

    # cleaning data all_2021_mar
    all_2021_apr = all_2021_apr[6:-7]
    all_2021_apr = [string for string in all_2021_apr if string.strip()]
    all_2021_apr = [i for i in all_2021_apr if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_apr = []
    dates_2021_apr = []
    for i in range(len(all_2021_apr)):
        if i % 2 == 0:
            festivals_2021_apr.append(all_2021_apr[i])
        else:
            dates_2021_apr.append(all_2021_apr[i])

    # spliting original date format to start date and end date
    dates2_2021_apr = [i.split('-') for i in dates_2021_apr]

    for i in range(len(dates2_2021_apr)):
        if len(dates2_2021_apr[i]) == 1:
            dates2_2021_apr[i].append(dates2_2021_apr[i][0])
        for j in (0,1):
            dates2_2021_apr[i][j] = dates2_2021_apr[i][j].strip()

    for i in dates2_2021_apr:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_apr, dates2_2021_apr


# MAY 2021
def ff2021_may():
    # web scraping
    soup = BeautifulSoup('../data/ff2021_may.html', "html.parser")
    all_2021_may = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_may = word.get_text()
        all_2021_may.append(find_all_festival_2021_may)

    # cleaning data all_2021_may
    all_2021_may = all_2021_may[4:-5]
    all_2021_may = [string for string in all_2021_may if string.strip()]
    all_2021_may = [i for i in all_2021_may if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_may = []
    dates_2021_may = []
    for i in range(len(all_2021_may)):
        if i % 2 == 0:
            festivals_2021_may.append(all_2021_may[i])
        else:
            dates_2021_may.append(all_2021_may[i])

    # spliting original date format to start date and end date
    dates2_2021_may = [i.split('-') for i in dates_2021_may]

    for i in range(len(dates2_2021_may)):
        if len(dates2_2021_may[i]) == 1:
            dates2_2021_may[i].append(dates2_2021_may[i][0])
        for j in (0,1):
            dates2_2021_may[i][j] = dates2_2021_may[i][j].strip()

    for i in dates2_2021_may:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_may, dates2_2021_may


# JUNE 2021
def ff2021_jun():
    # web scraping 2021 jun
    soup = BeautifulSoup('../data/ff2021_jun.html', "html.parser")
    all_2021_jun = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_jun = word.get_text()
        all_2021_jun.append(find_all_festival_2021_jun)

    # cleaning data all_2021_jun
    all_2021_jun = all_2021_jun[5:-5]
    all_2021_jun = [string for string in all_2021_jun if string.strip()]
    all_2021_jun = [i for i in all_2021_jun if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_jun = []
    dates_2021_jun = []
    for i in range(len(all_2021_jun)):
        if i % 2 == 0:
            festivals_2021_jun.append(all_2021_jun[i])
        else:
            dates_2021_jun.append(all_2021_jun[i])

    # spliting original date format to start date and end date
    dates2_2021_jun = [i.split('-') for i in dates_2021_jun]

    for i in range(len(dates2_2021_jun)):
        if len(dates2_2021_jun[i]) == 1:
            dates2_2021_jun[i].append(dates2_2021_jun[i][0])
        for j in (0,1):
            dates2_2021_jun[i][j] = dates2_2021_jun[i][j].strip()

    for i in dates2_2021_jun:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_jun, dates2_2021_jun


# JULY 2021
def ff2021_july():
    # web scraping 2021 july
    soup = BeautifulSoup('../data/ff2021_july.html', "html.parser")
    all_2021_july = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_july = word.get_text()
        all_2021_july.append(find_all_festival_2021_july)

    # cleaning data all_2021_july
    all_2021_july = all_2021_july[5:-6]
    all_2021_july = [string for string in all_2021_july if string.strip()]
    all_2021_july = [i for i in all_2021_july if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_july = []
    dates_2021_july = []
    for i in range(len(all_2021_july)):
        if i % 2 == 0:
            festivals_2021_july.append(all_2021_july[i])
        else:
            dates_2021_july.append(all_2021_july[i])

    # spliting original date format to start date and end date
    dates2_2021_july = [i.split('-') for i in dates_2021_july]

    for i in range(len(dates2_2021_july)):
        dates2_2021_july[i][0] = re.sub(r'(?:[A-z, &\(\)äöüÄŠńžÖÜâßŽ]+ \| )', '', dates2_2021_july[i][0])
        dates2_2021_july[i][1] = dates2_2021_july[i][1].replace(', 2021', '')
        if len(dates2_2021_july[i]) == 1:
            dates2_2021_july[i].append(dates2_2021_july[i][0])
        for j in (0,1):
            dates2_2021_july[i][j] = dates2_2021_july[i][j].strip()

    for i in dates2_2021_july:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_july, dates2_2021_july


# OCTOBER 2021
def ff2021_oct():
    # web scraping
    soup = BeautifulSoup('../data/ff2021_oct.html', "html.parser")
    all_2021_oct = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_oct = word.get_text()
        all_2021_oct.append(find_all_festival_2021_oct)

    # cleaning data all_2021_oct
    all_2021_oct = all_2021_oct[3:-6]
    all_2021_oct = [string for string in all_2021_oct if string.strip()]
    all_2021_oct = [i for i in all_2021_oct if i != 'Learn more  | Instagram']
    all_2021_oct = [i for i in all_2021_oct if i != 'Learn more | Instagram']
    all_2021_oct = [i for i in all_2021_oct if i != 'Learn more']

    # seperating festivals and dates
    festivals_2021_oct = []
    dates_2021_oct = []
    for i in range(len(all_2021_oct)):
        if i % 2 == 0:
            festivals_2021_oct.append(all_2021_oct[i])
        else:
            dates_2021_oct.append(all_2021_oct[i])

    # spliting original date format to start date and end date
    dates2_2021_oct = [i.split('-') for i in dates_2021_oct]

    for i in range(len(dates2_2021_oct)):
        dates2_2021_oct[i][0] = re.sub(r'(?:[A-z, &\(\)äöüÄŠńžÖÜâßŽ’]+ \| )', '', dates2_2021_oct[i][0])
        dates2_2021_oct[i][1] = dates2_2021_oct[i][1].replace(', 2021', '')
        if len(dates2_2021_oct[i]) == 1:
            dates2_2021_oct[i].append(dates2_2021_oct[i][0])
        for j in (0,1):
            dates2_2021_oct[i][j] = dates2_2021_oct[i][j].strip()

    for i in dates2_2021_oct:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_oct, dates2_2021_oct


# NOVEMBER 2021
def ff2021_nov():
    # web scraping 2021 nov
    soup = BeautifulSoup('../data/ff2021_nov.html', "html.parser")
    all_2021_nov = []
    for word in soup.find_all('p'):  
        find_all_festival_2021_nov = word.get_text()
        all_2021_nov.append(find_all_festival_2021_nov)

    # deleting irrelevant data
    all_2021_nov = all_2021_nov[6:-7]
    all_2021_nov = [string for string in all_2021_nov if string.strip()]
    all_2021_nov = [i for i in all_2021_nov if i != 'Learn more  | Instagram']
    all_2021_nov = [i for i in all_2021_nov if i != 'Learn more | Instagram']
    all_2021_nov = [i for i in all_2021_nov if i != 'Learn more']
    all_2021_nov = [i for i in all_2021_nov if i != 'Explore our film festival coverage opportunities and reach out to promote your festival :)']

    # seperating festivals and dates
    festivals_2021_nov = []
    dates_2021_nov = []
    for i in range(len(all_2021_nov)):
        if i % 2 == 0:
            festivals_2021_nov.append(all_2021_nov[i])
        else:
            dates_2021_nov.append(all_2021_nov[i])

    # for Abertoir International Horror Festival of Wales, which has two dates, I seperate them into two events (1 & 2)
    festivals_2021_nov.append('Abertoir International Horror Festival of Wales 2')
    dates_2021_nov.append('November 12-14, 2021 | Wales')
    festivals_2021_nov[5] = 'Abertoir International Horror Festival of Wales 1'
    dates_2021_nov[5] = 'November 2-7'

    # spliting original date format to start date and end date
    dates2_2021_nov = [i.split('-') for i in dates_2021_nov]
    
    for i in range(len(dates2_2021_nov)):
        dates2_2021_nov[i][1] = re.sub(r'(?:, 2021 \| [A-z, &\(\)äöüÄŠńžÖÜâßŽ\’]+)', '', dates2_2021_nov[i][1])
        if len(dates2_2021_nov[i]) == 1:
            dates2_2021_nov[i].append(dates2_2021_nov[i][0])
        for j in (0,1):
            dates2_2021_nov[i][j] = dates2_2021_nov[i][j].strip()

    for i in dates2_2021_nov:
        i[0] = datetime.strptime(i[0], '%B %d').strftime('%d %B')
        if len(i[1]) > 2:
            i[1] = datetime.strptime(i[1], '%B %d').strftime('%d %B')
        else:
            i[1] = str(i[1] + i[0][2:])
        for j in (0,1):
            i[j] = str(i[j] + ' 2021')

    return festivals_2021_nov, dates2_2021_nov


# Joining 2021 Film Festivals
def ff2021():
    # Joining film festival data
    festivals_2021 = []
    festivals_2021.extend(ff2021_feb()[0])
    festivals_2021.extend(ff2021_mar()[0])
    festivals_2021.extend(ff2021_apr()[0])
    festivals_2021.extend(ff2021_may()[0])
    festivals_2021.extend(ff2021_jun()[0])
    festivals_2021.extend(ff2021_july()[0])
    festivals_2021.extend(ff2021_oct()[0])
    festivals_2021.extend(ff2021_nov()[0])

    # Joining dates and seperate them to Start_Date and End_Date
    dates_2021 = []
    dates_2021.extend(ff2021_feb()[1])
    dates_2021.extend(ff2021_mar()[1])
    dates_2021.extend(ff2021_apr()[1])
    dates_2021.extend(ff2021_may()[1])
    dates_2021.extend(ff2021_jun()[1])
    dates_2021.extend(ff2021_july()[1])
    dates_2021.extend(ff2021_oct()[1])
    dates_2021.extend(ff2021_nov()[1])

    start_date_2021 = []
    end_date_2021 = []
    for i in range(len(dates_2021)):
        for j in (0,1):
            if j % 2 == 0:
                start_date_2021.append(dates_2021[i][j])
            else:
                end_date_2021.append(dates_2021[i][j])

    ff2021 = pd.DataFrame(list(zip(festivals_2021, start_date_2021, end_date_2021)), columns =['Festivals', 'Start_Date', 'End_Date']) 

    return ff2021


# Importing 2020 film festivals
def ff2020():
    # the original dataset was downloaded form https://docs.google.com/spreadsheets/d/1lEBkMsbXHu-TwZlPZBSVUn8GQDmzT2ADr74CBa92txE/edit#gid=205447644
    # Since there were a lot of changes due to COVID-19, a certain amount of manual data cleaning was done to the dataset
    # I deleted the data with no specific dates and corrected the date changes because of COVID-19
    ff2020_df = pd.read_csv('../data/ff2020.csv')

    # formatting date for film festivals 2020
    ff2020_df['Start_Date'] = pd.to_datetime(ff2020_df['Start_Date'])
    ff2020_df['Start_Date'] = ff2020_df['Start_Date'].dt.strftime('%Y-%m-%d')
    ff2020_df['End_Date'] = pd.to_datetime(ff2020_df['End_Date'])
    ff2020_df['End_Date'] = ff2020_df['End_Date'].dt.strftime('%Y-%m-%d')

    return ff2020_df


# Creating a dataframe that contains all film festivals and the dates
def ff_all():
    # changing the date format of ff2021
    ff2021_df = ff2021()
    ff2021_df['Start_Date'] = pd.to_datetime(ff2021_df['Start_Date'])
    ff2021_df['Start_Date'] = ff2021_df['Start_Date'].dt.strftime('%Y-%m-%d')
    ff2021_df['End_Date'] = pd.to_datetime(ff2021_df['End_Date'])
    ff2021_df['End_Date'] = ff2021_df['End_Date'].dt.strftime('%Y-%m-%d')

    # changing the date format of ff2022
    ff2022_df = ff2022()
    ff2022_df['Start_Date'] = pd.to_datetime(ff2022_df['Start_Date'])
    ff2022_df['Start_Date'] = ff2022_df['Start_Date'].dt.strftime('%Y-%m-%d')
    ff2022_df['End_Date'] = pd.to_datetime(ff2022_df['End_Date'])
    ff2022_df['End_Date'] = ff2022_df['End_Date'].dt.strftime('%Y-%m-%d')

    ff2020_df = ff2020()

    # joining ff2020, ff2021, ff2022
    df_filmfestivals = pd.concat([ff2020_df, ff2021_df, ff2022_df], ignore_index = True)

    # Create Event_Date column that contains a sequence of dates between start dates and end dates
    # modyfied from original code by Shih-Min Huang in sporting_event.py
    df_filmfestivals1 = df_filmfestivals.assign(Event_Date = [pd.date_range(start, end, freq = '1d') for start, end in zip(
    df_filmfestivals['Start_Date'], df_filmfestivals['End_Date'])]).explode('Event_Date')

    return df_filmfestivals1

def post_filmfestival_date_match():
    # Prepare for the two data to be merged
    pixstory_df_path = '../data/pixstory/pixstory_sports.csv'
    pixstory_df = pd.read_csv(pixstory_df_path)

    # Change the format of 'Account Created Date' to '%Y-%m-%d'
    pixstory_df['Account Created Date'] = pd.to_datetime(pixstory_df['Account Created Date'])
    pixstory_df['Account Created Date'] = pixstory_df['Account Created Date'].dt.strftime('%Y-%m-%d')
    pixstory_date = pixstory_df['Account Created Date'].unique()
    pixstory_date = pd.DataFrame({'Account Created Date': pixstory_date})
    filmfestivals_df = ff_all()[['Event_Date', 'Festivals']]

    # Merge the data (post date - event date)
    pixstory_date = pixstory_date.astype('datetime64[ns]')
    joined_df = pd.merge(pixstory_date, filmfestivals_df, left_on = ['Account Created Date'], right_on = ['Event_Date'], how = 'left')
    new_joined_df = joined_df[['Account Created Date', 'Festivals']].dropna()

    # Create the column listing all corresponding events on the dates
    df = new_joined_df.groupby(['Account Created Date']).agg({'Festivals': lambda x: x.tolist()}).reset_index(level = 0)

    # Merge the corresponding table with the original pixstory dataset
    pixstory_df = pd.read_csv(pixstory_df_path)
    pixstory_df['Account Created Date'] = pixstory_df['Account Created Date'].astype('datetime64[ns]')
    post_filmfestival_date_match = pd.merge(pixstory_df, df, on = ['Account Created Date'], how = 'left')

    post_filmfestival_date_match.to_csv('../data/pixstory/pixstory_film.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    post_filmfestival_date_match()
