"""Module containing decorators for formatting Matplotlib charts in my favorite design"""

# Imports
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Add fonts
font_dirs = ["00_Pinksheepkit/fonts/poppins"]
font_files = fm.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    fm.fontManager.addfont(font_file)

# plt.rcParams['font.family'] = 'My Custom Font'

print("Matplotkit is successfully configured")
