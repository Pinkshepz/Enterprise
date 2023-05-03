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

# Get file path
PATH_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//image//"
# PATH_INPUT = "/workspaces/Enterprise/02_Candlestick/input/image/"
FILE_INPUT = next(os.walk(PATH_INPUT), (None, None, []))[2]

CSV_INPUT = "c://Users//Art//Documents//A1-AspirePC//CS Project//07_Enterprise//Enterprise//02_Candlestick//input//candlestick_parameters.csv"
CSV_INPUT = "workspaces/Enterprise/02_Candlestick/input/candlestick_parameters.csv"

# Read csv
CSV = np

print("There are {0} images to process".format(len(FILE_INPUT)))

for IMG_FILE in FILE_INPUT:
    



# load the image and convert into list
IMG = Image.open(PATH_INPUT + FILE_INPUT[0])
IMG_LIST = np.asarray(IMG).tolist()

cf.highlight_candlestick(IMG_LIST)

