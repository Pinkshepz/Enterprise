""" Pandakit.py module

    Contains functions for facilitating pandas operation

    1. pdk.agg_count(df)
"""

# import
import pandas as pd

# 1. pdk.agg_count()
def agg_count(*args: object) -> list:
    """ function to group and count set of data from iterators 

    args:
    1. args[*iterators]: i.e. list, tuple, numpy.array, pandas.DataFrame

    out:
    1. [*iterators, count]: [all unique zip(*iterators), count]

    example:
    input: args[i1, i2, i3]     output: [i1, i2, i3, count]
    where i1 = [1, 3, 1, 4]
          i2 = [2, 5, 2, 6]
          i3 = [3, 7, 3, 8]

     i1   i2   i3               i1   i2   i3   count
     1    2    3                1    2    3    2
     3    5    7       -->      3    5    7    1
     1    2    3                4    6    8    1
     4    6    8

    """

    # create dataframe for all iterators
    df_iters = pd.DataFrame(*args).transpose()
    
    # group by item and agg by counting
    df_iters.groupby(df_iters.columns.tolist(),as_index=False).size()
