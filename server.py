# don't forget: source secret.sh

# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from datetime import datetime
from flask import Flask, session, render_template, request, jsonify, flash, redirect, g
from flask_debugtoolbar import DebugToolbarExtension
import os, sys, json
from helpers import (
                    create_association_keywords_to_lab,
                    create_cohort,
                    create_lab_pair,
                    create_lab,
                    create_student,
                    return_all_keywords,
                    return_certain_keywords_ids,
                    return_cohort_members,
                    return_keywords_ids,
                    return_lab_pairs,
                    return_labs_by_keyword_id,
                    create_multiple_keywords,
                    return_other_students,
                    return_pair_details,
                    update_many_student_fields,
                    update_pair_notes
                    )
# import json TODO 

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

################################################################################


JS_TESTING_MODE = False

@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE



################################################################################

@app.route("/", methods=["GET"])
def homepage():
    """Show homepage"""

    if "student_id" in session:
        return redirect("/%s-profile" % session["student_id"])

    elif "admin_id" in session:

        cohorts = Cohort.query.filter(Cohort.admin_id == session["admin_id"]).all()

    else:
        cohorts = Cohort.query.all()

    return render_template("home.html", cohorts=cohorts)


################################################################################


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
            cohort_members = return_cohort_members(db, session["cohort_id"])
            flash("You are logged in now.")
            return redirect("/%s-profile" % session["student_id"])


    flash("invalid login")
    return redirect("/")


################################################################################

@app.route("/signedout")
def signedout():
    """Log user out and say goodbye"""

    if "student_id" in session:
        del session["student_id"]
    elif "admin_id" in session:
        del session["admin_id"]
    if "cohort_id" in session:
        del session["cohort_id"]

    flash("You have signed out")

    return redirect("/")


################################################################################

@app.route("/clear_cohort")
def clear_cohort():

    if "cohort_id" in session:
        del session["cohort_id"]

    return redirect("/")


################################################################################

@app.route("/<student_id>-profile")
def display_profile(student_id):
    """Display a student profile"""

    student = Student.query.filter(Student.student_id == student_id).first()

    return render_template("profile.html", student=student)


################################################################################

@app.route("/update_<student_id>_profile")
def update_student_profile(student_id):

    student = Student.query.filter(Student.student_id == student_id).one()

    return render_template("update_student_profile.html", student=student)


################################################################################

@app.route("/post_student_update", methods=["POST"])
def post_update_student_profile():

    student = Student.query.filter(Student.student_id == session['student_id']).one()

    all_fields = request.form.get("all_fields")
    updates = json.loads(all_fields)

    update_many_student_fields(db, student=student, updates=updates)

    response = {
                "bio": student.bio,
                "email": student.email,
                "demoVid": student.demo_vid,
                "githubLink": student.github_link,
                "profilePic": student.profile_pic
                }

    return jsonify(response)



################################################################################

@app.route("/labs")
def labs():
    """display the lab history"""
    
    labs = db.session.query(Lab).order_by(Lab.date).join(Cohort).all()

    return render_template("labs.html", labs=labs)


################################################################################

@app.route("/lab/<lab_id>")
def lab_details(lab_id):
    """Display details of a lab"""

    lab = Lab.query.get(lab_id)


    pairs = return_lab_pairs(db, lab_id)

    ids_to_exclude = []

    for pair in pairs:
        ids_to_exclude.append(pair.student_1_id)
        ids_to_exclude.append(pair.student_2_id)

    keywords = [x.keyword for x in lab.labs_keywords]

    students = return_other_students(db, excluded_ids=ids_to_exclude, cohort_id=lab.cohort_id)

    return render_template("lab_page.html",
                            lab=lab,
                            keywords=keywords,
                            pairs=pairs,
                            students=students)


################################################################################

@app.route("/pair/<pairing_id>")
def pair_page(pairing_id):


    pair_details = return_pair_details(db, pairing_id)

    lab = pair_details["lab"]
    student1 = pair_details["student1"]
    student2 = pair_details["student2"]
    notes = pair_details["notes"]
    pair_id = pair_details["pairing_id"]
    # TODO
    return render_template("pair.html", pair_id=pair_id, notes=notes, lab=lab, student1=student1, student2=student2)


################################################################################

@app.route("/update-pair-notes", methods=["POST"])
def update_pair_lab_notes():

    notes = request.form.get("pair_notes")
    pair_id = request.form.get("pair_id")

    update_pair_notes(db, pairing_id=pair_id, new_value=notes)

    response = {
                "newNotes": notes
                }

    return jsonify(response)




################################################################################


@app.route("/pair_students", methods=["POST"])
def pair_students():

    new_pair1 = request.form.get("new_pair1")
    new_pair2 = request.form.get("new_pair2")
    lab_id = request.form.get("lab_id")

    new_lab_pair = create_lab_pair(db, int(new_pair1), int(new_pair2), int(lab_id))

    pairs = return_lab_pairs(db, lab_id)


    ids_to_exclude = []
    paired_with_names_for_response = [] # {student_1_name:, student_1_id:, student_2_name:, student_2_id:, notes:}

    for pair in pairs:
        add_pair = {}
        ids_to_exclude.append(pair.student_1_id)
        add_pair["student_1_id"] = pair.student_1_id
        add_pair["student_1_name"] = pair.student1.name

        ids_to_exclude.append(pair.student_2_id)
        add_pair["student_2_id"] = pair.student_2_id
        add_pair["student_2_name"] = pair.student2.name

        add_pair["notes"] = pair.notes

        paired_with_names_for_response.append(add_pair)

    unpaired_with_names_for_response = []

    unpaired = return_other_students(db, excluded_ids=ids_to_exclude, cohort_id=session["cohort_id"])

    for student in unpaired:
        student_info = {}
        student_info["student_id"] = student.student_id
        student_info["student_name"] = student.name
        unpaired_with_names_for_response.append(student_info)



    # unpaired = return_other_students(db, excluded_ids)

    response = {
                "pairs": paired_with_names_for_response,
                "unpaireds": unpaired_with_names_for_response 
                }

    return jsonify(response)

