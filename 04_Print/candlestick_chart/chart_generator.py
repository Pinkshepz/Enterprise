""" chart_generator.py module
    Produce candlestick chart image and forex factory table in weekly timeframe

    Input:
    1. .csv file path of candlestick chart
    2. .csv file path of forex economic data

    Out:
    1. .png image of candlestick chart
    2. .csv file of FOREX economic data parsed by week

    This is a cat -> 🐈
"""

# Imports
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from tqdm import tqdm

# Configure fonts
FONT_PATH = "/workspaces/Enterprise/00_Pinksheepkit/fonts/poppins/Poppins-{0}.ttf"
HEADING = "Bold"
LABEL = "Regular"
CONTENT = "Light"

# Font properties **kwargs -> usage: plt.some_method(**H_FONT)
H_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(HEADING)), "size": 12}
L_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(LABEL)), "size": 10}
C_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(CONTENT)), "size": 8}

# color palattes for candlestick chart
C_BULL = "#51A299"
C_BEAR = "#DD5E57"
C_SLATE500 = '#64748B'

# Configure plt rc params
plt.rcParams['figure.dpi'] = 300

# Root path
ROOT = '/workspaces/Enterprise/04_Print/static/data/'

# Function for data preparation and cleaning to DataFrame
def prepare_data(path_xauusd, path_forex):
    """ Prepare and clean DataFrame 

    Args
    1. XAUUSD.csv path
    2. FOREX.csv path

    Out
    1. pd.DataFrame of XAUUSD
    2. pd.DataFrame of FOREX
    """

    # Read csv
    df_xauusd = pd.read_csv(PATH_XAUUSD, parse_dates=['time']).drop(columns=['Unnamed: 0'])
    df_forex = pd.read_csv(PATH_FOREX, parse_dates=[['date', 'time']]).drop(columns=['Unnamed: 0'])

    df_xauusd.rename(columns={'time': 'datetime'}, inplace=True)
    df_forex.rename(columns={'date_time': 'datetime'}, inplace=True)

    # Change dataype of df_xauusd
    for col in df_xauusd.columns[1:]:
        df_xauusd[col] = df_xauusd[col].astype('float64')

    # Change dataype of df_forex
    df_forex["datetime"] = pd.to_datetime(df_xauusd["datetime"], format='%d-%b-%Y, %H:%M:%S')
    df_forex['currency'] = df_forex['currency'].astype('category')
    df_forex['impact'] = df_forex['impact'].astype('category')
    df_forex['event'] = df_forex['event'].astype('category')

    # Define function to handle various nember formats i.e. 100K 50%
    def handle_number_format(number: str) -> list:
        """ Separate value and unit of given number formats
        
        Arg:
            1. number: str i.e. 6.5%, 100K, 2.8

        Out:
            1. list: <[float, str | None]> i.e. [6.5, "%"], [100, "K"], [2.8, None]
        """

        # case 1: na
        if number == '':
            return [None, None]
        number = str(number)
        # case 2: % value
        if (number[-1] == '%') & (number.lstrip('-')[0].isnumeric() is True):
            return [float(number.rstrip('%')), '%']
        # case 3: 1K 1M 1B 1T unit
        if (number[-1].isalpha() is True) & (number.lstrip('-')[0].isnumeric() is True):
            return [float(str(number)[:-1]), number[-1]]
        # case 4: ordinary numbers
        if number.replace(',', '').replace('.', '').lstrip('-').isnumeric() is True:
            return [float(number.replace(',', '')), None]
        # case 5: non-numbers
        return [number, None]

    # Apply data format function
    for col in df_forex.columns[5:]:
        df_forex[col] = df_forex[col].fillna('').apply(handle_number_format)

    return df_xauusd, df_forex


