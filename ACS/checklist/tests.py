from django.test import TestCase, Client
import unittest
from django.urls import reverse

SUCCESS_REDIRECT = 302
OK = 200


class TestChecklist(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, OK)

    def test_login_student(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        response = self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/checklist/')

    '''
    def test_login_staff(self):
        self.client.post('/staffCreateAccount/', {'institution_name': 'CWRU', 'username': 'staff1',
                                                  'password': 'Iamschool', 'password_reenter': "Iamschool"})
        response = self.client.post('/login/', {'username': 'staff1', 'password': 'Iamschool'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/checklist/')
    '''

    def test_dup_username(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                               'password_reenter': 'Iheartschool'})
        response = self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                               'password_reenter': 'Iheartschool'})
        self.assertEqual(response.status_code, OK)

    def test_failed_login(self):
        response = self.client.post('/login/', {'username': 'skateboarddude24', 'password': 'halfpipe'})
        self.assertEqual(response.status_code, OK)

    def test_unauthenticated_checklist(self):
        response = self.client.post('/checklist/')
        self.assertEqual(response.url, '/login/')

    def test_program_detail(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        response = self.client.post('/createProgram/', {'university_name': 'CWRU',
                                                        'degree_type': 'masters',
                                                        'major': 'CS',
                                                        'tests': True,
                                                        'statement_of_purpose': True,
                                                        'personal_statement': False,
                                                        'references': True,
                                                        'official_transcript': True})
        self.assertEquals(response.url, '/checklist/')
        response = self.client.get(reverse('checklist:detail_program', args=['0']))
        self.assertEqual(response.status_code, OK)

    def test_search_program(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
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
        self.assertTrue(response.context['programs'])

    def test_search_program_not_found(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        response = self.client.post('/search/', {'university_name': 'CWRU', 'degree_type': 'masters', 'major': 'CSS'})
        self.assertEqual(response.status_code, OK)
        self.assertFalse('programs' in response.context)

    def test_add_program_to_checklist(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        self.client.post('/createProgram/', {'university_name': 'CWRU',
                                                        'degree_type': 'masters',
                                                        'major': 'CS',
                                                        'tests': True,
                                                        'statement_of_purpose': True,
                                                        'personal_statement': False,
                                                        'references': True,
                                                        'official_transcript': True})
        response = self.client.post(reverse('checklist:detail_program', args=['0']))
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        self.assertEqual(response.url, '/checklist/')
        response = self.client.get('/checklist/')
        self.assertTrue(response.context['checklists'] != [])

    def test_default_empty_checklist(self):
        self.client = Client()
        self.client.post('/studentCreateAccount/', {'username': 'studentt', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        self.client.post('/login/', {'username': 'studentt', 'password': 'Iheartschool'})
        response = self.client.get('/checklist/')
        self.assertTrue(response.context['checklists'] == [])
