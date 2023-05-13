"""Essential functions for reading candlestick images

    Functions:
    1. highlight_candlestick(img_list: list) -> dict
    2. interpret_candlestick(candlestick_polymerase: dict, initial_time: tuple) -> dict
    3. calibrate_candlestick(candlestick: dict, **calibrated_candlestick_param) -> dict
    4. candlestick_reader(path_input: str, img_input: list, csv_input: str) -> dict
    
"""

# Import libraries
import numpy as np
import pandas as pd
import datetime as dt
from PIL import Image


def highlight_candlestick(img_list: list) -> dict:
    """Recognize bull and bear candlestick
        Bull -> R - G < -10 & R + G > 200 -> +1
        Bear -> R + G > 10 & R + G > 200 -> -1
        Store [count of +1/-1 score, lowest point that contain +1/-1] of each column

        Parameters:
        1. img_list = 3D list of image pixels (jpeg: rgb, png: rgba)

        Output:
        1. CANDLESTICK POLYMERASE = dict(pixel no. horizontally: 
            count of +1/-1 score, 
            lowest point that contain +1/-1 of each column)
    """

    CANDLESTICK_POLYMERASE = {}  # {w: [count, lowest_point]}
    for h in np.arange(len(img_list)):
        for w in np.arange(len(img_list[h])):
            r = img_list[h][w][0]
            g = img_list[h][w][1]
            if (r + g > 200) & (r - g < -10):
                if w in CANDLESTICK_POLYMERASE:
                    CANDLESTICK_POLYMERASE[w][0] += 1
                    CANDLESTICK_POLYMERASE[w][1] = len(img_list[h]) - h - 1
                else:
                    CANDLESTICK_POLYMERASE[w] = [1, len(img_list[h]) - h - 1]
            elif (r + g > 200) & (r - g > 10):
                if w in CANDLESTICK_POLYMERASE:
                    CANDLESTICK_POLYMERASE[w][0] -= 1
                    CANDLESTICK_POLYMERASE[w][1] = len(img_list[h]) - h - 1
                else:
                    CANDLESTICK_POLYMERASE[w] = [-1, len(img_list[h]) - h - 1]
            else:
                if w not in CANDLESTICK_POLYMERASE:
                    CANDLESTICK_POLYMERASE[w] = [0, 0]

    # Sort CANDLESTICK_POLYMERASE keys
    CANDLESTICK_POLYMERASE = ({k: v for k, v in sorted(
        CANDLESTICK_POLYMERASE.items(), key=lambda item: item[0])})

    return CANDLESTICK_POLYMERASE


def interpret_candlestick(candlestick_polymerase: dict, initial_time: dt.datetime, excluded_time: list) -> dict:
    """Interpret candlestick pixel value (open, high, low, close)

    Parameters:
    1. candlestick_polymerase = dict(pixel no. horizontally: 
        count of +1/-1 score, 
        lowest point that contain +1/-1 of each column)

    Output:
    1. CANDLESTICK = dict(date (datetime64: YY MM DD HH mm):
        open: float,
        high: float,
        low: float,
        close: float)
"""

    CANDLESTICK = {}  # {date: [open, high, low, close]}

    # Manage datetime
    # datetime(year, month, day, hour, minute, second)
    DELTA_TIME = dt.timedelta(hours=1)

    def next_datetime(time: dt.datetime, excluded_time=excluded_time, dt=DELTA_TIME):
        """Forward candlestick time"""
        while True:
            time += dt
            if time in excluded_time:
                continue
            # XAU market close -> [SAT 05.00 - MON 04.00]
            if (time.weekday() in [1, 2, 3, 4]) | ((time.weekday() == 5) & (time.hour < 5)) | ((time.weekday() == 0) & (time.hour > 4)):
                break
        return time

    candle_time = initial_time
    position = 0

    while position < len(candlestick_polymerase):
        # Find candle (count != 0)
        if candlestick_polymerase[position][0] > 0:  # Bullish candle
            CANDLESTICK[candle_time] = {"open": candlestick_polymerase[position][1],
                                        "high": candlestick_polymerase[position][1] + candlestick_polymerase[position][0],
                                        "low": candlestick_polymerase[position][1],
                                        "close": candlestick_polymerase[position][1] + candlestick_polymerase[position][0]}
            position += 1
            temp_high = CANDLESTICK[candle_time]["high"]
            temp_low = CANDLESTICK[candle_time]["low"]
            while position < len(candlestick_polymerase):
                if candlestick_polymerase[position][0] == 0:
                    break
                if (temp_high != candlestick_polymerase[position][1] + candlestick_polymerase[position][0]) | (temp_low != candlestick_polymerase[position][1]):
                    CANDLESTICK[candle_time]["high"] = candlestick_polymerase[position][1] + \
                        candlestick_polymerase[position][0]
                    CANDLESTICK[candle_time]["low"] = candlestick_polymerase[position][1]
                position += 1
            candle_time = next_datetime(candle_time)
        elif candlestick_polymerase[position][0] < 0:  # Bearish candle
            CANDLESTICK[candle_time] = {"open": candlestick_polymerase[position][1] - candlestick_polymerase[position][0],
                                        "high": candlestick_polymerase[position][1] - candlestick_polymerase[position][0],
                                        "low": candlestick_polymerase[position][1],
                                        "close": candlestick_polymerase[position][1]}
            position += 1
            temp_high = CANDLESTICK[candle_time]["high"]
            temp_low = CANDLESTICK[candle_time]["low"]
            while position < len(candlestick_polymerase):
                if candlestick_polymerase[position][0] == 0:
                    break
                if (temp_high != candlestick_polymerase[position][1] - candlestick_polymerase[position][0]) | (temp_low != candlestick_polymerase[position][1]):
                    CANDLESTICK[candle_time]["high"] = candlestick_polymerase[position][1] - \
                        candlestick_polymerase[position][0]
                    CANDLESTICK[candle_time]["low"] = candlestick_polymerase[position][1]
                position += 1
            candle_time = next_datetime(candle_time)
        position += 1

    return CANDLESTICK


