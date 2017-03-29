# don't forget: source secret.sh

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']
