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
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from tqdm import tqdm

# Configure fonts
FONT_PATH = "/workspaces/Enterprise/00_Pinksheepkit/fonts/poppins/Poppins-{0}.ttf"
HEADING = "Bold"
LABEL = "Medium"
CONTENT = "Regular"

# Font properties **kwargs -> usage: plt.some_method(**H_FONT)
H_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(HEADING)), "size": 12}
L_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(LABEL)), "size": 10}
C_FONT = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(CONTENT)), "size": 8}

# color palattes for candlestick chart
C_BULL = "#51A299"
C_BEAR = "#DD5E57"
C_SLATE500 = '#64748B'

C_LOW = "#EAB308"
C_MEDIUM = "#F97316"
C_HIGH = "#EF4444"

# Configure pandas and matplotlib settings
pd.options.mode.chained_assignment = None  # default='warn'
mpl.rcParams['grid.color'] = '#f0f0f0'
plt.rcParams['figure.dpi'] = 300

# Root path
ROOT = '/workspaces/Enterprise/04_Print/static/data/'

# Function for data preparation and cleaning to DataFrame
def prepare_data(path_xauusd: str, path_forex: str) -> tuple:
    """ Prepare and clean DataFrame 

    Args
    1. XAUUSD.csv path
    2. FOREX.csv path

    Out
    1. pd.DataFrame of XAUUSD
    2. pd.DataFrame of FOREX
    """

    # Read csv
    df_xauusd = pd.read_csv(path_xauusd, parse_dates=['time']).drop(columns=['Unnamed: 0'])
    df_forex = pd.read_csv(path_forex, parse_dates=[['date', 'time']]).drop(columns=['Unnamed: 0'])
    df_forex = df_forex[df_forex['currency'] == 'USD']

    df_xauusd.rename(columns={'time': 'datetime'}, inplace=True)
    df_forex.rename(columns={'date_time': 'datetime'}, inplace=True)

    # Change dataype of df_xauusd
    for col in df_xauusd.columns[1:]:
        df_xauusd[col] = df_xauusd[col].astype('float64')

    # Change dataype of df_forex
    df_forex["datetime"] = pd.to_datetime(df_xauusd["datetime"], format='%d-%b-%y %H:%M:%S')
    df_forex["date"] = df_forex["datetime"].dt.strftime('%d %b')
    df_forex["time"] = df_forex["datetime"].dt.strftime('%H:%M')
    df_forex['currency'] = df_forex['currency'].astype('category')
    df_forex['impact'] = df_forex['impact'].astype('category')
    df_forex['event'] = df_forex['event'].astype('category')

    # Filter out impact: holiday
    df_forex = df_forex[df_forex.impact != 'holiday']

    # Swap column order
    df_forex = df_forex.reindex(columns=["datetime", "date", "time", "impact", "event", "actual", "forecast", "previous"])

    return df_xauusd, df_forex


# Function for plot candlestick chart
def candlestick_chart(df_xauusd: pd.DataFrame, df_forex: pd.DataFrame) -> int:
    """ Plot candlestick chart

    Args:
    1. df_xauusd DataFrame
    2. df_forex DataFrame

    Out:
    1. .png image of candlestick chart parsed by week
    """

    # create new DataFrame
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))

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
    
    # Mark FOREX news impact
    impact_mapper_color = {'low': C_LOW, 'medium': C_MEDIUM, 'high': C_HIGH}
    ax.scatter(df_forex.datetime, [min(df_xauusd.low) - 1] * df_forex.shape[0], marker='s',
               s=20, c=df_forex.impact.map(impact_mapper_color), alpha=1)

    # Format ticks
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=(0, 6, 12, 18)))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    ax.xaxis.grid(True, which='minor')
    ax.yaxis.grid(True)

    ax.tick_params(axis="x", which="major", pad=3.3)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    plt.xticks(**C_FONT, color='#444')
    plt.xticks(minor=True, color='#777', **C_FONT)
    plt.yticks(**C_FONT,  color='#777')

    # ax.set_xlabel('Datetime (24H UTC+7)', **L_FONT)
    # ax.set_ylabel('Price (USD)', **L_FONT)

    # Format spines and grid
    ax.spines[['left']].set_visible(False)
    ax.spines[['right']].set_visible(False)
    ax.spines[['top']].set_visible(False)
    ax.spines[['bottom']].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(True)
    
    # Save and close figure
    f_name = f'{ROOT}candle_{df_xauusd.iloc[0, 0].strftime("%y_%U")}.png'
    plt.savefig(f_name, bbox_inches='tight')
    plt.close()

    return 0


# Function for exporting csv of forex html data table
def forex_html_csv(parse_forex: list) -> int:
    # List storing html of pd.DataFrame
    parse_html_forex = []

    # Loop over list of pd.DataFrame
    for parse_df in parse_forex:
        # Convert imapct to color code
        impact_html_mapper = {
            'low': f'<div class="square" style="background-color: {C_LOW};"></div>',
            'medium': f'<div class="square" style="background-color: {C_MEDIUM};"></div>', 
            'high': f'<div class="square" style="background-color: {C_HIGH};"></div>'}

        parse_df.impact = parse_df.impact.map(impact_html_mapper)

        # Rename columns
        parse_df.columns = ["Datetime", "Date", "Time", "IMP", "Event", "Actual", "Fore", "Prev"]

        # Convert to html
        html_forex = parse_df.iloc[:, 1:].to_html(index=False, escape=False) # Exclude datetime column

        # Adjust HTML
        # html_forex = html_forex.replace('"', '')
        html_forex = html_forex.replace("border", "b")
        html_forex = html_forex.replace("right", "left")

        parse_html_forex.append(html_forex)

    # Export .csv file
    f_name = f'{ROOT}forex_html.csv'
    pd.Series(parse_html_forex).to_csv(f_name)

    return 0


# Function for parsing DataFrame weekly
def parse_data(df_xauusd: pd.DataFrame, df_forex: pd.DataFrame) -> list:
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
    parse_forex = []

    # Use datetime range form candlestick chart as primary source
    # Left join (df_xauusd | df_forex)
   
    # Loop parsing weekly
    while week_start < terminal_date:
        # Append parsed DataFrame
        parse_xauusd.append(
            df_xauusd[(df_xauusd.datetime >= week_start) & (df_xauusd.datetime < week_end)]
        )
        parse_forex.append(
            df_forex[(df_forex.datetime >= week_start) & (df_forex.datetime < week_end)]
        )

        # Increment week day interval
        week_start += week_delta
        week_end += week_delta
    
    return parse_xauusd, parse_forex


# Run this module
if __name__ == '__main__':
    print("Initiating...")
    # Path of two datasets
    PATH_XAUUSD = '/workspaces/Enterprise/03_Analytics/input/XAUUSD-1H_220103_230503.csv'
    PATH_FOREX = '/workspaces/Enterprise/03_Analytics/input/FOREX_311222_131020.csv'

    # Get DataFrame
    DF_XAUUSD, DF_FOREX = prepare_data(PATH_XAUUSD, PATH_FOREX)

    # Parse date
    parse_xauusd, parse_forex = parse_data(DF_XAUUSD, DF_FOREX)

    # Render candlestick chart
    # print("Rendering images...")
    # for parse_df_xauusd, parse_df_forex in tqdm(zip(parse_xauusd, parse_forex)):
    #     candlestick_chart(parse_df_xauusd, parse_df_forex)

    # print("Successfully render images...")

    # Parse HTML of FOREX tabular data
    print("Parsing HTML...")
    forex_html_csv(parse_forex)

    print("Successfully parse html to csv")
