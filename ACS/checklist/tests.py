from django.test import TestCase, Client
import unittest

SUCCESS_REDIRECT = 302
OK = 200

# Create your tests here.
class TestChecklist(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, OK)

    def test_login_student(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool'})
        response = self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/checklist/')

    def test_dup_username(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'iheartschool'})
        self.client.post('/login/', {'username': 'student', 'password': 'iheartschool'})
        #self.client.post(response.build_absolute_uri('/'), {})
        response = self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Ihateschool'})
        self.assertEqual(response.status_code, OK)

    def test_failed_login(self):
        response = self.client.post('/login/', {'username': 'skateboarddude24', 'password': 'halfpipe'})
        self.assertEqual(response.status_code, OK)

    def test_unauthenticated_checklist(self):
        response = self.client.post('/checklist/')
        self.assertEqual(response.url, '/login/')

    def test_program_detail(self):
        response = self.client.post('/createProgram/', {'university_name': 'CWRU',
                                                        'degree_type': 'masters',
                                                        'major': 'CS',
                                                        'tests': True,
                                                        'statement_of_purpose': True,
                                                        'personal_statement': False,
                                                        'references': True,
                                                        'official_transcript': True})
        self.assertEquals(response.url, '/checklist/')
        response = self.client.post('/program/0/')
        self.assertEqual(response.status_code, OK)


    def test_search_program(self):
        self.client.post('/createProgram/', {'university_name': 'CWRU',
                                                        'degree_type': 'masters',
                                                        'major': 'CS',
                                                        'tests': True,
                                                        'statement_of_purpose': True,
                                                        'personal_statement': False,
                                                        'references': True,
                                                        'official_transcript': True})
        response = self.client.post('/search/', {'university_name': 'CWRU', 'degree_type': 'masters', 'major': 'CS'})
        self.assertEqual(response.status_code, OK)