import unittest
from time import sleep
from model import connect_to_db, db, Admin, Cohort, Student, Lab, Pair, Keyword, LabKeyword
from server import app
import server
from selenium import webdriver
from test_seed import create_admin, create_cohort, create_students


class UserSignin(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

        create_admin()
        create_cohort()
        create_students()

        cls.browser = webdriver.Chrome()



    @classmethod
    def tearDownClass(cls):

        cls.browser.quit()

        db.session.close()
        db.drop_all()



    def test_view_signin_page(self):

        """Addy views the signin page"""

        self.browser.get('http://localhost:5000/signin')
        self.assertEqual(self.browser.title, "Kat Signin")


    def test_admin_signin(self):
        """Addy Gladdy enters her name and password and hits submit button"""

        self.browser.get('http://localhost:5000/signin')

        self.browser.find_element_by_id("admin-radio").click()
        name = self.browser.find_element_by_id("signin-name")
        name.send_keys("Addy Gladdy")
        sleep(1)
        password = self.browser.find_element_by_id("signin-password")
        password.send_keys("pw")
        sleep(1)        
        password.submit()
        self.assertEqual(self.browser.find_element_by_id("cohort1")
            .get_attribute("innerHTML"), "Boudicca")


    def test_student_signin(self):
        """Beth Happy enters her name and password and hits submit button"""

        self.browser.get('http://localhost:5000/signin')

        self.browser.find_element_by_id("student-radio").click()
        name = self.browser.find_element_by_id("signin-name")
        name.send_keys("Beth Happy")
        sleep(1)
        password = self.browser.find_element_by_id("signin-password")
        password.send_keys("pw")
        sleep(1)        
        password.submit()
        sleep(3)   
        self.browser.get('http://localhost:5000/1-profile') # TODO do I still need this if I remove from server.py DebudToolbarExtention(app)? 
        self.assertEqual(self.browser.find_element_by_id("greet-signedin-student")
            .get_attribute("innerHTML"), "Hey Beth Happy! Welcome to your own profile!")


################################################################################




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
        sleep(1)
        new_name = self.browser.find_element_by_id("enter-cohort-name")
        new_name.send_keys("Joan")
        sleep(1)    
        new_password = self.browser.find_element_by_id("enter-cohort-password")
        new_password.send_keys("pw")

        new_password.submit()

        sleep(.5)

        self.assertEqual(self.browser.find_element_by_id("new-cohort")
            .get_attribute("innerHTML"), '<a href="/2/cohort">Joan</a>')



################################################################################


class NewStudent(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()

        connect_to_db(app, "postgresql:///kattestdb")
        db.create_all()

        create_admin()
        create_cohort()
        create_students()

        cls.browser = webdriver.Chrome()



    @classmethod
    def tearDownClass(cls):

        cls.browser.quit()

        db.drop_all()
        db.session.close()



    def test_new_student_join_cohort(self):
        """Pia Miya joins the Boudicca cohort 
        with her name, "pw" as her password and "secretpw" as the cohort password"""


        self.browser.get('http://localhost:5000/cohort1')
        sleep(1)
        new_student_name = self.browser.find_element_by_id("enter-student-name")
        new_student_name.send_keys("Pia Miya")
        new_student_email = self.browser.find_element_by_id("enter-student-email")
        new_student_email.send_keys("pw")
        sleep(1) 
        new_student_password = self.browser.find_element_by_id("enter-student-password")
        new_student_password.send_keys("pw")   
        cohort_password = self.browser.find_element_by_id("enter-this-cohort-password")
        cohort_password.send_keys("secretpw")

        cohort_password.submit()

        sleep(.5)

        self.assertEqual(self.browser.find_element_by_id("new-student")
            .get_attribute("innerHTML"), "Pia Miya")





################################################################################



if __name__ == "__main__":


    unittest.main()