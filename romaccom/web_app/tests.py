from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from web_app.views import index, home_view
from web_app.models import User, UserProfile, Operator, OperatorProfile, Accommodation, Review, Image, AccommodationImage
from web_app.models import validate_glasgow_postcode
from web_app.models import validate_uk_address
from django.core.files.uploadedfile import SimpleUploadedFile

#TESTING MODELS

class PostCodeAndAddressValidation(TestCase):
    def test_postcode_validate(self): 
        invalid_postcodes =["g1","E1","G100",""]      
        for pc in invalid_postcodes:
            with self.assertRaises(ValidationError):
                validate_glasgow_postcode(pc)
                self.assertEqual(ValidationError, f"{pc} is not a valid Glasgow postcode. Use only the first part (e.g., G1, G2, G12)" )

    def test_address_validate(self): 
        invalid_addresses = ["Main Street","123","123 @Main Street","","   ",]
        for address in invalid_addresses:
            with self.assertRaises(ValidationError):
                validate_uk_address(address)
                self.assertEqual(ValidationError, "Address must start with a number followed by a street name.")


        

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

class UserProfileModelTests(TestCase):
    def test_one_profile_per_user(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        profile = UserProfile.objects.create(user=user)

        profile, created = UserProfile.objects.get_or_create(user=user)
        self.assertFalse(created)
    
    def test_profile_deletion(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        profile = UserProfile.objects.create(user=user)

        user.delete()
        self.assertEqual(UserProfile.objects.count(),0)
    
    def test_user_profile_access(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(user.profile, profile)

    def test_valid_url(self):
        user = User.objects.create_user(username="testname", password="password123")
        profile = UserProfile.objects.create(user=user, website="https://example.com")
    
        self.assertEqual(profile.website,"https://example.com")

    def test_invalid_url(self):
        user = User.objects.create_user(username="testname", password="password123")
        profile = UserProfile.objects.create(user=user, website="invalid_url")
    
        with self.assertRaises(ValidationError):
            profile.full_clean()

   # def test_invalid_image(self):
   #     user = User.objects.create_user(username="testname", password="password123")
    #    invalid_file = SimpleUploadedFile(name="document.txt", content=b"This is not an image.", content_type="text/plain")
     #   profile = UserProfile.objects.create(user=user, picture =invalid_file)
    
      #  with self.assertRaises(ValidationError):
       #     profile.save()

    def test_blank_website(self):
        user = User.objects.create_user(username="testname", password="testpassword")
        profile = UserProfile.objects.create(user=user, website="")  
        
        self.assertFalse(profile.website)

    def test_blank_picture(self):
       
        user = User.objects.create_user(username="testname", password="testpassword")
        profile = UserProfile.objects.create(user=user, picture="") 
        
       
        self.assertFalse(profile.picture)  

class OperatorModelTest(TestCase):
    def test_create_operator(self):
        operator = Operator.objects.create(
            name="Test Operator",
            email="test@example.com",
            password="securepassword"
        )
        self.assertEqual(str(operator), "Test Operator")

    def test_operator_email_field(self):
        operator = Operator.objects.create(
            name="Test Operator",
            email="test@example.com",
            password="securepassword"
        )
        self.assertEqual(operator.email, "test@example.com")

    def test_operator_password_field(self):
        operator = Operator.objects.create(
            name="Test Password",
            email="testpass@example.com",
            password="securepassword123"
        )
        self.assertEqual(operator.password, "securepassword123")

    def test_operator_email_optional(self):
        operator = Operator.objects.create(
            name="No Email Operator",
            password="securepassword"
        )
        self.assertIsNone(operator.email)

class OperatorProfileModelTest(TestCase):
    def test_create_operator_profile(self):
        operator = Operator.objects.create(name="Test Operator", email="test@example.com", password="password123")
        profile = OperatorProfile.objects.create(
            operator=operator,
            description="A great business",
            website="https://example.com"
        )
        self.assertEqual(str(profile), "Test Operator's Profile")
        self.assertEqual(profile.website, "https://example.com")

    def test_operator_profile_only_one(self):
        
        operator = Operator.objects.create(name="Unique Profile Operator", email="unique@example.com", password="password123")
        OperatorProfile.objects.create(operator=operator)

        with self.assertRaises(Exception): 
            OperatorProfile.objects.create(operator=operator)
    
    def test_operator_profile_description_optional(self):
        operator = Operator.objects.create(name="Blank Fields Operator", email="blank@example.com", password="password123")
        profile = OperatorProfile.objects.create(operator=operator)

        self.assertEqual(profile.description, "") 

    def test_operator_profile_website_optional(self):
        operator = Operator.objects.create(name="Blank Fields Operator", email="blank@example.com", password="password123")
        profile = OperatorProfile.objects.create(operator=operator)

        self.assertEqual(profile.website, "")

    def test_operator_profile_logo_optional(self):
        operator = Operator.objects.create(name="Blank Fields Operator", email="blank@example.com", password="password123")
        profile = OperatorProfile.objects.create(operator=operator)

        self.assertFalse(profile.logo)  

    def test_operator_profile_logo_upload(self):
        
        operator = Operator.objects.create(name="Logo Operator", email="logo@example.com", password="password123")
        image = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        
        profile = OperatorProfile.objects.create(operator=operator, logo=image)
        self.assertTrue(profile.logo)


class AccommodationMethodTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )

    def test_update_average_rating_with_reviews(self):
        Review.objects.create(user=self.user, accommodation=self.accommodation, rating=4, review_text="Good")
        Review.objects.create(user=self.user, accommodation=self.accommodation, rating=2, review_text="Okay")

        self.accommodation.update_average_rating()
        expected_rating = (4 + 2) / 2
        self.assertAlmostEqual(self.accommodation.average_rating, expected_rating, places=1)

    def test_update_average_rating_without_reviews(self):
        self.accommodation.update_average_rating()
        self.assertEqual(self.accommodation.average_rating, 0)

    def test_increment_view_count(self):
        initial_count = self.accommodation.view_count
        self.accommodation.increment_view_count()
        self.assertEqual(self.accommodation.view_count, initial_count + 1)

class ReviewMethodTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            rating=4,
            review_text="Good place"
            )

        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.accommodation.name, "Test Hotel")
        self.assertEqual(review.accommodation.address, "123 Main Street")
        self.assertEqual(review.accommodation.postcode, "G1")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.review_text, "Good place")

class ImageMethodTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )
        self.review = Review.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            rating=4,
            review_text="Good place"
        )

    def test_image_creation(self):
        image = Image.objects.create(
            review=self.review,
            image="review_images/test.jpg"
        )

        self.assertEqual(image.review, self.review)
        self.assertEqual(image.image, "review_images/test.jpg")

class AccommodationImageMethodTest(TestCase):
    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )

    def test_accommodation_image_creation(self):
        accom_image = AccommodationImage.objects.create(
            accommodation=self.accommodation,
            image="accommodation_images/test.jpg"
        )

        self.assertEqual(accom_image.accommodation, self.accommodation)
        self.assertEqual(accom_image.image, "accommodation_images/test.jpg")
        self.assertFalse(accom_image.is_main)

#TESTING VIEWS

class IndexPageViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
       #Create accommodations with different view counts and ratings.
       
        cls.accommodation1 = Accommodation.objects.create(name="Accom 1", view_count=100, average_rating=4.5)
        cls.accommodation2 = Accommodation.objects.create(name="Accom 2", view_count=200, average_rating=3.0)
        cls.accommodation3 = Accommodation.objects.create(name="Accom 3", view_count=50, average_rating=5.0)
        cls.accommodation4 = Accommodation.objects.create(name="Accom 4", view_count=250, average_rating=2.0)
        cls.accommodation5 = Accommodation.objects.create(name="Accom 5", view_count=150, average_rating=4.8)
        cls.accommodation6 = Accommodation.objects.create(name="Accom 6", view_count=300, average_rating=3.5)

    def test_index_view_status_code(self):
        #Test if the index page loads successfully (status code 200)
        response = self.client.get(reverse('index')) 
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'romaccom/home.html')

    def test_trending_accommodations_order_by_view_count(self):
        
        response = self.client.get(reverse('index'))
        trending_accommodations = list(response.context['trending_accommodations'])

        expected_order = [
            self.accommodation6,  # 300 views
            self.accommodation4,  # 250 views
            self.accommodation2,  # 200 views
            self.accommodation5,  # 150 views
            self.accommodation1,  # 100 views
        ]
        self.assertEqual(trending_accommodations, expected_order)

    def test_trending_accommodations_top_five(self):
        """ Ensure only the top 5 accommodations by view count are included in trending. """
        response = self.client.get(reverse('index'))
        trending_accommodations = list(response.context['trending_accommodations'])

        # Expected top 5 accommodations based on view_count
        expected_top_5 = [
            self.accommodation6,  # 300 views
            self.accommodation4,  # 250 views
            self.accommodation2,  # 200 views
            self.accommodation5,  # 150 views
            self.accommodation1,  # 100 views
        ]
        self.assertNotIn(self.accommodation3, trending_accommodations)

    def test_top_rated_accommodations_ordered_by_average_rating(self):
        
        response = self.client.get(reverse('index'))
        top_rated_accommodations = list(response.context['top_rated_accommodations'])

        expected_order = [
            self.accommodation3,  # 5.0 rating
            self.accommodation5,  # 4.8 rating
            self.accommodation1,  # 4.5 rating
            self.accommodation6,  # 3.5 rating
            self.accommodation2,  # 3.0 rating
        ]
        self.assertEqual(top_rated_accommodations, expected_order)

class HomePageViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.accommodation1 = Accommodation.objects.create(name="Accom 1", view_count=100, average_rating=4.5)
        cls.accommodation2 = Accommodation.objects.create(name="Accom 2", view_count=200, average_rating=3.0)
        cls.accommodation3 = Accommodation.objects.create(name="Accom 3", view_count=50, average_rating=5.0)
        cls.accommodation4 = Accommodation.objects.create(name="Accom 4", view_count=250, average_rating=2.0)
        cls.accommodation5 = Accommodation.objects.create(name="Accom 5", view_count=150, average_rating=4.8)
        cls.accommodation6 = Accommodation.objects.create(name="Accom 6", view_count=300, average_rating=3.5)

    

    def test_home_view_top_rated_accommodations(self):
        
        response = self.client.get(reverse('home'))
        top_rated_accommodations = response.context['top_rated_accommodations']
        expected_top_rated = [self.accommodation3, self.accommodation5, self.accommodation1, self.accommodation6, self.accommodation2]

        self.assertEqual(list(top_rated_accommodations), expected_top_rated)

    def test_home_view_trending_accommodations(self):
    
        response = self.client.get(reverse('home'))
        trending_accommodations = response.context['trending_accommodations']
        expected_trending = [self.accommodation6, self.accommodation4, self.accommodation2, self.accommodation5, self.accommodation1]

        self.assertEqual(list(trending_accommodations), expected_trending)

    def test_home_view_operator_logic_logged_in(self):
        session = self.client.session
        session['operator_id'] = 1
        session['operator_name'] = 'Test Operator'
        session.save()

        response = self.client.get(reverse('home'))  

        self.assertTrue(response.context['operator_logged_in']) 
        

    def test_home_view_operator_logic_not_logged_in(self):
        response = self.client.get(reverse('home'))

        self.assertFalse(response.context['operator_logged_in'])



