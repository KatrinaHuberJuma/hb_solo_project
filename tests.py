
# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Cohort, Student, Lab, Pair
import unittest
from server import app, session

######################################################
#TESTS FOR THE SERVER ALONE
######################################################

class ServerUnitTests(unittest.TestCase):
    """ tests routes """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True # fixme before deployment

    def test_homepage_route(self):
        # TODO: check the signedout redirect to signin
        result = self.client.get("/")
        self.assertIn("Welcome!", result.data)

    def test_signin_route(self): 
        result = self.client.get("/signin")
        self.assertIn("Please sign in!", result.data)


######################################################
#TESTS FOR THE DATABASE ALONE
######################################################

class RelationshipUnitTests(unittest.TestCase):
    """Tests that the classes in model correctly polulate a database"""

    def setUp(self):
        """Should connect to test db (kattestdb) and populate tables for testing"""

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

    def tearDown(self):
        """Should close the session and drop all tables"""

        db.session.close()
        db.drop_all()

    def test_cohort_row(self):
        """checks that the test cohort is in the cohorts table"""
        create_cohort()

        self.assertEqual('Boudicca', Cohort.query
            .filter(Cohort.name == 'Boudicca')
            .first()
            .name
            )



    def test_student_row(self):
        """ checks that 'Beth Happy' was correctly added to database """

        create_students()

        self.assertEqual('Beth Happy', Student.query
            .filter(Student.name == 'Beth Happy')
            .one()
            .name
            )


    def test_student_to_cohort_relation(self):
        """Checks that the relationship between students and cohorts is correct"""

        create_students()

        self.assertEqual('Boudicca', db.session
            .query(Student)
            .join(Cohort)
            .filter(Student.name=='Beth Happy')
            .one()
            .cohort.name
            )
        

    def test_lab_row(self):
        """ tests that a row was added to the labss table """

        create_lab()

        self.assertEqual('Balloonicorn Melon Festival', Lab.query
            .filter(Lab.title == 'Balloonicorn Melon Festival')
            .one()
            .title
            )


    def test_pair_relationship_to_lab(self):
        """ tests that there is a relationship between cohort and pair """

        create_pair()

        self.assertEqual('Balloonicorn Melon Festival', db.session
            .query(Pair)
            .join(Lab)
            .first()
            .lab.title
            )


    def test_pair_relationship_to_student(self):
        """ tests that there is a relationship between cohort and pair """

        create_pair()

        self.assertEqual('Beth Happy', db.session
            .query(Pair)
            .first() # check do I need to have the join (see above)
            .student1.name
            )


######################################################
#TESTS FOR THE DATABASE AND SERVER INTEGRATION
######################################################


class ModelServerIntegration(unittest.TestCase):
    """Tests that the database content displays correctly on the webpages"""

    def setUp(self):
        """Should connect to test db (kattestdb) and populate tables for testing"""

        self.client = app.test_client()
        app.config['TESTING'] = True # fixme before deployment

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

    def tearDown(self):
        """Should close the session and drop all tables"""

        db.session.close()
        db.drop_all()

    def test_display_cohort_members(self):

        create_students()

        result = self.client.post("/",
                                   data={"name":"Beth Happy",
                                         "email":"gmail.planetsave"})
        self.assertIn("<li>Ellen Bellen</li>", result.data)

    def test_profile(self):

        create_students()

        result = self.client.get("/2-profile")
        self.assertIn("This is Ellen Bellen's profile", result.data)

######################################################
#HELPERS
######################################################



def create_cohort():
    """Adds a cohort to the database"""

    bo = Cohort(name="Boudicca")
    db.session.add(bo)
    db.session.commit()


def create_students():
    """Adds two students (of one cohort) to the database"""

    create_cohort()

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
    db.session.commit()


def create_lab():
    """Adds a lab to the database"""

    mel = Lab(title="Balloonicorn Melon Festival",\
        description="Balloonicorn's festival of melons")
    db.session.add(mel)
    db.session.commit()


def create_pair():
    """Creates a relationship between two students and a lab"""

    create_students()
    create_lab()

    beth_and_ellen = Student.query.all()
    a_lab_id = Lab.query.first().lab_id


    pa = Pair(lab_id=a_lab_id,\
        student_1_id=beth_and_ellen[0].student_id,\
        student_2_id=beth_and_ellen[1].student_id,\
        notes="We learned soooo much!")

    db.session.add(pa)
    db.session.commit()






if __name__ == "__main__":
    unittest.main()
