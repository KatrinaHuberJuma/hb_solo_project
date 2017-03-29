# don't forget: source secret.sh

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']


@app.route("/")
def homepage():
    """Show homepage"""

    # TODO: if not signed in, redirect to signin page

    return render_template("home.html")


@app.route("/signin")
def signinpage():
    """Show homepage"""

    # TODO: if not signed in, redirect to signin page

    return render_template("signin.html")


if __name__ =="__main__":

    app.run(port=5000, host='0.0.0.0')