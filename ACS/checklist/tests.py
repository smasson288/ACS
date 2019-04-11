from django.test import TestCase, Client
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
                                                    'password_reenter': 'teacher', 'institution_name': 'CWRU',
                                                  'address_street':'11100 Euclid Ave', 'address_city':'Cleveland',
                                                  'address_state':'OH','zipcode':'44106'})
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
        self.client.get('/createProgram/')
        self.client.post('/createProgram/', {
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        self.assertEqual(Program.objects.all().count(), 1)

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
        response = self.client.post('/createProgram/', {
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': True,
                                             'statement_of_purpose': True,
                                             'personal_statement': False,
                                             'references': True,
                                             'official_transcript': True})
        self.assertEqual(Program.objects.all().count(), 0)

    def test_postWrongType(self):
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        initialCount = Program.objects.all().count()
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'String',
                                             'statement_of_purpose': 'Yes',
                                             'personal_statement': 'not a boolean',
                                             'references': True,
                                             'official_transcript': True})

        self.assertEqual(Program.objects.all().count(), initialCount)

    def test_addProgramToChecklist(self):
        self.client = Client()
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.get('/createProgram/')
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        self.client.get('/program/0')
        response = self.client.post('/addToChecklist/0')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(Checklist.objects.all().count(), 1)

    def test_feedbackSuccess(self):
        self.client = Client()
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        self.client.post('/addToChecklist/0')
        self.client.get('/feedback/0')
        self.client.post('/feedback/0', {'school_name': 'School of Dummy', 'gpa': '4', 'tests': '123', 'reference':
                         'three', 'research': 'N/A', 'publication': 'N/A', 'other_comment': 'great program',
                         'admission_result': 'ACCEPTED'})
        self.assertEqual(Feedback.objects.all().count(), 1)


    def test_feedbackAlreadyGiven(self):
        self.client = Client()
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        print()
        self.client.post('/addToChecklist/0')
        self.client.get('/feedback/0')
        self.client.post('/feedback/0', {'school_name': 'School of Dummy', 'gpa': '4', 'tests': '123', 'reference':
            'three', 'research': 'N/A', 'publication': 'N/A', 'other_comment': 'great program',
                                         'admission_result': 'ACCEPTED'})
        response = self.client.get('/feedback/0')
        self.assertEqual(response.status_code, 302)



    def test_feedbackEmptyField(self):
        self.client = Client()
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        print()
        self.client.post('/addToChecklist/0')
        self.client.get('/feedback/0')
        self.client.post('/feedback/0', {'school_name': 'School of Dummy', 'gpa': '4', 'tests': '123', 'reference':
                         'three', 'publication': 'N/A', 'other_comment': 'great program',
                         'admission_result': 'ACCEPTED'})
        self.assertEqual(Feedback.objects.all().count(), 0)


    # Checklist
