from django.test import TestCase
from django.core.exceptions import ValidationError
from web_app.models import User, UserProfile, Operator, OperatorProfile, Accommodation, Review, Image, AccommodationImage
from web_app.models import validate_glasgow_postcode
from web_app.models import validate_uk_address
from django.core.files.uploadedfile import SimpleUploadedFile


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


