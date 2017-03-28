import model
import unittest



class RelationshipUnitTests(unittest.TestCase):
    """Tests that the classes in model correctly polulate a database"""

    def setUp(self):
        """Should connect to test db (kattestdb)"""


        model.connect_to_db(app, "postgresql:///kattestdb")


    def make_cohort(self):
        """Should instantiate a Cohort and add it to the cohorts table"""

        jo = Cohort(name = "Joan")

        db.session.add(jo)
        db.session.commit()

        print Cohort.query.all()



    def tearDown(self):
        """Should close the session and drop all tables"""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()
