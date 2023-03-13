import pandas as pd
import csv

def consolidate_pixstory_data():
    nov10_15000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/15000 data 10 Nov.csv'
    nov18_15000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/15000 data 18 Nov.csv'
    nov18_10000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/10000 data 18 Nov.csv'
    data_15000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/15000 data.csv'
    data1_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/data1.csv'
    data_10000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/10000 data.csv'
    nov10_10000_filepath = '../data/pixstory/Pixstory Dataset Feb 2023/10000 data 10Nov .csv'

    # import data
    nov10_15000_df = pd.read_csv(nov10_15000_filepath, delimiter=',', encoding='utf-8')
    nov18_15000_df = pd.read_csv(nov18_15000_filepath, delimiter=',', encoding='utf-8')
    nov18_10000_df = pd.read_csv(nov18_10000_filepath, delimiter=',', encoding='utf-8')
    data_15000_df = pd.read_csv(data_15000_filepath, delimiter=',', encoding='utf-8')
    data1_df = pd.read_csv(data1_filepath, delimiter=',', encoding='utf-8')
    data_10000_df = pd.read_csv(data_10000_filepath, delimiter=',', encoding='utf-8')
    nov10_10000_df = pd.read_csv(nov10_10000_filepath, delimiter=',', encoding='utf-8')

    # consolidate data
    pixstory_df =  pd.concat([nov10_15000_df, nov18_15000_df, nov18_10000_df, data_15000_df, data1_df, data_10000_df, nov10_10000_df])

    # export data
    pixstory_df.to_csv('../data/pixstory/pixstory.csv', encoding='utf-8', index=False)

def convert_csv_to_tsv(input_file, output_file):
    input_path = '../data/pixstory/' + input_file
    output_path = '../data/pixstory/' + output_file
    
    with    open(input_path, 'r', encoding='utf-8') as csvin, \
            open(output_path, 'w', encoding='utf-8') as tsvout:
                csvin = csv.reader(csvin)
                tsvout = csv.writer(tsvout, dialect='excel-tab')
 
                for row in csvin:
                    tsvout.writerow(row)

if __name__ == '__main__':
    consolidate_pixstory_data()
    # convert_csv_to_tsv('pixstory.csv', 'pixstory_original.tsv')
    # convert_csv_to_tsv('pixstory_adindex.csv', 'pixstory_final.tsv')
