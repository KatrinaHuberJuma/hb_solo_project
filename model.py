# from server import app
# Hello everyone in lecture! this is great
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    """admin fields"""

    __tablename__ = "admins"
    # add repr

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    github_link = db.Column(db.String(100))
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    profile_pic = db.Column(db.String(100))
    bio = db.Column(db.String)





class Cohort(db.Model):
    """ cohort fields """

    __tablename__ = "cohorts"

    def __repr__(self):
        return "< %s Cohort, grad %s >" % (self.name, self.grad_date)

    cohort_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    grad_date = db.Column(db.DateTime)
    admin_id = db.Column(db.Integer,
        db.ForeignKey('admins.admin_id'),
        nullable=False)



class Student(db.Model):
    """ student fields and relationship to cohorts table """

    __tablename__ = "students"

    def __repr__(self):

        return "< %s is a student %s >" % (self.name, self.student_id)

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    github_link = db.Column(db.String(100))
    cohort_id = db.Column(db.Integer,
                          db.ForeignKey('cohorts.cohort_id'),
                          nullable=False)
    email = db.Column(db.String, nullable=False) # unique
    password = db.Column(db.String(20), nullable=False)
    demo_vid = db.Column(db.String)
    profile_pic = db.Column(db.String)
    bio = db.Column(db.String)

    cohort = db.relationship("Cohort", backref="students")



class Lab(db.Model):
    """ Lab fields """

    __tablename__="labs"

    def __repr__(self):
        return "< LAB = %s >" % (self.title)

    lab_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    cohort_id = db.Column(db.Integer,
                          db.ForeignKey('cohorts.cohort_id'),
                          nullable=False)
    description = db.Column(db.String)
    instructions = db.Column(db.String)
    date = db.Column(db.DateTime)

    cohort = db.relationship("Cohort", backref="labs")


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


class Keyword(db.Model):
    """Keywords"""

    __tablename__= "keywords"

    def __repr__(self):
        return "< keyword: %s >" % (self.keyword)

    keyword_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(50))



class LabKeyword(db.Model):
    """Association table connecting labs and keywords"""

    __tablename__="labs_keywords"

    row_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column(db.Integer,
                          db.ForeignKey('labs.lab_id'),
                          nullable=False)
    keyword_id = db.Column(db.Integer,
                          db.ForeignKey('keywords.keyword_id'),
                          nullable=False)

    keyword = db.relationship("Keyword", backref="labs_keywords")
    lab = db.relationship("Lab", backref="labs_keywords")



################################################################################


def connect_to_db(app, db_uri="postgresql:///katcohort"):
    """ Connect the database to the Flask app """

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


################################################################################

if __name__ == "__main__":
  
    from server import app
    connect_to_db(app, "postgresql:///katfuntest")
    db.create_all() # this is not "creating the db" it is creating the tables, cols etc
    


    #############################
#     Lab.query.filter(Lab.lab_id==1).join(LabKeyword).join(Keyword).first()
