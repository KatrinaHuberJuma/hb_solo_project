from model import connect_to_db, db, Cohort, Student, Lab, Pair
from server import app

safe_to_proceed = raw_input("did you drop katfuntest since the last time you ran this? did your recreate it? (y/n)")

if safe_to_proceed == 'y':
    connect_to_db(app, "postgresql:///katfuntest")
    db.create_all()

    bo = Cohort(name="Boudicca")
    db.session.add(bo)
    db.session.commit()

    bo_from_db = Cohort.query.first()
    bo_id = bo_from_db.cohort_id


    beth = Student(name="Beth Happy",\
        github_link="git.hub",\
        cohort_id=bo_id,\
        email="gmail.planetsave")

    db.session.add(beth)

    ellen = Student(name="Ellen Bellen",\
        github_link="hub.git",\
        cohort_id=bo_id,\
        email="gmail.gmail")

    db.session.add(ellen)

    mel = Lab(title="Balloonicorn Melon Festival",\
        description="Balloonicorn's festival of melons")
    db.session.add(mel)

    db.session.commit()


    beth_and_ellen = Student.query.all()
    a_lab_id = Lab.query.first().lab_id


    pa = Pair(lab_id=a_lab_id,\
        student_1_id=beth_and_ellen[0].student_id,\
        student_2_id=beth_and_ellen[1].student_id,\
        notes="We learned soooo much!")

    db.session.add(pa)
    db.session.commit()

