import unittest
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from server import app, session
from selenium import webdriver
from test_seed import create_admin

class AddyAdmin(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()
        app.config['TESTING'] = True # fixme before deployment

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

        create_admin()

        cls.browser = webdriver.Chrome()



    @classmethod
    def tearDownClass(cls):

        cls.browser.quit()

        db.session.close()
        db.drop_all()



    def test_view_signin_page(self):

        self.browser.get('http://localhost:5000/signin')
        self.assertEqual(self.browser.title, "Kat Signin")





if __name__ == "__main__":
    unittest.main()