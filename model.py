from flask_sqlalchemy import SQLAlchemy
from server import app

db = SQLAlchemy()


class Cohort(db.Model):
    """A group of students"""

    __tablename__ = "cohorts"

    def __repr__(self):

        return "\n< %s Cohort, grad %s >" % (self.name, self.grad_date)

    cohort_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    grad_date = db.Column(db.DateTime) 


class Student(db.Model):
    """ student (user) information"""

    __tablename__ = "students"

    def __repr__(self):

        return "\n< %s is a student >" % (self.name)

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    github_link = db.Column(db.String(100))
    cohort_id = db.Column(db.Integer,
                          db.ForeignKey('cohorts.cohort_id'),
                          nullable=False)
    email = db.Column(db.String(20), nullable=False)

    cohort = db.relationship("Cohort", backref="students")





def connect_to_db(app, db_uri="postgresql:///katcohort"):
    """ Connect the database to the Flask app """

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


# connect_to_db(app, "postgresql:///kattestdb")

# Student(name ="Beth Happy", github_link ="git.hub", cohort_id = 1, email = "gmail.gmail")

# Cohort(name = "Joan")



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app, "postgresql:///kattestdb")
    print "Connected to DB."

    db.create_all() # this is not "creating the db" it is creating the tables, cols etc
    