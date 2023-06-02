"""Python app for generating HTML pages"""

import glob
from pathlib import Path
import datetime as dt
from flask import Flask, render_template

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Define dict storing data of each page
page_dict = {}
candle_path = "/workspaces/Enterprise/04_Print/static/data/candle*.png"

for page, path in enumerate(sorted(glob.glob(candle_path, recursive=True))):
    try:
        # get file name and store file data in dict
        file_name = Path(path).stem
        year, week = file_name.split('_')[1], file_name.split('_')[2]
        start_date = dt.datetime.strptime(year + '-' + week + '-1', "%y-%U-%w").strftime('%d %b %y')
        end_date = (dt.datetime.strptime(year + '-' + week + '-1', '%y-%U-%w') + dt.timedelta(days=6)).strftime('%d %b %y')
        page_dict[page] = {'candle': file_name + '.png',
                           'year': year,
                           'week': week,
                           'start_date': start_date,
                           'end_date': end_date}

    # error case
    except FileNotFoundError as e:
        print(e)
        
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Index (main) page
@app.route("/", methods=["GET"])
def index():
    # Display data on index.html
    return render_template("index.html", content_pages=list(page_dict.items()))
