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
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Iheartschool',
                                                    'password_reenter': 'Iheartschool'})
        response = self.client.post('/login/', {'username': 'student', 'password': 'Iheartschool'})
        self.assertEqual(response.status_code, SUCCESS_REDIRECT)
        print(response)
        self.assertEqual(response.url, '/checklist/')

    def test_dup_username(self):
        self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'iheartschool'})
        response = self.client.post('/login/', {'username': 'student', 'password': 'iheartschool'})
        #self.client.post(response.build_absolute_uri('/'), {})
        response = self.client.post('/studentCreateAccount/', {'username': 'student', 'password': 'Ihateschool'})
        self.assertEqual(response.status_code, 200)

    def test_failed_login(self):
        response = self.client.post('/login/', {'username': 'skateboarddude24', 'password': 'halfpipe'})
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_checklist(self):
        response = self.client.post('/checklist/')
        self.assertEqual(response.url, '/login/')

