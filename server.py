# don't forget: source secret.sh

# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword

from flask import Flask, session, render_template, request, jsonify, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']


@app.route("/", methods=["GET"])
def homepage():
    """Show homepage"""

    if "cohort_id" in session:
        cohort_members = Student.query.filter(Student.cohort_id == session["cohort_id"]).all()

        return render_template("home.html", cohort_members=cohort_members)
    else:
        return redirect("/signin") #TODO

@app.route("/", methods=["POST"])
def homepage_post():
    """Handle the signin form inputs"""

    name = request.form.get("name")
    password = request.form.get("password")
    permissions = request.form.get("permissions")


    if permissions == "admin":
        valid_admin = Admin.query.filter((Admin.name == name)
                                        & (Admin.password == password)).first()

        if valid_admin:
            admin = valid_admin
            session["admin_id"] = admin.admin_id
            cohorts = Cohort.query.filter(Cohort.admin_id == admin.admin_id).all()
            
            flash("You are logged in now.")
            return render_template("home.html", cohorts=cohorts)

    elif permissions == "student":
        valid_student = Student.query.filter((Student.name == name)
                                        & (Student.password == password)).first()

        if valid_student:
            
            student = valid_student
            session["student_id"] = student.student_id
            session["cohort_id"] = student.cohort_id
            cohort_members = Student.query.filter(Student.cohort_id ==
                session["cohort_id"]).all()

            flash("You are logged in now.")
            return render_template("home.html", cohort_members=cohort_members)



    flash("invalid login")
    return redirect("/signin")



@app.route("/signin")
def signinpage():
    """Show signin"""

    # TODO: if not signed in, redirect to signin page

    return render_template("signin.html")

@app.route("/signedout")
def signedout():
    """Log user out and say goodbye"""

    if "student_id" in session:
        del session["student_id"]
        del session["cohort_id"]

    flash("You have signed out")

    return redirect("/signin")


@app.route("/<student_id>-profile")
def display_profile(student_id):
    """Display a student profile"""

    student_details = Student.query.filter(Student.student_id == student_id).one()

    return render_template("profile.html", student_details=student_details)

@app.route("/labs")
def labs():
    """display the lab history"""

    labs = Lab.query.all() # TODO specify cohort

    return render_template("labs.html", labs=labs)

@app.route("/lab/<lab_id>")
def lab_details(lab_id):
    """Display details of a lab"""

    lab = Lab.query.get(lab_id)
    pairs = Pair.query.filter(Pair.lab_id == lab_id, \
        db.or_(Pair.student_1_id == session["student_id"],\
        Pair.student_2_id == session["student_id"])).all() #pair.student1 etc #TODO admin

    keywords = [ x.keyword for x in lab.labs_keywords]

    return render_template("lab_page.html", lab=lab, keywords=keywords, pairs=pairs)


@app.route("/add-cohort", methods=["POST"])
def add_cohort():
    """Allow admin to create a cohort"""
    print "this happened"

    new_cohort_name = request.form.get("new-cohort-name")
    new_cohort_password = request.form.get("new-cohort-password")
    admin_id = session["admin_id"]

    new_cohort = Cohort(name=new_cohort_name,
        password=new_cohort_password,
        admin_id=admin_id)

    db.session.add(new_cohort)
    db.session.commit()

    most_recent = db.session.query(Cohort).order_by(Cohort.cohort_id.desc()).first()

    if most_recent.name == new_cohort_name and most_recent.password == new_cohort_password:
        response = {"string": most_recent.name}

    else:
        response = {"string": "Not added"}


    return jsonify(response)













################################################################################

if __name__ =="__main__":

    app.debug = True # fixme before deployment
    app.jinja_env.auto_reload = app.debug # fixme before deployment

    connect_to_db(app, "postgresql:///katfuntest") # fixme before deployment

    DebugToolbarExtension(app) # fixme before deployment

    app.run(port=5000, host='0.0.0.0')