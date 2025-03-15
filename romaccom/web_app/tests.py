from django.test import TestCase
from web_app.models import User

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertIsInstance(user,User)
    
    def test_name_of_user(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertEqual(user.username, "testname")
        