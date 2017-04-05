
# from connect_to_db import connect_to_db, db
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
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

    def test_admin_row(self):
        """checks that 'Addy Gladdy' was correctly added to the database"""

        create_admin()

        self.assertEqual('greatness.git', Admin.query
            .filter(Admin.name == 'Addy Gladdy')
            .first()
            .github_link
            )

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
        """ tests that a row was added to the labs table """

        create_labs()

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

    def test_keyword_created(self):
        """Tests that the keywords table exists and has an added keyword"""

        create_keywords()

        self.assertEqual("word", Keyword.query.first().keyword)

    def test_lab_keyword_association(self):
        """Tests that a lab and a keyword can be associated through the labs_keywords table"""

        associate_labs_to_keywords()

        # Session.query(Articles).filter(Articles.article_id == ArticleTags.article_id).
        # filter(ArticleTags.tag_id == Tags.tag_id).
        # filter(Tags.name == 'tag_name')

        self.assertEqual('word', db.session
            .query(LabKeyword)
            .filter(Lab.lab_id==LabKeyword.lab_id)
            .filter(LabKeyword.keyword_id==Keyword.keyword_id)
            .first().keyword.keyword
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

    # def test_admin_create_cohort(self):
    #     """Tests that a singed in admin can create a cohort"""

    #     create_admin()

    #     result = self.client.post("/new-cohort",
    #                                data={"cohort_name":"New Cohort",
    #                                      "password":"pw"})
    #     self.assertIn("Ellen Bellen", result.data)


    def test_display_cohort_members(self):

        create_students()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["student_id"] = 1
                sess["cohort_id"] = 1

        result = self.client.post("/",
                                   data={"name":"Beth Happy",
                                         "email":"gmail.planetsave"})
        self.assertIn("Ellen Bellen", result.data)

    def test_profile(self):

        create_students()

        result = self.client.get("/2-profile")
        self.assertIn("This is Ellen Bellen's profile", result.data)


    def test_labs_route(self):
        create_labs()

        result = self.client.get("/labs")
        self.assertIn("Yay", result.data)

    def test_lab_details(self):

        associate_labs_to_keywords()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["student_id"] = 1

        result = self.client.get("/lab/1")
        self.assertIn("Balloonicorn Melon Festival", result.data)
        self.assertIn("Ellen Bellen", result.data)
        self.assertIn("word", result.data)

######################################################
#HELPERS
######################################################


def create_admin():
    """creates an admin in the admins table"""

    ad = Admin(name="Addy Gladdy", 
        github_link="greatness.git",
        email="awesome.awe",
        profile_pic="so pretty picture",
        password="pw")

    db.session.add(ad)
    db.session.commit()


def create_cohort():
    """Adds a cohort to the database"""
    create_admin()

    admin_id = Admin.query.first().admin_id

    bo = Cohort(name="Boudicca", password="secretpw", admin_id=admin_id)
    db.session.add(bo)
    db.session.commit()


def create_students():
    """Adds two students (of one cohort) to the database"""

    create_cohort()

    bo_from_db = Cohort.query.first()
    bo_id = bo_from_db.cohort_id


    beth = Student(name="Beth Happy",
        github_link="git.hub",
        cohort_id=bo_id,
        email="gmail.planetsave",
        password="pw")

    db.session.add(beth)

    ellen = Student(name="Ellen Bellen",
        github_link="hub.git",
        cohort_id=bo_id,
        email="gmail.gmail",
        password="pw")

    db.session.add(ellen)
    db.session.commit()


def create_labs():
    """Adds a lab to the database"""

    mel = Lab(title="Balloonicorn Melon Festival",
        description="Balloonicorn's festival of melons")
    db.session.add(mel)

    yay = Lab(title="Yay",
        description="Labs are great")
    db.session.add(yay)

    db.session.commit()


def create_pair():
    """Creates a relationship between two students and a lab"""

    create_students()
    create_labs()

    beth_and_ellen = Student.query.all()
    a_lab_id = Lab.query.first().lab_id


    pa = Pair(lab_id=a_lab_id,
        student_1_id=beth_and_ellen[0].student_id,
        student_2_id=beth_and_ellen[1].student_id,
        notes="We learned soooo much!")

    db.session.add(pa)
    db.session.commit()


def create_keywords():
    kw = Keyword(keyword="word")
    kw2 = Keyword(keyword="key")

    db.session.add(kw)
    db.session.add(kw2)
    db.session.commit()

def associate_labs_to_keywords():
    create_pair()
    create_keywords()

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


if __name__ == "__main__":
    unittest.main()
