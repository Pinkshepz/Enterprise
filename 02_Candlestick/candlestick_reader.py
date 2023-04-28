"""Compute candlestick chart into tabular format"""

# Import libraries
from PIL import Image
from numpy import asarray

path = "02_Candlestick/input/01.jpeg"
# load the image and convert into np.array
img = Image.open(path)

# asarray() class is used to convert
# PIL images into NumPy arrays
numpydata = asarray(img)

# <class 'numpy.ndarray'>
print(type(numpydata))

#  shape
print(numpydata.shape)
