
# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Cohort, Student, Lab, Pair
import unittest
from server import app

class ServerTests(unittest.TestCase):
    """ tests routes """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True # fixme before deployment

    def test_homepage(self):
        # TODO: check the signedout redirect to signin
        result = self.client.get("/")
        self.assertIn("Welcome!", result.data)

    def test_signin(self): 
        result = self.client.get("/signin")
        self.assertIn("Please sign in!", result.data)




class RelationshipUnitTests(unittest.TestCase):
    """Tests that the classes in model correctly polulate a database"""

    def setUp(self):
        """Should connect to test db (kattestdb) and populate tables for testing"""

        connect_to_db(app, "postgresql:///kattestdb")
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


    def test_cohort_row(self):
        """checks that the test cohort is in the cohorts table"""

        self.assertEqual('Boudicca', Cohort.query
            .filter(Cohort.name == 'Boudicca')
            .first()
            .name
            )



    def test_student_row(self):
        """ checks that 'Beth Happy' was correctly added to database """


        self.assertEqual('Beth Happy', Student.query
            .filter(Student.name == 'Beth Happy')
            .one()
            .name
            )


    def test_student_to_cohort_relation(self):
        """Checks that the relationship between students and cohorts is correct"""

        self.assertEqual('Boudicca', db.session
            .query(Student)
            .join(Cohort)
            .filter(Student.name=='Beth Happy')
            .one()
            .cohort.name
            )
        

    def test_lab_row(self):
        """ tests that a row was added to the labss table """

        self.assertEqual('Balloonicorn Melon Festival', Lab.query
            .filter(Lab.title == 'Balloonicorn Melon Festival')
            .one()
            .title
            )


    def test_pair_relationship_to_lab(self):
        """ tests that there is a relationship between cohort and pair """

        self.assertEqual('Balloonicorn Melon Festival', db.session
            .query(Pair)
            .join(Lab)
            .first()
            .lab.title
            )


    def test_pair_relationship_to_student(self):
        """ tests that there is a relationship between cohort and pair """

        self.assertEqual('Beth Happy', db.session
            .query(Pair)
            .first() # check do I need to have the join (see above)
            .student1.name
            )



    def tearDown(self):
        """Should close the session and drop all tables"""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()


# def print_my_tables():
#     pass
    