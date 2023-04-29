"""Compute candlestick chart into tabular format"""

# Import libraries
import os
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
import ast

# Get file path
PATH_INPUT = "02_Candlestick/input/"
FILE_INPUT = next(os.walk(PATH_INPUT), (None, None, []))[2]

# load the image and convert into np.array
IMG = Image.open(PATH_INPUT + FILE_INPUT[0])

# asarray() class is used to convert
# PIL images into NumPy arrays
IMG_ARR = asarray(IMG)

# Shape
HEIGHT, WIDTH, RGB = IMG_ARR.shape

# Check Color Profile
CHECK_COLOR_PROFILE = True

if CHECK_COLOR_PROFILE is True:
    color_profile = {}
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pixel = str(IMG_ARR[i][j])
            if pixel in color_profile:
                color_profile[pixel] += 1
            else:
                color_profile[pixel] = 1
    color_profile = ({k: v for k, v in sorted(color_profile.items(), key=lambda item: item[1])})

    fig, ax = plt.subplots()

    var_plot = color_profile[-10:-1]

    var_x = var_plot.keys()
    print(var_x)
    # var_count = var_plot.values()
    # var_colors = [(r / 255, g / 255, b / 255) for r, g, b in ast.literal_eval(var_x)]

    # ax.bar(var_x, var_y, label=bar_labels, color=bar_colors)

    # ax.set_ylabel('fruit supply')
    # ax.set_title('Fruit supply by kind and color')
    # ax.legend(title='Color')

    # plt.show()