def calibrate_candlestick(candlestick: dict, calibrated_candlestick_values: dict) -> dict:
    """Calibrate candlesitck value by calculate pixels to price"""

    # Get non-calibrated price from candlestick
    non_calibrated_value = candlestick[calibrated_candlestick_values["calibrated_time"].to_pydatetime(
    )]
    candle_price_per_pixel = abs(calibrated_candlestick_values["calibrated_open"] - calibrated_candlestick_values["calibrated_close"]) / \
        abs(non_calibrated_value["open"] - non_calibrated_value["close"])
    wick_price_per_pixel = abs(calibrated_candlestick_values["calibrated_high"] - calibrated_candlestick_values["calibrated_low"]) / \
        abs(non_calibrated_value["high"] - non_calibrated_value["low"])
    price_per_pixel = (candle_price_per_pixel + wick_price_per_pixel) / 2

    # Calculate price
    def calibrate_price(pixel: float,
                        price_per_pixel=price_per_pixel,
                        exp_pixel=non_calibrated_value["open"],
                        exp_price=calibrated_candlestick_values["calibrated_open"]) -> float:
        """Calculate price from pixel"""

        return exp_price - ((exp_pixel-pixel)*price_per_pixel)

    for candlestick_date in candlestick.keys():
        candlestick[candlestick_date]["open"] = round(
            calibrate_price(candlestick[candlestick_date]["open"]), 2)
        candlestick[candlestick_date]["high"] = round(
            calibrate_price(candlestick[candlestick_date]["high"]), 2)
        candlestick[candlestick_date]["low"] = round(
            calibrate_price(candlestick[candlestick_date]["low"]), 2)
        candlestick[candlestick_date]["close"] = round(
            calibrate_price(candlestick[candlestick_date]["close"]), 2)

    # Error should be less than 1%
    error = abs(candle_price_per_pixel - wick_price_per_pixel) * \
        100 / candle_price_per_pixel
    if error > 1:
        return (candlestick, (error, candle_price_per_pixel, wick_price_per_pixel))

    return (candlestick, None)


