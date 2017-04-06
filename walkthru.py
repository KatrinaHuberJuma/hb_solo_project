import unittest
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from server import app, session
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from test_seed import create_admin
from time import sleep






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



    def test_admin_view_signin_page(self):

        """Addy views the signin page"""

        self.browser.get('http://localhost:5000/signin')
        self.assertEqual(self.browser.title, "Kat Signin")


    def test_admin_signin(self):
        """Addy enters her name and password and hits submit button"""

        self.browser.get('http://localhost:5000/signin')

        self.browser.find_element_by_id("admin-radio").click()
        name = self.browser.find_element_by_id("signin-name")
        name.send_keys("Addy Gladdy")
        password = self.browser.find_element_by_id("signin-password")
        password.send_keys("pw")

        password.submit()
        self.assertEqual(self.browser.find_element_by_id("cohort1")
            .get_attribute("innerHTML"), "Boudicca")



if __name__ == "__main__":
    unittest.main()