# Function for plot candlestick chart
def candlestick_chart(df_xauusd):
    """ Plot candlestick chart

    Args:
    1. df_xauusd DataFrame
    2. df_forex DataFrame

    Out:
    1. .png image of candlestick chart parsed by week
    """

    # create new DataFrame
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    # create candlestick features
    ## 1. bullish-bearish color
    df_xauusd['bb'] = df_xauusd['%Change'].apply(
        lambda x: C_BULL if x >= 0 else C_BEAR)

    ## 2.candle-wick patterns xauusd
    df_xauusd['candle'] = df_xauusd[['open', 'high', 'low', 'close']].apply(
        lambda x: sorted(x)[2] - sorted(x)[1], axis=1)
    df_xauusd['w+'] = df_xauusd[['open', 'high', 'low', 'close']].apply(
        lambda x: sorted(x)[3] - sorted(x)[2], axis=1)
    df_xauusd['w-'] = df_xauusd[['open', 'high', 'low', 'close']].apply(
        lambda x: sorted(x)[0] - sorted(x)[1], axis=1)
    df_xauusd['bottom'] = df_xauusd[['open', 'high', 'low', 'close']].apply(
        lambda x: sorted(x)[1], axis=1)
    df_xauusd['upper'] = df_xauusd[['open', 'high', 'low', 'close']].apply(
        lambda x: sorted(x)[2], axis=1)
    
    # Setting width of candlestick elements
    width_candle = .03
    width_wick = .003

    # Plotting df_xauusd prices of the stock
    ax.bar(df_xauusd.datetime, df_xauusd['candle'], width_candle,
           bottom=df_xauusd['bottom'], color=df_xauusd['bb'])
    ax.bar(df_xauusd.datetime, df_xauusd['w+'], width_wick,
           bottom=df_xauusd['upper'], color=df_xauusd['bb'])
    ax.bar(df_xauusd.datetime, df_xauusd['w-'], width_wick,
           bottom=df_xauusd['bottom'], color=df_xauusd['bb'])

    # Format ticks
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=(0, 6, 12, 18)))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    ax.xaxis.grid(True, which='minor')
    ax.yaxis.grid(True)

    ax.tick_params(axis="x", which="major", pad=0)

    plt.xticks(**C_FONT)
    plt.xticks(minor=True, **C_FONT)
    plt.yticks(**C_FONT)

    ax.set_xlabel('Datetime (24H UTC+7)', **L_FONT)
    ax.set_ylabel('Price (USD)', **L_FONT)

    # Format spines and grid
    ax.spines[['right']].set_visible(False)
    ax.spines[['top']].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(True)
    
    # Save figure
    f_name = f'{ROOT}candle_{df_xauusd.iloc[0, 0].strftime("%y_%U")}.png'
    plt.savefig(f_name)

    return 0


# Function for parsing DataFrame weekly
def parse_data(df_xauusd, df_forex):
    """ Parse xauusd and forex data weekly

    Args:
    1. df_xauusd DataFrame
    2. df_forex DataFrame

    Out:
    1. list of weekly parsed df_xauusd DataFrame
    2. list of weekly parsed df_forex DataFrame
    """

    # Get first day in xauusd DataFrame
    origin_date = df_xauusd.iloc[0, 0]
    terminal_date = df_xauusd.iloc[-1, 0]

    # Get first and last days of the first week
    week_start = origin_date - dt.timedelta(days=origin_date.weekday()) # time 05:00:00
    week_end = week_start + dt.timedelta(days=6) # time 05:00:00

    # Parse weekly
    week_delta = dt.timedelta(weeks=1)

    # List of weekly parsed data
    parse_xauusd = []

    # Loop parsing weekly
    while week_start < terminal_date:
        # Append parsed DataFrame
        parse_xauusd.append(
            df_xauusd[(df_xauusd.datetime >= week_start) & (df_xauusd.datetime < week_end)]
        )

        # Increment week day interval
        week_start += week_delta
        week_end += week_delta
    
    return parse_xauusd


# Run this module
if __name__ == '__main__':
    print("Initiating...")
    # Path of two datasets
    PATH_XAUUSD = '/workspaces/Enterprise/03_Analytics/input/XAUUSD-1H_220103_230503.csv'
    PATH_FOREX = '/workspaces/Enterprise/03_Analytics/input/FOREX_311222_131020.csv'

    # Get DataFrame
    DF_XAUUSD, DF_FOREX = prepare_data(PATH_XAUUSD, PATH_FOREX)

    # Parse date
    parse_xauusd = parse_data(DF_XAUUSD, DF_FOREX)

    print("Rendering images...")
    count = 0
    for parse_df in tqdm(parse_xauusd):
        candlestick_chart(parse_df)
        count += 1

    print("Successfully render {count} images...")
