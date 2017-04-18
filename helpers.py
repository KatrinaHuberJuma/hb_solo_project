from model import Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from datetime import datetime
import urllib, hashlib

def create_gravatar_url(email):
    default = "/static/img/switch.png"
    size = 100
     
    # construct the url
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

    return gravatar_url

def create_admin(db, name, github_link, email, profile_pic, password):

    ad = Admin(name=name, 
        github_link=github_link,
        email=email,
        profile_pic=profile_pic,
        password=password)

    db.session.add(ad)
    db.session.commit()


def create_cohort(db, name, password, grad_date, admin_id):

    new_cohort = Cohort(name=name,
        password=password,
        admin_id=admin_id,
        grad_date=datetime.strptime(grad_date,"%Y-%m-%d")) 


    db.session.add(new_cohort)
    db.session.commit()
    return new_cohort

def create_student(db, name, cohort_id, email, password):
    print "add proper github links"

    gravatar_url = create_gravatar_url(email)

    student = Student(name=name,
        github_link="git.hub",
        cohort_id=cohort_id,
        email=email,
        password=password,
        profile_pic=gravatar_url)

    db.session.add(student)
    db.session.commit()

    return student


def create_lab_pair(db, student_1_id, student_2_id, lab_id, notes="No notes yet"):
    """creates lab pair, commits it to the database and returns the pair object"""
   
    pa = Pair(lab_id=lab_id,
        student_1_id=student_1_id,
        student_2_id=student_2_id,
        notes=notes)

    db.session.add(pa)
    db.session.commit()
    return pa

def create_multiple_keywords(db, keywords):
    """creates a keyword and adds it to the database"""

    for keyword in keywords:
        kw = Keyword(keyword=keyword)
        db.session.add(kw)
        
    db.session.commit()

def create_association_keywords_to_lab(db, lab_id, keywords_ids):
    """Associates individual keywords to a lab through a new row in the labs_keywords table"""

    already_associated = LabKeyword.query.filter(LabKeyword.lab_id == lab_id, LabKeyword.keyword_id.in_(keywords_ids)).all()
    already_associated_ids = set([a.keyword_id for a in already_associated])

    keywords_ids = set(keywords_ids) - already_associated_ids

    for keyword_id in keywords_ids:
        lkw = LabKeyword(lab_id=lab_id, keyword_id=keyword_id)

        db.session.add(lkw)

    db.session.commit()

def return_all_keywords(db):

    keywords = Keyword.query.order_by(Keyword.keyword).all()

    return keywords


def return_certain_keywords_ids(db, keywords):

    certain_keywords = Keyword.query.filter(Keyword.keyword.in_(keywords)).all()
    certain_keywords_ids = [keyword.keyword_id for keyword in certain_keywords]
    return certain_keywords_ids

def return_keywords_ids(db, keywords):

    prospective_keywords = set(keywords)

    prexisting_keywords = return_all_keywords(db)
    kw_ids = []

    for keyword in prexisting_keywords:
        if keyword.keyword in prospective_keywords:
            kw_ids.append(keyword.keyword_id)
            prospective_keywords.remove(keyword.keyword)


    create_multiple_keywords(db, prospective_keywords)
   
    new_kw_ids = return_certain_keywords_ids(db, prospective_keywords)

    kw_ids.extend(new_kw_ids)

    return kw_ids


def return_labs_by_keyword_id(db, keyword_id):
    labs = db.session.query(Lab).filter(Lab.labs_keywords.any(LabKeyword.keyword_id ==keyword_id)).all()
    return labs

def return_cohort_members(db, cohort_id):
    cohort_members = Student.query.filter(Student.cohort_id == cohort_id).all()
    return cohort_members


def return_lab_pairs(db, lab_id):

    pairs = Pair.query.filter(Pair.lab_id == lab_id).all()

    return pairs

def return_other_students(db, excluded_ids, cohort_id):

    students = Student.query.filter(Student.cohort_id == cohort_id, ~Student.student_id.in_(excluded_ids)).all()
    return students


