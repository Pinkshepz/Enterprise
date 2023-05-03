"""Essential functions for reading candlestick images

    Functions:
    1. highlight_candlestick(img_list: list) -> dict
    2. interpret_candlestick(candlestick_polymerase: dict, initial_time: tuple) -> dict
    3. calibrate_candlestick(candlestick: dict, **calibrated_candlestick_param) -> dict:
    
"""
# Import libraries
import numpy as np
import pandas as pd
import datetime as dt

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


def interpret_candlestick(candlestick_polymerase: dict, initial_time: tuple) -> dict:
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
    initial_time = dt.datetime(2023, 4, 17, 17, 00, 00)
    delta_time = dt.timedelta(hours=1)

    def next_datetime(time, dt=delta_time):
        """Forward candlestick time"""
        while True:
            time += dt
            # XAU market close -> SAT 05.00 - MON 04.00
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
                                        "close": candlestick_polymerase[position][1] + candlestick_polymerase[position][0],
                                        "type": "bullish"}
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
                                        "close": candlestick_polymerase[position][1],
                                        "type": "bearish"}
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


def calibrate_candlestick(candlestick: dict,
                          calibrated_candlestick_time: dt.datetime,
                          calibrated_candlestick_open: float,
                          calibrated_candlestick_high: float,
                          calibrated_candlestick_low: float,
                          calibrated_candlestick_close: float) -> dict:

    # Calibrate candlestick price
    c_date = dt.datetime(2023, 4, 19, 20, 00, 00)
    c_open = 1980.20
    c_high = 1992.90
    c_low = 1978.90
    c_close = 1990.55

    # Get non-calibrated price from candlestick
    non_calibrated_value = candlestick[calibrated_candlestick_time]
    candle_price_per_pixel = abs(calibrated_candlestick_open - calibrated_candlestick_close) / \
        abs(non_calibrated_value["open"] - non_calibrated_value["close"])
    wick_price_per_pixel = abs(calibrated_candlestick_high - calibrated_candlestick_low) / \
        abs(non_calibrated_value["high"] - non_calibrated_value["low"])
    price_per_pixel = (candle_price_per_pixel + wick_price_per_pixel) / 2

    # Calculate price
    def calibrate_price(pixel: float,
                        price_per_pixel=price_per_pixel,
                        exp_pixel=non_calibrated_value["open"],
                        exp_price=calibrated_candlestick_open) -> float:
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

    return candlestick
