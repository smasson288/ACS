from django.test import TestCase, Client
import unittest
from django.urls import reverse
from .models import *

SUCCESS_REDIRECT = 302
OK = 200


#start of functional tests

# Program
class FunctionalTestProgram(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/staffCreateAccount/', {'username': 'staff', 'password': 'teacher',
                                                    'password_reenter': 'teacher'})
        School.objects.create(School_id=999,
            School_desc = 'dummy school',
            School_name = 'School of Dummy',
            Address_street = 'Rainbow Road',
            Address_city = 'Testville',
            Address_state = 'Test',
            Address_zipcode = '55555')

    #School Official Program is Posted
    def test_postSuccess(self):
        self.client = Client()
        self.client.post('/login/0', {'username': 'staff', 'password': 'teacher'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': 2019,
                                             'tests': True,
                                             'statement_of_purpose': True,
                                             'personal_statement': False,
                                             'references': True,
                                             'official_transcript': True})
        self.assertTrue(Program.objects.all())

    def test_postAlreadyExists(self):
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': True,
                                             'statement_of_purpose': True,
                                             'personal_statement': False,
                                             'references': True,
                                             'official_transcript': True})

        response = self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': True,
                                             'statement_of_purpose': True,
                                             'personal_statement': False,
                                             'references': True,
                                             'official_transcript': True})
        self.assertTrue(response.status_code, 302)

    def test_postEmptyFields(self):
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.post('/createProgram/', {'university_name': '',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': True,
                                             'statement_of_purpose': True,
                                             'personal_statement': False,
                                             'references': True,
                                             'official_transcript': True})
        self.assertTrue(not Program.objects.all())

    def test_postWrongType(self):
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'String',
                                             'statement_of_purpose': 'Yes',
                                             'personal_statement': 'not a boolean',
                                             'references': True,
                                             'official_transcript': True})

        self.assertFalse(Program.objects.all())


    #Add Program to Checklist ******************************************
    #***************how the fuck do we do this?*******
    def test_addProgramToChecklist(self):
        testProgram = Program.objects.create(Program_id=2, Major='COGS', Degree='masters', School_id_id=999)
        testStaff = User.objects.create(username='teststaff', password='teststaff', school_id=999)
        testRequirement = Requirement.objects.create(Requirement_id=1, Program_id=testProgram, Created_by=testStaff,
            Certified=True, Term_season='Spring', Term_year='2019', Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)

        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('addToChecklist/1')
        self.assertTrue(Checklist.objects.all())


    #Give Feedback on Program ************************* how to do choice fields****************
    def test_feedbackSuccess(self):
        testProgram = Program.objects.create(Program_id=2, Major='COGS', Degree='masters', School_id_id=999)
        testStaff = User.objects.create(username='teststaff', password='teststaff', school_id=999)
        testRequirement = Requirement.objects.create(Requirement_id=1, Program_id=testProgram, Created_by=testStaff,
            Certified=True, Term_season='Spring', Term_year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)
        testChecklist = Checklist.objects.create(Checklist_id=1, Requirement_id=testRequirement, Student_id_id=1,
            Term_season='Spring', Term_Year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)

        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/feedback/1', {'school_name': 'School of Dummy', 'gpa': 4.0, 'tests': 'yes', 'reference': 'three',
                            'research': 'N/A', 'publication': 'N/A', 'other_comment': 'great program',
                                         'admission_result': 'ACCEPTED'})
        self.assertTrue(Feedback.objects.all())

    def test_feedbackAlreadyGiven(self):
        testProgram = Program.objects.create(Program_id=2, Major='COGS', Degree='masters', School_id_id=999)
        testStaff = User.objects.create(username='teststaff', password='teststaff', school_id=999)
        testRequirement = Requirement.objects.create(Requirement_id=1, Program_id=testProgram, Created_by=testStaff,
            Certified=True, Term_season='Spring', Term_year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)
        testChecklist = Checklist.objects.create(Checklist_id=1, Requirement_id=testRequirement, Student_id_id=1,
            Term_season='Spring', Term_Year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)

        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/feedback/1', {'school_name': 'School of Dummy', 'gpa': 4.0, 'tests': 'yes', 'reference': 'three',
                            'research': 'N/A', 'publication': 'N/A', 'other_comment': 'great program',
                                         'admission_result': 'ACCEPTED'})
        response = self.client.post('/feedback/1', {'school_name': 'School of Dummy', 'gpa': 4.0, 'tests': 'yes', 'reference': 'three',
                            'research': 'N/A', 'publication': 'N/A', 'other_comment': 'bad program',
                                         'admission_result': 'ACCEPTED'})
        self.assertEqual(response.status_code, 302)

    def test_feedbackEmptyField(self):
        testProgram = Program.objects.create(Program_id=2, Major='COGS', Degree='masters', School_id_id=999)
        testStaff = User.objects.create(username='teststaff', password='teststaff', school_id=999)
        testRequirement = Requirement.objects.create(Requirement_id=1, Program_id=testProgram, Created_by=testStaff,
            Certified=True, Term_season='Spring', Term_year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)
        testChecklist = Checklist.objects.create(Checklist_id=1, Requirement_id=testRequirement, Student_id_id=1,
            Term_season='Spring', Term_Year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)

        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.post('/feedback/1', {'school_name': '', 'gpa': 4.0, 'tests': '', 'reference': '',
                            'research': '', 'publication': '', 'other_comment': '',
                                         'admission_result': ''})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Feedback.objects.all())


    #Checklist
