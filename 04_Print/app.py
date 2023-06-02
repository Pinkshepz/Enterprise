import os
from flask import Flask,render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    return render_template("index.html", content_pages=[1, 2, 3, 4, 5])
