''' Web scrapper to get economic data from Forex Factory.
Returns pd.dataFrame of all economic data in a specific range '''

# Imports
import datetime as dt
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Requests web elements
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}


def handle_time(time: str) -> tuple[str, int]:
    ''' Change time format from 12-hour UTC-5 to 24-hour UTC+7 '''

    if time in ["All Day", " "]:
        return time, 0
    elif str(time.split(":")[1][-2:]) == "am":
        return str(int(time.split(":")[0]) + 12) + ":" + str(time.split(":")[1][:-2]), 0
    else:
        return str(time.split(":")[0]) + ":" + str(time.split(":")[1][:-2]), 1


def scrapper(date: str) -> list():  # Date format: mmmd.yyyy
    ''' Return table of economic data of given date '''

    fdate = date.strftime("%b").lower() + date.strftime("%d").lstrip("0") + date.strftime(".%Y")
    url = "https://www.forexfactory.com/calendar?day=" + fdate
    response = requests.get(
        url,
        timeout=1000,
        headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

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
        timesig = handle_time(row.find(class_="time").contents[-1].lstrip("\n"))
        columns.append((date + dt.timedelta(days=timesig[1])).strftime("%a, %d %b %y"))
        columns.append(timesig[0])
        columns.append(*row.find(class_="currency").stripped_strings)
        columns.append(
            row.find(class_="impact").contents[1].contents[1]['class'][0])
        columns.append(
            row.find(class_="event").contents[1].contents[1].contents[0])
        columns.append(row.find(class_="actual").string)
        columns.append(row.find(class_="forecast").string)
        if row.find(class_="previous").string is None:
            if len(row.find(class_="previous").contents) != 0:
                columns.append(
                    row.find(class_="previous").contents[0].contents[0])
            else:
                columns.append(None)
        else:
            columns.append(row.find(class_="previous").string)

        array.append(columns)

    return array

# Loop for each day's data: set 1000 days
start_date = dt.datetime(2022, 12, 31)
final_data = []

for i in range(1000):
    idate = start_date - dt.timedelta(days=i)
    final_data.extend(scrapper(idate))
    print(idate.strftime("%b %d %Y") + " count:" + str(len(final_data)))

# Convert to pd.DataFrame with some cleaning
header = ["date", "time", "currency", "impact", "event", "actual", "forecast", "previous"]
df = pd.DataFrame(final_data, columns=header)
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
df.sort_values(by=["date"], inplace=True, ascending=False)
df.reset_index(inplace=True, drop=True)
print(df)
