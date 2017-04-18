
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from datetime import datetime
from server import app
from helpers import create_admin, create_cohort, create_lab_pair, create_student

######################################################
#TEST DATA SEED
######################################################


def create_addy_admin():
    """creates an admin in the admins table"""

    ad = create_admin(db=db, name="Addy Gladdy", 
        github_link="greatness.git",
        email="awesome.awe",
        profile_pic="so pretty picture",
        password="pw")



def create_boudicca_cohort():
    """Adds a cohort to the database

    Call creat_admin() before calling this function

    """

    admin_id = Admin.query.first().admin_id

    bo = create_cohort(db=db, name="Boudicca",
        password="secretpw",
        admin_id=admin_id,
        grad_date="2017-04-05")

    return bo

  

def create_beth_and_ellen_students():
    """Adds two students (of one cohort) to the database

    Call create_admin(), create_boudicca_cohort() before calling this function

    """

    bo_from_db = Cohort.query.first()
    bo_id = bo_from_db.cohort_id


    beth = create_student(db,
        name="Beth Happy",
        cohort_id=bo_id,
        email="katrina.huber@gmail.com",
        password="pw")
   

    ellen = create_student(db,
        name="Ellen Bellen",
        cohort_id=bo_id,
        email="katrina.huber@gmail.com",
        password="pw")


    return [beth, ellen]


def create_labs():
    """Adds a lab to the database

    Call create_admin(), create_boudicca_cohort() before calling this function"""

    bo_from_db = Cohort.query.first()
    bo_id = bo_from_db.cohort_id

    mel = Lab(title="Balloonicorn Melon Festival",
        description="Balloonicorn's festival of melons",
        cohort_id=bo_id,
        date=datetime.strptime("03/11/2017", "%m/%d/%Y")
        )
    db.session.add(mel)

    yay = Lab(title="Yay",
        description="Labs are great",
        cohort_id=bo_id,
        date=datetime.strptime("03/5/2017", "%m/%d/%Y")
        )
    db.session.add(yay)

    db.session.commit()

    return [mel, yay]


def create_pair():
    """Creates a relationship between two students and a lab

    Call create_admin(), create_boudicca_cohort(), create_beth_and_ellen_students() 
    and create_labs() before calling this function
    """

    beth_and_ellen = Student.query.all()
    a_lab_id = Lab.query.first().lab_id


    pa = create_lab_pair(db=db,
        lab_id=a_lab_id,
        student_1_id=beth_and_ellen[0].student_id,
        student_2_id=beth_and_ellen[1].student_id,
        notes="We learned soooo much!")

    



def create_keywords():
    kw = Keyword(keyword="word")
    kw2 = Keyword(keyword="key")

    db.session.add(kw)
    db.session.add(kw2)
    db.session.commit()
    
    return [kw, kw2]

def associate_labs_to_keywords():
    """Associates labs and keywords

    Call create_admin(), create_boudicca_cohort(), create_labs()
    and create_keywords() before calling this function
    """

    lab_1_id = Lab.query.get(1).lab_id
    keyword_1 = Keyword.query.get(1).keyword_id

    lab_2_id = Lab.query.get(2).lab_id
    keyword_2 = Keyword.query.get(2).keyword_id

    lw1 = LabKeyword(lab_id=lab_1_id, keyword_id=keyword_1)

    lw2 = LabKeyword(lab_id=lab_2_id, keyword_id=keyword_2)

    db.session.add(lw1)
    db.session.add(lw2)
    db.session.commit()


################################################################################
# SEED katfuntest DATABASE FOR FUNCTIONAL TESTING
################################################################################


if __name__ == "__main__":
    safe_to_proceed = raw_input("did you drop katfuntest since the last time you ran this? did your recreate it? (y/n)")

    if safe_to_proceed == 'y':
        connect_to_db(app, "postgresql:///katfuntest")
        db.create_all()
        
        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()
        create_labs()
        create_pair()
        create_keywords()
        associate_labs_to_keywords()