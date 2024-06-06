import urllib3
from datetime import datetime
import csv
import pandas as pd


PATH = "./ad1"

regions = {
    1: 22,
    2: 24,
    3: 23,
    4: 25,
    5: 3,
    6: 4,
    7: 8,
    8: 19,
    9: 20,
    10: 21,
    11: 9,
    12: '-',
    13: 10,
    14: 11,
    15: 12,
    16: 13,
    17: 14,
    18: 15,
    19: 16,
    20: '-',
    21: 17,
    22: 18,
    23: 6,
    24: 1,
    25: 2,
    26: 7,
    27: 5,
}


def obl_read(filename, i):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    df = pd.read_csv(filename, header=1, names=headers)  # read csv, create df
    df.drop('empty', inplace=True, axis=1)  # drop empty column
    df.drop(df.tail(1).index, inplace=True)  # drop last row
    df['Year'] = df['Year'].replace(['<tt><pre>1982'], '1982')  # delete tags from first value
    df = df.drop(df.loc[df['VHI'] == -1].index)  # drop all nan values
    df['area'] = i  # service reg number
    df['area'].replace({i: regions[i]}, inplace=True)  # task reg number
    return df


def main():

    http = urllib3.PoolManager()

    for i in range(1, 28):
        url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2024&type=Mean'

        response = http.request('GET', url)
        text = response.data

        now = datetime.now()
        date_and_time_time = now.strftime("%d%m%Y%H%M%S")

        with open(f"{PATH}NOAA_ID{i}_{date_and_time_time}.csv", 'wb') as f:
            f.write(text)

        if i == 1:
            df = obl_read(f"{PATH}NOAA_ID{i}_{date_and_time_time}.csv", i)
        else:
            df = pd.concat([df, obl_read(f"{PATH}NOAA_ID{i}_{date_and_time_time}.csv", i)])
        # print(obl_read(f"{PATH}NOAA_ID{i}_{date_and_time_time}.csv", i).head())

    print("VHI is downloaded...")

    df.to_csv('complete_dataset.csv', encoding='utf-8')


def get_dataset():
    df = pd.read_csv('complete_dataset.csv', encoding='utf-8')
    return df


if __name__ == "__main__":
    main()

