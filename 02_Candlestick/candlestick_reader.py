"""Compute candlestick chart into tabular format

    Parameters:
    1. input_folder = directory to images
    2. csv file containing
        first_candlestick_time = YY MM DD HH mm
        calibrated_candlestick_time = YY MM DD HH mm
        calibrated_candlestick_open = float
        calibrated_candlestick_high = float
        calibrated_candlestick_low = float
        calibrated_candlestick_close = float
    
    Output:
    1. csv file containing
        candlestick_time = YY MM DD HH mm
        candlestick_open = float
        candlestick_high = float
        candlestick_low = float
        candlestick_close = float
"""

# Import libraries
import os
import datetime as dt
import candlestick_function

# Read input file
# Image
# PATH_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//image//"
PATH_INPUT = "/workspaces/Enterprise/02_Candlestick/input/image/"
IMG_INPUT = sorted(next(os.walk(PATH_INPUT), (None, None, []))[2])

# CSV Tabular
# CSV_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//candlestick_parameters.csv"
CSV_INPUT = "/workspaces/Enterprise/02_Candlestick/input/candlestick_parameters.csv"

PATH_OUTPUT = "/workspaces/Enterprise/02_Candlestick/output/"

excluded_time = [
    dt.datetime(year=2022, month=1, day=10, hour=5),
    dt.datetime(year=2022, month=3, day=19, hour=4),
    dt.datetime(year=2022, month=4, day=15, hour=16),
    dt.datetime(year=2022, month=4, day=15, hour=17),
    dt.datetime(year=2022, month=4, day=15, hour=18),
    dt.datetime(year=2022, month=4, day=15, hour=19),
    dt.datetime(year=2022, month=4, day=15, hour=21),
    dt.datetime(year=2022, month=4, day=15, hour=22),
    dt.datetime(year=2022, month=4, day=16, hour=0),
    dt.datetime(year=2022, month=4, day=16, hour=1),
    dt.datetime(year=2022, month=4, day=16, hour=3),
    dt.datetime(year=2022, month=4, day=16, hour=4),
    dt.datetime(year=2022, month=4, day=30, hour=4),
    dt.datetime(year=2022, month=5, day=14, hour=4),
    dt.datetime(year=2022, month=5, day=28, hour=4),
    dt.datetime(year=2022, month=5, day=31, hour=3),
    dt.datetime(year=2022, month=5, day=31, hour=4),
    dt.datetime(year=2022, month=7, day=5, hour=2),
    dt.datetime(year=2022, month=7, day=30, hour=4),
    dt.datetime(year=2022, month=11, day=28, hour=5),
    dt.datetime(year=2022, month=12, day=26, hour=9),
    dt.datetime(year=2022, month=12, day=26, hour=13),
    dt.datetime(year=2022, month=12, day=26, hour=16),
    dt.datetime(year=2022, month=12, day=26, hour=17),
    dt.datetime(year=2022, month=12, day=26, hour=19),
    dt.datetime(year=2022, month=12, day=26, hour=20),
    dt.datetime(year=2022, month=12, day=26, hour=21),
    dt.datetime(year=2022, month=12, day=26, hour=22),
    dt.datetime(year=2022, month=12, day=27, hour=0),
    dt.datetime(year=2022, month=12, day=27, hour=2),
    dt.datetime(year=2022, month=12, day=27, hour=3),
    dt.datetime(year=2023, month=1, day=2, hour=7),
    dt.datetime(year=2023, month=1, day=2, hour=9),
    dt.datetime(year=2023, month=1, day=2, hour=13),
    dt.datetime(year=2023, month=1, day=2, hour=17),
    dt.datetime(year=2023, month=1, day=2, hour=19),
    dt.datetime(year=2023, month=1, day=2, hour=20),
    dt.datetime(year=2023, month=1, day=2, hour=23),
    dt.datetime(year=2023, month=1, day=3, hour=0),
    dt.datetime(year=2023, month=1, day=3, hour=2),
    dt.datetime(year=2023, month=1, day=3, hour=3),
    dt.datetime(year=2023, month=1, day=3, hour=4),
    dt.datetime(year=2023, month=2, day=21, hour=3),
    dt.datetime(year=2023, month=2, day=21, hour=4),
    dt.datetime(year=2023, month=2, day=21, hour=5),
    dt.datetime(year=2023, month=4, day=1, hour=4),
    dt.datetime(year=2023, month=4, day=7, hour=5),
    dt.datetime(year=2023, month=4, day=7, hour=6),
    dt.datetime(year=2023, month=4, day=7, hour=7),
    dt.datetime(year=2023, month=4, day=7, hour=8),
    dt.datetime(year=2023, month=4, day=7, hour=9),
    dt.datetime(year=2023, month=4, day=7, hour=10),
    dt.datetime(year=2023, month=4, day=7, hour=13),
    dt.datetime(year=2023, month=4, day=7, hour=14),
    dt.datetime(year=2023, month=4, day=7, hour=15),
    dt.datetime(year=2023, month=4, day=7, hour=16),
    dt.datetime(year=2023, month=4, day=7, hour=17),
    dt.datetime(year=2023, month=4, day=7, hour=18),
    dt.datetime(year=2023, month=4, day=7, hour=20),
    dt.datetime(year=2023, month=4, day=7, hour=21),
    dt.datetime(year=2023, month=4, day=7, hour=22),
    dt.datetime(year=2023, month=4, day=7, hour=23),
    dt.datetime(year=2023, month=4, day=8, hour=0),
    dt.datetime(year=2023, month=4, day=8, hour=1),
    dt.datetime(year=2023, month=4, day=8, hour=2),
    dt.datetime(year=2023, month=4, day=8, hour=3),
]

# Config batch size
BATCH_SIZE = 100
BATCH_NO = 0
INITIAL = 0 + (BATCH_SIZE * BATCH_NO)
FINAL = BATCH_SIZE + (BATCH_SIZE * BATCH_NO)
BATCH_INPUT = [INITIAL, FINAL]

candlestick_function.candlestick_reader(path_input=PATH_INPUT,
                                        img_input=IMG_INPUT,
                                        batch_input=BATCH_INPUT,
                                        csv_input=CSV_INPUT,
                                        excluded_time=excluded_time,
                                        name="XAUUSD-1H",
                                        path_output=PATH_OUTPUT)