class FunctionalTestChecklist(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        self.client.post('/addToChecklist/0')

    # Check Off Items from Checklist
    def test_CheckOffItems(self):
        response = self.client.post('/checklist/', {'checklist_id': '0', 'tests': 'on', 'statement_of_purpose': 'on',
                                    'personal_statement': 'on', 'references': 'on', 'official_transcript': 'on'})
        cl = Checklist.objects.get(Checklist_id=0)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cl.Personal_statement)
        self.assertTrue(cl.Recommendation_letters)
        self.assertTrue(cl.Transcript)
        self.assertTrue(cl.Tests)
        self.assertTrue(cl.Statement_of_purpose)

    def test_ChecklistFormNotValid(self):
        cl = Checklist.objects.get(Checklist_id=0)
        oldps = cl.Personal_statement
        oldrl = cl.Recommendation_letters
        oldts = cl.Transcript
        oldt = cl.Tests
        oldsop = cl.Statement_of_purpose
        response = self.client.post('/checklist/', {'checklist_id': '0', 'tests': 'on', 'statement_of_purpose': 'on',
                                    'personal_statement': 'what', 'official_transcript': 'on'})
        cl = Checklist.objects.get(Checklist_id=0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cl.Personal_statement, oldps)
        self.assertEqual(cl.Recommendation_letters, oldrl)
        self.assertEqual(cl.Transcript, oldts)
        self.assertEqual(cl.Tests, oldt)
        self.assertEqual(cl.Statement_of_purpose, oldsop)

    def test_ChecklistItemNotExist(self):
        response = self.client.post('/checklist/', {'checklist_id': '2', 'tests': 'on', 'statement_of_purpose': 'on',
                                                    'personal_statement': 'what', 'official_transcript': 'on'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/')


# Search
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
        response = self.client.get('/search/')
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
        self.client.get('/studentCreateAccount/')
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
        response = self.client.post('/studentCreateAccount/', {'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.assertEqual(response.status_code, 200)

    def test_CreateStudentMismatchPassword(self):
        response = self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisboring'})
        self.assertEqual(response.status_code, 200)


    #Create a Staff Account
    def test_CreateStaffSucces(self):
        self.client.get('/staffCreateAccount/')
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


class FunctionalExtraTests(TestCase):
    def test_index_anonymous(self):
        self.client = Client()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_not_anonymous(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.get('/login/1')
        response = self.client.get('/checklist/')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)

    def test_student_logged_in_create_another_account(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.get('/studentCreateAccount/')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)

    def test_staff_logged_in_create_another_account(self):
        self.client = Client()
        self.client.post('/staffCreateAccount/', {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                                        'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                                        'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.client.post('/login/0', {'username': 'staff', 'password': 'IamStaff'})
        response = self.client.get('/staffCreateAccount/')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)

    def test_staff_main_page(self):
        self.client = Client()
        self.client.post('/staffCreateAccount/',
                         {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                          'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                          'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.client.post('/login/0', {'username': 'staff', 'password': 'IamStaff'})
        response = self.client.get('/staff/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_attempt_to_staff_main(self):
        self.client = Client()
        response = self.client.get('/staff/')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        response = self.client.get('/staff/')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)

    def test_deleteChecklist(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        self.client.post('/addToChecklist/0')
        self.client.get('/deleteChecklist/0')
        self.assertEqual(Checklist.objects.all().count(), 0)

    def test_staff_delete_checklist(self):
        self.client = Client()
        self.client.post('/staffCreateAccount/',
                         {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                          'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                          'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.client.post('/login/0', {'username': 'staff', 'password': 'IamStaff'})
        response = self.client.get('/deleteChecklist/0')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/staff/')

    def test_create_new_req_for_program(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        initial_count = Requirement.objects.all().count()
        self.client.post('/program/0', {'term': 'Fall', 'year': '2019', 'tests': 'on', 'statement_of_purpose': 'on'})
        self.assertEqual(Requirement.objects.all().count(), initial_count + 1)

    def test_anonymous_post_on_program_page(self):
        self.client = Client()
        response = self.client.post('/program/0', {'term': 'Fall', 'year': '2019', 'tests': 'on', 'statement_of_purpose': 'on'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/login/0')

    def test_staff_post_on_program_page(self):
        self.client = Client()
        self.client.post('/staffCreateAccount/',
                         {'institution_name': 'CWRU', 'address_street': 'Rainbow Road', 'address_city': 'fake city',
                          'address_state': 'New Delaware', 'zipcode': '55555', 'username': 'staff',
                          'password': 'IamStaff', 'password_reenter': 'IamStaff'})
        self.client.post('/login/0', {'username': 'staff', 'password': 'IamStaff'})
        response = self.client.post('/program/0', {'term': 'Fall', 'year': '2019', 'tests': 'on',
                                                   'statement_of_purpose': 'on'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/staff/')

    def test_anonymous_delete_checklist(self):
        self.client = Client()
        response = self.client.get('/deleteChecklist/0')
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/login/0')

    def test_stat_filter_with_year(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        response = self.client.post('/programFilter/0', {'year': '2019', 'admission_result': 'ACCEPTED'})
        self.assertEqual(response.status_code, 200)

    def test_stat_filter_without_year(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'schoolisfun',
                                                    'password_reenter': 'schoolisfun'})
        self.client.post('/login/0', {'username': 'student', 'password': 'schoolisfun'})
        self.client.post('/createProgram/', {'university_name': 'School of Dummy',
                                             'degree_type': 'masters',
                                             'major': 'CS',
                                             'term': 'Spring',
                                             'year': '2019',
                                             'tests': 'on',
                                             'statement_of_purpose': 'on',
                                             'personal_statement': 'on',
                                             'references': 'on',
                                             'official_transcript': 'on'
                                             })
        response = self.client.post('/programFilter/0', {'admission_result': 'ACCEPTED'})
        self.assertEqual(response.status_code, 200)

