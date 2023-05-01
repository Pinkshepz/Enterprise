"""Module containing decorators for formatting Matplotlib charts in my favorite design"""

# Imports
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Configure fonts
FONT_PATH = "/workspaces/Enterprise/00_Pinksheepkit/fonts/poppins/Poppins-{0}.ttf"
HEADING = "Bold"
LABEL = "Regular"
CONTENT = "Light"

h_font = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(HEADING)),
          "size": 12}
l_font = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(LABEL)),
          "size": 10}
c_font = {"fontproperties": fm.FontProperties(fname=FONT_PATH.format(CONTENT)),
          "size": 8}

# alpha decorator (Simple two-axis charts)
def alpha_format(function):
    """Alpha decorator (Simple two-axis charts) accept 3 arguments: title, x_label, y_label"""
    def wrapper(title, x_label, y_label): # title, x_label, y_label
        fig, ax = function()
        plt.rcParams['figure.dpi'] = 100
        ax.spines[['right', 'top']].set_visible(False)
        ax.set_title(title, **h_font)
        ax.set_xlabel(x_label, **l_font)
        ax.set_ylabel(y_label, **l_font)
        for label in ax.get_xticklabels():
            label.set_fontproperties(c_font)
        for label in ax.get_yticklabels():
            label.set_fontproperties(c_font)
        plt.show()
        return fig, ax
    return wrapper
