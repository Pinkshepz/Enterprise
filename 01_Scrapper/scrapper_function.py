''' Web scrapper to get economic data from Forex Factory.
Returns pd.dataFrame of all economic data in a specific range '''

# Imports
import datetime as dt
import pandas as pd
from numpy import arange
from bs4 import BeautifulSoup
# from selenium import webdriver
import requests

# Requests web elements
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}


def handle_time(time: str) -> tuple:
    """Change time format from 12-hour UTC+8 to 24-hour UTC+7

    Args:
        time (str): Time i.e. 8.00pm

    Returns:
        tuple(str, int): (24h time format i.e. 20.00, date addition from timezone change i.e. +1)
    """

    if ":" not in time or time == " ":
        return time, 0
    elif str(time.split(":")[1][-2:]) == "am":
        if int(time.split(":")[0]) - 1 < 0:
            return int(time.split(":")[0]) + 23, -1
        return str(int(time.split(":")[0]) - 1) + ":" + str(time.split(":")[1][:-2]), 0
    else:
        return str(int(time.split(":")[0]) + 11) + ":" + str(time.split(":")[1][:-2]), 0


def scrapper(date: str) -> list():  # Date format: mmmd.yyyy
    """Return table of economic data of given date

    Args:
        date (str): date for fetching data

    Returns:
        list of data: column name: [
            index,date,time,currency,impact,event,actual,forecast,previous
        ]
    """

    fdate = date.strftime("%b").lower() + date.strftime("%d").lstrip("0") + date.strftime(".%Y")
    url = "https://www.forexfactory.com/calendar?day=" + fdate
    response = requests.get(
        url,
        timeout=1000,
        headers=headers)
    html = response.text
    
    # dr = webdriver.Chrome()
    # dr.get(url)

    # soup = BeautifulSoup(dr.page_source.encode("utf-8"), "html.parser")
    soup = BeautifulSoup(html, "html.parser")

    # Economic data are stored in <tr class='calendar_row'>{data}</tr> tag
    table_rows = soup.find_all(class_="calendar_row")

    # 2D array storing all processed economic data
    array = []

    for row in table_rows:
        # Extract data from each distinct column
        # Since each column has different html structure, we have to parse it manually ;-;
        try:
            type(*row.find(class_="currency").stripped_strings)
        except TypeError:
            break

        columns = []
        timesig = handle_time(row.find(class_="time").contents[1].contents[0].lstrip('\n'))
        columns.append((date + dt.timedelta(days=timesig[1])).strftime("%a, %d %b %y"))
        columns.append(timesig[0])
        columns.append(*row.find(class_="currency").stripped_strings)
        columns.append(
            row.find(class_="impact").contents[1].get('title').split(" ")[0])
        columns.append(
            row.find(class_="event").contents[1].contents[1].contents[0])
        
        if len(row.find(class_="actual").find_all('span')) > 0:
            columns.append(row.find(class_="actual").find_all('span')[0].get_text())
        else:
            columns.append(None)

        if len(row.find(class_="forecast").find_all('span')) > 0:
            if row.find(class_="forecast").find_all('span')[0].contents[0] != '\xa0':
                columns.append(row.find(class_="forecast").find_all('span')[0].contents[0])
            else:
                columns.append(None)
        else:
            columns.append(None)

        if len(row.find(class_="previous").find_all('span')) > 0:
            if len(row.find(class_="previous").find_all('span', class_='revised')) > 0:
                columns.append(row.find(class_="previous").find_all('span', class_='revised')[0].contents[0])
            elif '\xa0' in row.find(class_="previous").find_all('span')[0].contents[0]:
                columns.append(None)
            else:
                columns.append(row.find(class_="previous").find_all('span')[0].contents[0].split(' ')[-5])
        else:
            columns.append(None)
        
        array.append(columns)

    return array


def forex_factory_scrapper(start_date: dt.datetime, end_date: dt.datetime) -> None:
    """Scrap financial data from FOREX factory website

    Args:
        start_date (dt.datetime): start date
        end_date (dt.datetime): end date
        
    Returns:
        csv file (.csv): column name: [
            index,date,time,currency,impact,event,actual,forecast,previous
        ]
    """

    DAYS = (end_date - start_date).days
    
    # Check interval is lesser than 10000
    LIMIT_DAYS = 9999
    if DAYS > LIMIT_DAYS:
        # Print log
        print(f"ERROR: TOO LONG DATE INTERVAL: {DAYS} expected {LIMIT_DAYS}")
        return 1
    
    FETCH_DATA = []

    # Print log
    print("START FETCHING DATA FROM FOREX FACTORY")
    print("--------------------------------------")
    print("#     DATE         COUNT")
    
    # Loop scrap data of each day
    for step in arange(1, DAYS):
        DATE = start_date + dt.timedelta(days=int(step)-1)
        SCRAP = scrapper(DATE)
        FETCH_DATA.extend(SCRAP)
        
        # Print log
        print(f'{step:04}  {DATE.strftime("%b %d %Y")}  {str(len(SCRAP))}')

    # Convert to pd.DataFrame with some cleaning
    HEADER = ['date', 'time', 'currency', 'impact', 'event', 'actual', 'forecast', 'previous']
    DF_DATA = pd.DataFrame(FETCH_DATA, columns=HEADER)
    DF_DATA['date'] = pd.to_datetime(DF_DATA['date'], format='%a, %d %b %y')
    DF_DATA.sort_values(by=['date'], inplace=True, ascending=False)
    DF_DATA.reset_index(inplace=True, drop=True)

    print(DF_DATA)

    # Import to csv file
    FILE_NAME = 'FOREX_' + start_date.strftime("%y%m%d") + '_' + end_date.strftime("%y%m%d")
    DF_DATA.to_csv('/workspaces/Enterprise/01_Scrapper/output/' + FILE_NAME + '.csv', 
                   sep=',', 
                   encoding='utf-8')

    # Print log
    print('SUCCESSFULLY FETCH DATA')
    print('-----------------------')
