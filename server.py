# don't forget: source secret.sh

# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword

from flask import Flask, session, render_template, request, jsonify, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import os, sys

app = Flask(__name__)
app.secret_key = os.environ['secret_key']


@app.route("/", methods=["GET"])
def homepage():
    """Show homepage"""

    if "cohort_id" in session:
        cohort_members = Student.query.filter(Student.cohort_id == session["cohort_id"]).all()
        grad_date = Cohort.query.get(session["cohort_id"]).grad_date
        return render_template("home.html", cohort_members=cohort_members, grad_date=grad_date)
                                #cohort.html TODO
    elif "admin_id" in session:

        cohorts = Cohort.query.filter(Cohort.admin_id == session["admin_id"]).all()

        return render_template("home.html", cohorts=cohorts)

    else:
        cohorts = Cohort.query.all()

        return render_template("home.html", cohorts=cohorts)

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
    elif "admin_id" in session:
        del session["admin_id"]
        if "cohort_id" in session:
            del session["cohort_id"]

    flash("You have signed out")

    return redirect("/")


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

    new_cohort_name = request.form.get("new_cohort_name")
    new_cohort_password = request.form.get("new_cohort_password")
    admin_id = session["admin_id"]

    new_cohort = Cohort(name=new_cohort_name,
        password=new_cohort_password,
        admin_id=admin_id) 


    db.session.add(new_cohort)
    db.session.commit()

    db.session.refresh(new_cohort)


    if new_cohort.name == new_cohort_name and new_cohort.password == new_cohort_password:
        response = {
                    "string": new_cohort.name,
                    "createdId": new_cohort.cohort_id}

    else:
        response = {"string": "Not added"}


    return jsonify(response)



@app.route("/<cohort_id>/cohort")
def select_cohort(cohort_id):
    """Add cohort_id to session"""

    session["cohort_id"] = int(cohort_id)

    return redirect("/")





################################################################################

if __name__ =="__main__":

    app.debug = True # fixme before deployment
    app.jinja_env.auto_reload = app.debug # fixme before deployment
    

    if len(sys.argv) > 1 and sys.argv[1].lower() == 'testing':
        app.config['TESTING'] = True  
    else:
        app.config['TESTING'] = False


    database_uri = "postgresql:///kattestdb" if app.config['TESTING'] else "postgresql:///katfuntest"
    connect_to_db(app, database_uri) # fixme before deployment
    DebugToolbarExtension(app) # fixme before deployment

    app.run(port=5000, host='0.0.0.0')