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

# Import fundamental libraries
import os

# Import datasci libraries
import datetime as dt
import numpy as np
import pandas as pd
from PIL import Image

import candlestick_function as cf

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
]

BATCH_SIZE = 5
BATCH_NO = 0
INITIAL = 0 + (BATCH_SIZE * BATCH_NO)
FINAL = BATCH_SIZE + (BATCH_SIZE * BATCH_NO)

cf.candlestick_reader(path_input=PATH_INPUT,
                      img_input=IMG_INPUT[INITIAL:FINAL],
                      csv_input=CSV_INPUT,
                      excluded_time=excluded_time,
                      name="XAUUSD",
                      path_output=PATH_OUTPUT)
