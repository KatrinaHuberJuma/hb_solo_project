from flask_sqlalchemy import SQLAlchemy
from server import app

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

    cohort = db.relationship("Cohort", backref="students")



class Project(db.Model):
    """ Project fields """

    __tablename__="projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String)



class Pair(db.Model):
    """Who paired with whom on which project and what did they learn together"""

    __tablename__="pairs"

    pairing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer,
                          db.ForeignKey('projects.project_id'),
                          nullable=False)
    pair_1_id = db.Column(db.Integer,
                          db.ForeignKey('students.student_id'),
                          nullable=False)
    pair_2_id = db.Column(db.Integer,
                          db.ForeignKey('students.student_id'),
                          nullable=False)
    notes = db.Column(db.String)

    project = db.relationship("Project", backref="pairs")
    student = db.relationship("Student", backref="pairs")


def connect_to_db(app, db_uri="postgresql:///katcohort"):
    """ Connect the database to the Flask app """

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



# # Student(name ="Beth Happy", github_link ="git.hub", cohort_id = 1, email = "gmail.gmail")

# # Cohort(name = "Joan")



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app, "postgresql:///kattestdb")
    db.create_all() # this is not "creating the db" it is creating the tables, cols etc
    