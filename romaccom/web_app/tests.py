from django.test import TestCase
from django.core.exceptions import ValidationError
from web_app.models import User
from web_app.models import validate_glasgow_postcode
from web_app.models import validate_uk_address


class PostCodeAndAddressValidation(TestCase):

    def test_postcode_validate(self): 
        invalid_postcodes =["g1","E1","G100",""]      
        for pc in invalid_postcodes:
            with self.assertRaises(ValidationError):
                validate_glasgow_postcode(pc)
                self.assertEqual(ValidationError, f"{pc} is not a valid Glasgow postcode. Use only the first part (e.g., G1, G2, G12)" )




        

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertIsInstance(user,User)
    
    def test_username_of_user(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertEqual(user.username, "testname")
        
    def test_default_public(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertEqual(user.account_type, "public")
        self.assertTrue(user.profile_visibility)

    def test_user_full_name(self):
        user = User.objects.create_user(username="testname", first_name="John", last_name="Doe", password="testpassword")
        self.assertEqual(user.get_full_name(), "John Doe") 

    def test_user_short_name(self):
        user = User.objects.create_user(username="testname", first_name="John", last_name="Doe", password="testpassword")
        self.assertEqual(user.get_short_name(), "John") 

    def test_email_field(self):
        user = User.objects.create_user(username="testname", email="test@example.com", password="testpassword")
        self.assertEqual(user.email, "test@example.com")

    def test_user_permissions(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        self.assertFalse(user.is_staff) 
    
    def test_invalid_username(self):
        invalid_usernames = ["invalid username", "user@name", "name!", "name.with.dot"]

        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                user = User(username=username)
                user.full_clean()