class FunctionalTestChecklist(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/staffCreateAccount/', {'username': 'staff', 'password': 'teacher',
                                                    'password_reenter': 'teacher'})
        School.objects.create(School_id=999,
            School_desc = 'dummy school',
            School_name = 'School of Dummy',
            Address_street = 'Rainbow Road',
            Address_city = 'Testville',
            Address_state = 'Test',
            Address_zipcode = '55555')
        testProgram = Program.objects.create(Program_id=2, Major='COGS', Degree='masters', School_id_id=999)
        testStaff = User.objects.create(username='teststaff', password='teststaff', school_id=999)
        testRequirement = Requirement.objects.create(Requirement_id=1, Program_id=testProgram, Created_by=testStaff,
            Certified=True, Term_season='Spring', Term_year=2019, Recommendation_letters=True, Transcript=True,
            Tests=True, Statement_of_purpose=True, Personal_statement=True)
        testChecklist = Checklist.objects.create(Checklist_id=1, Requirement_id=testRequirement, Student_id_id=1,
            Term_season='Spring', Term_Year=2019, Recommendation_letters=False, Transcript=False,
            Tests=False, Statement_of_purpose=False, Personal_statement=False)

    #Check Off Items from Checklist*************************can't get it to work***
    #**********still need to do other 2 tests once figure it out*******
    def test_CheckOffItems(self):
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/checklist/', {'tests': True, 'statement_of_purpose': True, 'personal_statement': False,
                                         'references': False, 'official_transcript': False})
        self.assertTrue(Checklist.objects.filter(Tests=True, Statement_of_purpose=True))

    def test_ChecklistFormNotValid(self):
        self.assertTrue(False)

    def test_ChecklistItemNotExist(self):
        self.assertTrue(False)



    #Search
class FunctionalTestSearch(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})

    #Search for Programs
    def test_SearchSuccess(self):
        School.objects.create(School_id=999,
            School_desc = 'dummy school',
            School_name = 'School of Dummy',
            Address_street = 'Rainbow Road',
            Address_city = 'Testville',
            Address_state = 'Test',
            Address_zipcode = '55555')
        Program.objects.create(Program_id=2, Major='CS', Degree='PhD', School_id_id=999)
        response = self.client.post('/search/', {'university_name': 'School of Dummy', 'degree_type': 'PhD', 'major': 'CS'})
        self.assertTrue('programs' in response.context)

    def test_SearchNotExist(self):
        response = self.client.post('/search/', {'university_name': 'School of Dummy', 'degree_type': 'PhD', 'major': 'CS'})
        self.assertFalse('programs' in response.context)

    def test_SearchBadForm(self):
        School.objects.create(School_id=999,
            School_desc = 'dummy school',
            School_name = 'School of Dummy',
            Address_street = 'Rainbow Road',
            Address_city = 'Testville',
            Address_state = 'Test',
            Address_zipcode = '55555')
        Program.objects.create(Program_id=2, Major='CS', Degree='PhD', School_id_id=999)
        response = self.client.post('/search/', {'university_name': '', 'degree_type': '', 'major': ''})
        self.assertFalse('programs' in response.context)


#Login
class FunctionalTestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})

    #Login to Account
    def test_LoginSuccess(self):
        response = self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.assertRedirects(response, '/checklist/')

    def test_LoginWrongPassword(self):
        response = self.client.post('/login/0', {'username': 'student', 'password': 'wrongPassword'})
        self.assertEquals(response.status_code, 200)

    def test_LoginWrongUsername(self):
        response = self.client.post('/login/0', {'username': 'nobody', 'password': 'schoolisfun'})
        self.assertEquals(response.status_code, 200)

    def test_LoginBadField(self):
        response = self.client.post('/login/0', {'username': '', 'password': ''})
        self.assertEquals(response.status_code, 200)


#Signup
class FunctionalTestSignup(TestCase):
    def setUp(self):
        self.client = Client()

    #Create a Student Account
    def test_CreateStudentSuccess(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.assertTrue(User.objects.filter(username='student'))

    def test_CreateStudentUsernameAlreadyExist(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        response = self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisnotfun',
                                                    'password_reenter': 'schoolisnotfun'})
        self.assertEqual(response.status_code, 200)

    def test_CreateStudentMissingField(self):
        response = self.client.post('/studentCreateAccount/', {'username': '', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.assertEqual(response.status_code, 200)

    def test_CreateStudentMismatchPassword(self):
        response = self.client.post('/studentCreateAccount/', {'username': '', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisboring'})
        self.assertEqual(response.status_code, 200)


    #Create a Staff Account
    def test_CreateStaffSucces(self):
        self.client.post('/staffCreateAccount/', {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                                        'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                                        'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.assertTrue(User.objects.filter(username='staff'))

    def test_CreateStaffUsernameAlreadyExists(self):
        self.client.post('/staffCreateAccount/', {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                                        'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                                        'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        response = self.client.post('/staffCreateAccount/', {'institution_name': 'not CWRU', 'address_street': 'Rainbow Road',
                                        'address_city': 'fake city', 'address_state': 'Old Delaware', 'zipcode': '55556',
                                        'username': 'staff', 'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.assertTrue(response.status_code, 200)

    def test_CreateStaffEmptyField(self):
        response = self.client.post('/staffCreateAccount/', {'institution_name': '', 'address_street': '', 'address_city': '',
                                        'address_state': '', 'zipcode': '', 'username': '',
                                        'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.assertEqual(response.status_code, 200)

    def test_CreateStaffMismatchPassword(self):
        response = self.client.post('/staffCreateAccount/', {'institution_name': 'CWRU', 'address_street': 'Rainbow Road',
                                        'address_city': 'fake city', 'address_state': 'New Delaware', 'zipcode': '55555',
                                        'username': 'staff', 'password': 'IamStaff', 'password_reenter': 'IamStudent'})
        self.assertEqual(response.status_code, 200)
