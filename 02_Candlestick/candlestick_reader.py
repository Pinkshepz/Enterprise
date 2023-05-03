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
import numpy as np
import pandas as pd
from PIL import Image
import datetime as dt

import candlestick_function as cf

# Read input file
# Image
PATH_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//image//"
# PATH_INPUT = "/workspaces/Enterprise/02_Candlestick/input/image/"
IMG_INPUT = next(os.walk(PATH_INPUT), (None, None, []))[2]
# CSV Tabular
CSV_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//candlestick_parameters.csv"
# CSV_INPUT = "workspaces/Enterprise/02_Candlestick/input/candlestick_parameters.csv"
    
cf.candlestick_reader(PATH_INPUT, IMG_INPUT, CSV_INPUT)
