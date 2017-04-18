
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
import unittest
from server import app, session
from test_seed import create_addy_admin, create_boudicca_cohort, create_beth_and_ellen_students, create_labs, create_pair, create_keywords, associate_labs_to_keywords
from helpers import create_lab_pair, return_other_students, create_association_keywords_to_lab, create_multiple_keywords, return_certain_keywords_ids, return_keywords_ids, return_labs_by_keyword_id
######################################################
#TESTS FOR THE SERVER ALONE
######################################################

class ServerTests(unittest.TestCase):
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

class RelationshipTests(unittest.TestCase):
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

        create_addy_admin()

        self.assertEqual('greatness.git', Admin.query
            .filter(Admin.name == 'Addy Gladdy')
            .first()
            .github_link
            )

    def test_cohort_row(self):
        """checks that the test cohort is in the cohorts table"""

        create_addy_admin()
        create_boudicca_cohort()

        self.assertEqual('Boudicca', Cohort.query
            .filter(Cohort.name == 'Boudicca')
            .first()
            .name
            )


    def test_student_row(self):
        """ checks that 'Beth Happy' was correctly added to database """

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()

        self.assertEqual('Beth Happy', Student.query
            .filter(Student.name == 'Beth Happy')
            .one()
            .name
            )


    def test_student_to_cohort_relation(self):
        """Checks that the relationship between students and cohorts is correct"""

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()

        self.assertEqual('Boudicca', db.session
            .query(Student)
            .join(Cohort)
            .filter(Student.name=='Beth Happy')
            .one()
            .cohort.name
            )
        

    def test_lab_row(self):
        """ tests that a row was added to the labs table """

        create_addy_admin()
        create_boudicca_cohort()
        create_labs()

        self.assertEqual('Balloonicorn Melon Festival', Lab.query
            .filter(Lab.title == 'Balloonicorn Melon Festival')
            .one()
            .title
            )


    def test_pair_relationship_to_lab(self):
        """ tests that there is a relationship between cohort and pair """

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()
        create_labs()
        create_pair()

        self.assertEqual('Balloonicorn Melon Festival', db.session
            .query(Pair)
            .join(Lab)
            .first()
            .lab.title
            )


    def test_pair_relationship_to_student(self):
        """ tests that there is a relationship between cohort and pair """

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()
        create_labs()
        create_pair()

        self.assertEqual('Beth Happy', db.session
            .query(Pair)
            .first() # check do I need to have the join (see above)
            .student1.name
            )


    def test_keywords_created(self):
        """Tests that the keywords table exists and has an added keyword"""

        create_multiple_keywords(db=db, keywords=["Elephant", "puppy"])

        existing_keywords = Keyword.query.all()

        self.assertEqual("Elephant", existing_keywords[0].keyword)
        self.assertEqual("puppy", existing_keywords[1].keyword)



    def test_return_certain_keywords_ids(self):

        create_multiple_keywords(db=db, keywords=["Elephant", "puppy", "skipme", "cool"])

        certain_ids = return_certain_keywords_ids(db=db, keywords=["Elephant", "cool", "puppy"])

        self.assertEqual([1, 2, 4], certain_ids)        



    def test_return_keywords_ids(self):

        create_multiple_keywords(db=db, keywords=["Elephant", "puppy", "skipme", "cool"])


        these_kw_ids = return_keywords_ids(db=db, keywords=["Elephant", "cool", "puppy", "bestie"])

        self.assertEqual(set([1, 2, 4, 5]), set(these_kw_ids)) 



    def test_lab_keywords_association(self):
        """Tests that a lab and a keyword can be associated through the labs_keywords table"""

        create_addy_admin()
        create_boudicca_cohort()
        labs = create_labs()
        keywords = create_keywords()
        
        create_association_keywords_to_lab(db=db,
            lab_id=labs[0].lab_id,
            keywords_ids=[keyword.keyword_id for keyword in keywords])

        self.assertEqual('word', db.session
            .query(LabKeyword)
            .filter(Lab.lab_id==LabKeyword.lab_id)
            .filter(LabKeyword.keyword_id==Keyword.keyword_id)
            .all()[0].keyword.keyword
            )

        self.assertEqual('key', db.session
            .query(LabKeyword)
            .filter(Lab.lab_id==LabKeyword.lab_id)
            .filter(LabKeyword.keyword_id==Keyword.keyword_id)
            .all()[1].keyword.keyword
            )


    def test_no_duplicate_lab_keyword_association(self):
    
        create_addy_admin()
        create_boudicca_cohort()
        labs = create_labs()
        keywords = create_keywords()

        create_association_keywords_to_lab(db=db,
            lab_id=labs[0].lab_id,
            keywords_ids=[keyword.keyword_id for keyword in keywords]) 
                   
        create_association_keywords_to_lab(db=db,
            lab_id=labs[0].lab_id,
            keywords_ids=[keyword.keyword_id for keyword in keywords])

        self.assertEqual(LabKeyword.query.filter(LabKeyword.row_id == 3).first(), None)
        self.assertEqual(LabKeyword.query.filter(LabKeyword.row_id == 4).first(), None)


    def test_return_labs_by_keyword_id(self):
        
        create_addy_admin()
        create_boudicca_cohort()
        labs = create_labs()    
        mel_fest_keywords = ["outside", "melon", "fun", "goodness"]
        yay_keywords = ["excite", "yes", "goodness"]
        # other_cohort_keywords = ["no", "not", "bad"]
        mel_fest_keywords_ids = return_keywords_ids(db, mel_fest_keywords)
        yay_keywords_ids = return_keywords_ids(db, yay_keywords)
        create_association_keywords_to_lab(db, labs[0].lab_id, mel_fest_keywords_ids)
        create_association_keywords_to_lab(db, labs[1].lab_id, yay_keywords_ids)


        keywords_ids = return_keywords_ids(db, ["outside", "goodness", "excite"])


        self.assertEqual("Yay",
            return_labs_by_keyword_id(db, keywords_ids[0])[0].title)
        self.assertEqual(["Balloonicorn Melon Festival", "Yay"],
            [lab.title for lab in return_labs_by_keyword_id(db, keywords_ids[1])])
        self.assertEqual("Balloonicorn Melon Festival",
            return_labs_by_keyword_id(db, keywords_ids[2])[0].title)



    def test_create_lab_pair(self):

        create_addy_admin()
        create_boudicca_cohort()
        students = create_beth_and_ellen_students()
        labs = create_labs()
        lab_id = labs[1].lab_id

        print "\n\nstudents=", students
        create_lab_pair(db=db,
            student_1_id=students[0].student_id,
            student_2_id=students[1].student_id,
            lab_id=lab_id,
            notes="This is a test")

        self.assertEqual('Beth Happy', db.session
            .query(Pair)
            .first() 
            .student1.name
            )
        self.assertEqual('Ellen Bellen', db.session
            .query(Pair)
            .first() 
            .student2.name
            )
        self.assertEqual('Yay', db.session
            .query(Pair)
            .first()
            .lab.title
            )
        self.assertEqual('This is a test', db.session
            .query(Pair)
            .first()
            .notes
            )
            
    def test_return_other_students(self):

        create_addy_admin()
        create_boudicca_cohort()
        students = create_beth_and_ellen_students()

        other_students = return_other_students(db, excluded_ids=[1], cohort_id=1)

        self.assertNotIn("Beth Happy", [student.name for student in other_students])
        self.assertIn("Ellen Bellen", [student.name for student in other_students])



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
 

    def test_display_cohorts_admin(self):

        create_addy_admin()
        create_boudicca_cohort()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["admin_id"] = 1

        result = self.client.post("/",
                                   data={"name":"Addy Gladdy",
                                         "password":"pw",
                                         "permissions": "admin"})
        self.assertIn("Boudicca", result.data)


    def test_display_cohort_members_to_student(self):

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["student_id"] = 1
                sess["cohort_id"] = 1

        result = self.client.get("/cohort1")
        self.assertIn("Ellen Bellen", result.data)

    def test_profile(self):

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()

        result = self.client.get("/2-profile")
        self.assertIn("This is Ellen Bellen's profile", result.data)


    def test_labs_route(self):
        
        create_addy_admin()
        create_boudicca_cohort()
        create_labs()

        result = self.client.get("/labs")
        self.assertIn("Yay", result.data)

    def test_lab_details(self):

        create_addy_admin()
        create_boudicca_cohort()
        create_beth_and_ellen_students()
        create_labs()
        create_pair()
        create_keywords()
        associate_labs_to_keywords()
        associate_labs_to_keywords()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["student_id"] = 1
                sess["cohort_id"] = 1

        result = self.client.get("/lab/1")
        self.assertIn("Balloonicorn Melon Festival", result.data)
        self.assertIn("Ellen Bellen", result.data)
        self.assertIn("word", result.data)


################################################################################


if __name__ == "__main__":

    unittest.main()
