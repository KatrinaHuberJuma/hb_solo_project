# don't forget: source secret.sh

# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Cohort, Student, Lab, Pair

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']


@app.route("/", methods=["GET"])
def homepage():
    """Show homepage"""

    return render_template("home.html")

@app.route("/", methods=["POST"])
def homepage_post():
    """Handle the signin form inputs"""

    name = request.form.get("name")
    email = request.form.get("email")

    valid_user = Student.query.filter((Student.name == name)
                                    & (Student.email == email)).first()

    print "\n\n\n", name, "\n\n\n", email, "\n\n\n", valid_user, "\n\n\n"

    if valid_user:
        user = Student.query.filter(Student.name == name).first()
        session["user_id"] = user.student_id
        session["cohort_id"] = user.cohort_id

        print session["user_id"], session["cohort_id"]

        flash("You are logged in now.")
    else: 
        flash("invalid login")
        return redirect("/signin")

    return render_template("home.html")


@app.route("/signin")
def signinpage():
    """Show signin"""

    # TODO: if not signed in, redirect to signin page

    return render_template("signin.html")


if __name__ =="__main__":

    app.debug = True # fixme before deployment
    app.jinja_env.auto_reload = app.debug # fixme before deployment

    connect_to_db(app, "postgresql:///katfuntest")

    DebugToolbarExtension(app) # fixme before deployment

    app.run(port=5000, host='0.0.0.0')