def candlestick_reader(path_input: str,
                       img_input: list,
                       batch_input: tuple,
                       csv_input: str,
                       excluded_time: list,
                       name: str,
                       path_output: str) -> dict:
    """Read candlestick chart image and return csv file of price values

    Args:
        path_input (str): path of image folder
        img_input (list): list of input image file names
        batch_input (tuple): tuple of image file slicing
        csv_input (str): path to csv input file path
        excluded_time (list): list of holidays or other excluded time
        name (str): prefix of filename ({name}_{initial_date}_{final_date})
        path_output (str): path for output csv files

    Returns:
        csv file (.csv): column name: [
            index,date,time,currency,impact,event,actual,forecast,previous
        ]
    """

    print("----------INITIATING----------")
    # Adjust batch size not larger than existing input
    if batch_input[1] > len(img_input):
        batch_input[1] = len(img_input)

    img_input = img_input[batch_input[0]:batch_input[1]]
    CSV = pd.read_csv(csv_input)

    # Check image - CSV compatibility
    if (CSV.shape == 0) | (len(img_input) == 0):
        print("Error: CSV or image input are empty")
        return 1
    if CSV.shape == len(img_input):
        print("Error: Image files number are not equal to csv data")
        return 2

    print(f"There are {len(img_input)} images to process")
    print(*sorted(img_input))
    print("..............................")

    # Format datetime CSV dataframe
    CSV.iloc[:, 0] = pd.to_datetime(
        CSV.iloc[:, 0], format="%Y-%m-%d-%H")  # First-time
    CSV.iloc[:, 1] = pd.to_datetime(
        CSV.iloc[:, 1], format="%Y-%m-%d-%H")  # Last-time
    CSV.iloc[:, 2] = pd.to_datetime(
        CSV.iloc[:, 2], format="%Y-%m-%d-%H")  # Calibrated-time

    DFS_CANDLESTICK = {}  # {img_file: pd.DataFrame}

    for count, img_file in enumerate(sorted(img_input), start=batch_input[0]):
        print(f"Processing Image {img_file}")

        # Load the image and convert into list
        IMG = Image.open(str(path_input) + str(img_file))
        IMG_LIST = np.asarray(IMG).tolist()

        CANDLESTICK_POLYMERASE = highlight_candlestick(IMG_LIST)
        CANDLESTICK = interpret_candlestick(
            CANDLESTICK_POLYMERASE, CSV.iloc[count, 0], excluded_time)
        
        # Check last candlestick
        if list(CANDLESTICK.keys())[-1] != CSV.iloc[count, 1]:
            print("Error: Last candlestick date ({0} to {1}) is not corresponded to CSV ({2})".format(
                list(CANDLESTICK.keys())[0],
                list(CANDLESTICK.keys())[-1],
                CSV.iloc[count, 1]))

        CALIBRATED_CANDLESTICK = calibrate_candlestick(
            CANDLESTICK, CSV.iloc[count, 2:])
        
        # Check calibrate accuracy
        if CALIBRATED_CANDLESTICK[-1] != None:
            print("Error: Fail to calibrate due to high error at {0}% > 0.5% at file {1}. Ref: {2}".format(
                CALIBRATED_CANDLESTICK[-1][0], img_file, CALIBRATED_CANDLESTICK[-1][1:]))

        # Convert into pd.DataFrame
        DF_CANDLESTICK = pd.DataFrame(CALIBRATED_CANDLESTICK[0]).transpose(
        ).reset_index().rename(columns={'index': 'time'})

        # Convert dt.datetime to string
        DF_CANDLESTICK.time = DF_CANDLESTICK.time.dt.strftime(
            '%d-%b-%Y, %H:%M:%S')

        # Store in dictionary
        DFS_CANDLESTICK[img_file] = DF_CANDLESTICK
        print(f"{len(CANDLESTICK)} candlesticks fetched")
        print("..............................")

    # Merge all DataFrames
    print("Merge and export files")
    DF_MERGE_CANDLESTICK = pd.concat(df for df in DFS_CANDLESTICK.values(
    )).drop_duplicates(subset=['time'], keep='first').reset_index(drop=True)

    # Add %Change row
    DF_MERGE_CANDLESTICK['%Change'] = round(
        100 * (DF_MERGE_CANDLESTICK['close'] - DF_MERGE_CANDLESTICK['open']) / DF_MERGE_CANDLESTICK['open'], 4)

    # Export csv file
    NAME_DATE = CSV.iloc[batch_input[0], 0].strftime("%y%m%d") + '_' + CSV.iloc[batch_input[1] - 1, 1].strftime("%y%m%d")
    DF_MERGE_CANDLESTICK.to_csv((path_output + name + '_' + NAME_DATE + '.csv'),
                                sep=',',
                                encoding='utf-8')

    print(f"{len(DF_MERGE_CANDLESTICK)} candlesticks are successfully exported")
    print("----------COMPLETED-----------")

    return DFS_CANDLESTICK
