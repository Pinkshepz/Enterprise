# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import datetime as dt
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

# Path of two datasets
PATH_XAUUSD = '/workspaces/Enterprise/03_Analytics/input/XAUUSD-1H_220103_230503.csv'
PATH_FOREX = '/workspaces/Enterprise/03_Analytics/input/FOREX_311222_131020.csv'

# Read csv
DF_XAUUSD = pd.read_csv(PATH_XAUUSD, parse_dates=['time']).drop(columns=['Unnamed: 0'])
DF_FOREX = pd.read_csv(PATH_FOREX, parse_dates=[['date', 'time']]).drop(columns=['Unnamed: 0'])

DF_XAUUSD.rename(columns={'time': 'datetime'}, inplace=True)
DF_FOREX.rename(columns={'date_time': 'datetime'}, inplace=True)

# Change dataype of DF_XAUUSD
for col in DF_XAUUSD.columns[1:]:
    DF_XAUUSD[col] = DF_XAUUSD[col].astype('float64')

# Change dataype of DF_FOREX
DF_FOREX["datetime"] = pd.to_datetime(DF_XAUUSD["datetime"], format='%d-%b-%Y, %H:%M:%S')
DF_FOREX['currency'] = DF_FOREX['currency'].astype('category')
DF_FOREX['impact'] = DF_FOREX['impact'].astype('category')
DF_FOREX['event'] = DF_FOREX['event'].astype('category')

# Define function to handle various nember formats i.e. 100K 50%
def handle_number_format(number: str) -> list:
    """ Separate value and unit of given number formats
    
    Arg:
        1. number: str i.e. 6.5%, 100K, 2.8

    Out:
        1. list: <[float, str | None]> i.e. [6.5, "%"], [100, "K"], [2.8, None]
 
    This is a cat -> 🐈
    """

    # case 1: na
    if number == '':
        return [None, None]
    number = str(number)
    # case 2: % value
    if (number[-1] == '%') & (number.lstrip('-')[0].isnumeric() == True):
        return [float(number.rstrip('%')), '%']
    # case 3: 1K 1M 1B 1T unit
    if (number[-1].isalpha() == True) & (number.lstrip('-')[0].isnumeric() == True):
        return [float(str(number)[:-1]), number[-1]]
    # case 4: ordinary numbers
    if number.replace(',', '').replace('.', '').lstrip('-').isnumeric() == True: 
        return [float(number.replace(',', '')), None]
    # case 5: non-numbers
    return [number, None]

# Apply data format function
for col in DF_FOREX.columns[5:]:
    DF_FOREX[col] = DF_FOREX[col].fillna('').apply(handle_number_format)

# Function for plot candlestick chart
def candlestick(df_price):
    # Matplotlib figure
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    # Up stores bullish candles and down stores bearish candles
    up = df_price[df_price.close >= df_price.open]
    down = df_price[df_price.close < df_price.open]
    
    # Setting width of candlestick elements
    width = .7
    width2 = .07
    
    # Plotting bullish candles
    ax.bar(up.index, up.close-up.open, width, bottom=up.open, color=C_BULL) # candle
    ax.bar(up.index, up.high-up.close, width2, bottom=up.close, color=C_BULL) # upper wick
    ax.bar(up.index, up.low-up.open, width2, bottom=up.open, color=C_BULL) # lower wick
    
    # Plotting bearish candles
    ax.bar(down.index, down.close-down.open, width, bottom=down.open, color=C_BEAR) # candle
    ax.bar(down.index, down.high-down.open, width2, bottom=down.open, color=C_BEAR) # upper wick
    ax.bar(down.index, down.low-down.close, width2, bottom=down.close, color=C_BEAR) # lower wick
    
    # Format charts
    plt.xticks(**C_FONT)
    plt.yticks(**C_FONT)
    ax.set_xlabel('Time (24 Hours)', **L_FONT)
    ax.set_xticks(np.arange(0, 24, 2))
    ax.set_xlim([0, 23])
    ax.set_ylabel('Price (USD)', **L_FONT)
    ax.grid(True)
    
    # Save figure
    f_name = f'ROOT{df_price.iloc[0, 0].strftime("%y%m%d")}_price.png'
    plt.savefig(f_name)

    return 0

# Loop on each column to export candlestick chart image and tabular csv
