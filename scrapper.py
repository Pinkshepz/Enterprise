''' Web scrapper to get economic data from Forex Factory.
Returns pd.dataFrame of all economic data in a specific range '''

# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Requests web elements
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}


def scrapper(date: str):  # Date format: mmmd.yyyy
    ''' Return table of economic data of given date '''

    url = "https://www.forexfactory.com/calendar?day=" + date
    response = requests.get(
        url,
        timeout=1000,
        headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Economic data are stored in <tr class='calendar_row'> tag
    table_rows = soup.find_all(class_="calendar_row")

    # 2D array storing all processed economic data
    final_data = []

    for row in table_rows:
        # Extract data from each distinct column
        # Since each column has different html structure, we have to parse it manually ;-;
        columns = []
        columns.append(date)
        columns.append(*row.find(class_="time").stripped_strings)
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

        final_data.append(columns)

    return final_data


df = pd.DataFrame(scrapper("dec1.2022"))
print(df)
