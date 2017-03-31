
from connect_to_db import connect_to_db, db
# from server import app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Cohort(db.Model):
    """ cohort fields """

    __tablename__ = "cohorts"

    cohort_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    grad_date = db.Column(db.DateTime)

    def __repr__(self):
        return "< %s Cohort, grad %s >" % (self.name, self.grad_date)


class Student(db.Model):
    """ student fields and relationship to cohorts table """

    __tablename__ = "students"

    def __repr__(self):

        return "< %s is a student >" % (self.name)

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    github_link = db.Column(db.String(100))
    cohort_id = db.Column(db.Integer,
                          db.ForeignKey('cohorts.cohort_id'),
                          nullable=False)
    email = db.Column(db.String(20), nullable=False)
    demo_vid = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))

    cohort = db.relationship("Cohort", backref="students")



class Lab(db.Model):
    """ Lab fields """

    __tablename__="labs"

    def __repr__():
        return "< LAB = %s >" % (self.title)

    lab_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String)



class Pair(db.Model):
    """Who paired with whom on which lab and what did they learn together"""

    __tablename__ = "pairs"

    def __repr__(self):
        return "< LAB id = %s, STUDENT 1 id = %s, STUDENT 2 id = %s >" % (self.lab_id, 
                                                                    self.student_1_id, 
                                                                    self.student_2_id)

    pairing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column(db.Integer,
                          db.ForeignKey('labs.lab_id'),
                          nullable=False)
    student_1_id = db.Column(db.Integer,
                          db.ForeignKey('students.student_id'),
                          nullable=False)
    student_2_id = db.Column(db.Integer,
                          db.ForeignKey('students.student_id'),
                          nullable=False)
    notes = db.Column(db.String)

    lab = db.relationship("Lab", backref="pairs")
    student1 = db.relationship("Student", backref="pairs1",
        foreign_keys=[student_1_id])
    student2 = db.relationship("Student", backref="pairs2",
        foreign_keys=[student_2_id])


def connect_to_db(app, db_uri="postgresql:///katcohort"):
    """ Connect the database to the Flask app """

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
  
    from server import app
    connect_to_db(app, "postgresql:///katfuntest")
    db.create_all() # this is not "creating the db" it is creating the tables, cols etc
    