################################################################################

@app.route("/keywords")
def keywords():
    """Display all keywords, select one to view related labs"""

    keywords = return_all_keywords(db)

    return render_template("keywords.html", keywords=keywords)



################################################################################

@app.route("/show_related_labs", methods=["POST"])
def related_labs():
    """display all labs related to a given keyword_id"""

    keyword_id = request.form.get("keyword_id")

    labs = return_labs_by_keyword_id(db, keyword_id=keyword_id)

    labs = [{"lab_title": lab.title, "lab_id": lab.lab_id, "keyword_id": keyword_id} for lab in labs]

    return jsonify(labs)


################################################################################

@app.route("/add-cohort", methods=["POST"])
def add_cohort():
    """Allow admin to create a cohort"""

    new_cohort_name = request.form.get("new_cohort_name")
    new_cohort_password = request.form.get("new_cohort_password")
    new_grad_date = request.form.get("new_grad_date")
    admin_id = session["admin_id"]

    new_cohort = create_cohort(db=db,
        name=new_cohort_name,
        password=new_cohort_password,
        grad_date=new_grad_date,
        admin_id=admin_id)



    if new_cohort.name == new_cohort_name and new_cohort.password == new_cohort_password:
        response = {
                    "string": new_cohort.name,
                    "createdId": new_cohort.cohort_id
                    }

    else:
        response = {"string": "Not added",
                    "createdId": "fail"
                    }


    return jsonify(response)


################################################################################

@app.route("/add-lab", methods=["POST"])
def add_lab():
    """Allow admin to create a lab"""

    new_lab_name = request.form.get("new_lab_name")
    new_lab_description = request.form.get("new_lab_description")
    new_lab_date = request.form.get("new_lab_date")
    new_lab_instructions = request.form.get("new_lab_instructions")
    admin_id = session["admin_id"]

    new_lab = create_lab(db, title=new_lab_name,
        description=new_lab_description,
        cohort_id=session["cohort_id"],
        date=new_lab_date,
        instructions=new_lab_instructions) 


    response = {
                "string": new_lab.title,
                "createdId": new_lab.lab_id
                }



    return jsonify(response)


################################################################################


@app.route("/signup-student", methods=["POST"])
def signup_student():
    """Allow a new student to join a cohort using secret password"""

    new_student_name = request.form.get("new_student_name")
    new_student_email = request.form.get("new_student_email")
    new_student_password = request.form.get("new_student_password")
    given_cohort_password = request.form.get("cohort_password")


    valid_cohort_creds = Cohort.query.filter(
        Cohort.cohort_id == session["cohort_id"],
        Cohort.password == given_cohort_password).first()

    if valid_cohort_creds:
        new_student = create_student(db, name=new_student_name,
            password=new_student_password,
            cohort_id=session["cohort_id"],
            email=new_student_email)


        response = {
                    "string": new_student.name,
                    "createdId": new_student.student_id
                    }
                    
        session["student_id"]=new_student.student_id

    else:
        response = {
                    "string": "Sorry, you have not joined. Wrong cohort password maybe?",
                    "createdId": "fail"
                    }

    return jsonify(response)


################################################################################

@app.route("/add_keyword", methods=["POST"])
def add_keywords_to_lab():

    new_keywords = request.form.get("new_keywords")
    lab_id_for_keyword = request.form.get("lab_id_for_keyword")

    new_keywords = new_keywords.split(", ")

    kw_ids = return_keywords_ids(db=db, keywords=new_keywords)

    create_association_keywords_to_lab(db=db, lab_id=lab_id_for_keyword, keywords_ids=kw_ids)

    response = {
                "new_words": new_keywords
                } # TODO do i need this????

    return jsonify(new_keywords)



################################################################################

@app.route("/cohort<cohort_id>")
def cohort_home(cohort_id):

    session["cohort_id"] = session.get("cohort_id", int(cohort_id))

    cohort_members = return_cohort_members(db, session["cohort_id"])
    cohort = Cohort.query.get(session["cohort_id"])
    cohort_labs = Lab.query.filter(Lab.cohort_id == session["cohort_id"]).all()
    return render_template("cohort_home.html",
        cohort_members=cohort_members,
        cohort=cohort,
        cohort_labs=cohort_labs)



################################################################################

if __name__ =="__main__":

    app.debug = True # fixme before deployment
    app.jinja_env.auto_reload = app.debug # fixme before deployment
    

    if len(sys.argv) > 1 and sys.argv[1].lower() == 'testing':
        app.config['TESTING'] = True  
    elif len(sys.argv) > 1 and sys.argv[1].lower() == 'jstesting':
        JS_TESTING_MODE = True
        app.config['TESTING'] = False
    else:
        app.config['TESTING'] = False


    database_uri = "postgresql:///kattestdb" if app.config['TESTING'] else "postgresql:///katfuntest"
    connect_to_db(app, database_uri) # fixme before deployment
    # DebugToolbarExtension(app) # fixme before deployment

    app.run(port=5000, host='0.0.0.0')