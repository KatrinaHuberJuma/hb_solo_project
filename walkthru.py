import unittest
from time import sleep
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from server import app
import server
from selenium import webdriver
from test_seed import create_admin, create_cohort


class UserSignin(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

        create_admin()
        create_cohort()

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




class AddyAdmin(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

        create_admin()
        create_cohort()

        cls.browser = webdriver.Chrome()

        cls.browser.get('http://localhost:5000/signin')

        cls.browser.find_element_by_id("admin-radio").click()
        name = cls.browser.find_element_by_id("signin-name")
        name.send_keys("Addy Gladdy")
        password = cls.browser.find_element_by_id("signin-password")
        password.send_keys("pw")
        password.submit()





    @classmethod
    def tearDownClass(cls):

        cls.browser.quit()

        db.drop_all()
        db.session.close()



    def test_admin_create_cohort(self):
        """Addy creates a new cohort called "Joan" with the password "pw"""


        self.browser.get('http://localhost:5000/')

        new_name = self.browser.find_element_by_id("enter-cohort-name")
        new_name.send_keys("Joan")

        new_password = self.browser.find_element_by_id("enter-cohort-password")
        new_password.send_keys("pw")

        new_password.submit()

        sleep(.5)

        self.assertEqual(self.browser.find_element_by_id("new-cohort")
            .get_attribute("innerHTML"), '<a href="2">Joan</a>')




if __name__ == "__main__":
    unittest.main()