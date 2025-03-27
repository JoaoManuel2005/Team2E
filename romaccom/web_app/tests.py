from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.urls import reverse
from web_app.views import index, home_view
from web_app.models import User, UserProfile, Operator, OperatorProfile, Accommodation, Review, Image, AccommodationImage
from web_app.models import validate_glasgow_postcode
from web_app.models import validate_uk_address
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from .models import AccommodationImage

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

class MyReviewsViewTest(TestCase):
    def setUp(self):
        #create 2 users
        self.user1 = User.objects.create_user(username="testuser1", password="password123")
        self.user2 = User.objects.create_user(username="testuser2", password="password123")
        #create an accommodation
        self.accom =Accommodation.objects.create(name="Test Hotel", address="123 Main Street", postcode="G1")

        Review.objects.create(user=self.user1, accommodation=self.accom, rating=4, review_text="Good")
        Review.objects.create(user=self.user1, accommodation=self.accom, rating=5, review_text="They help me a lot!!!")
        Review.objects.create(user=self.user2, accommodation=self.accom, rating=2, review_text="BAD!")

        self.client = Client()

    def test_only_logged_in_user_reviews_returned(self):
        self.client.login(username="testuser1", password="password123")
        response = self.client.get(reverse("myreviews"))
        reviews = response.context["reviews"]

        self.assertEqual(len(reviews), 2)
        for review in reviews:
            self.assertEqual(review.user, self.user1)

#class SearchViewTest(TestCase):


class AccomPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.accom = Accommodation.objects.create(name="Test Hotel", address="123 Main St", postcode="G1")
        #creat two views
        self.review1 = Review.objects.create(user=User.objects.create_user("user1"), accommodation=self.accom, rating=4,
                                             review_text="Nice")
        self.review2 = Review.objects.create(user=User.objects.create_user("user2"), accommodation=self.accom, rating=5,
                                             review_text="Great")

        self.image_main = AccommodationImage.objects.create(accommodation=self.accom, image="main.jpg", is_main=True)
        self.image_other = AccommodationImage.objects.create(accommodation=self.accom, image="other.jpg", is_main=False)

        self.operator1 = Operator.objects.create(name="Operator 1")
        self.operator2 = Operator.objects.create(name="Operator 2")
        self.accom.operators.add(self.operator1) #Only operator1 can edit

    def test_view_without_operator(self):
        response = self.client.get(reverse('accommodation_detail', args=[self.accom.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['accommodation'], self.accom)
        self.assertEqual(list(response.context['reviews']),
                         list(Review.objects.filter(accommodation=self.accom).order_by('-created_at')))
        self.assertEqual(response.context['main_image'], self.image_main)
        self.assertFalse(response.context['operator_logged_in'])
        self.assertFalse(response.context['operator_manages_accommodation'])

    def test_view_with_logged_in_operator_not_managing(self):
        session = self.client.session
        session['operator_id'] = self.operator2.id
        session.save()
        response = self.client.get(reverse('accommodation_detail', args=[self.accom.id]))

        self.assertTrue(response.context['operator_logged_in'])
        self.assertFalse(response.context['operator_manages_accommodation'])

    def test_view_with_logged_in_operator_managing(self):
        session = self.client.session
        session['operator_id'] = self.operator1.id
        session.save()
        response = self.client.get(reverse('accommodation_detail', args=[self.accom.id]))
        self.assertTrue(response.context['operator_logged_in'])
        self.assertTrue(response.context['operator_manages_accommodation'])


class AccomReviewsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )
        self.review = Review.objects.create(
            accommodation=self.accommodation,
            user=self.user,
            review_text="Very comfortable",
            rating=4
        )

    def test_accom_reviews_view_returns_correct_template_and_context(self):
        url = reverse('accom_review_detail', args=[self.accommodation.id, self.review.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'romaccom/reviews.html')

        self.assertEqual(response.context['accommodation'], self.accommodation)
        self.assertEqual(response.context['review'], self.review)



#class AccomMapViewTest(TestCase):


class WriteReviewViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test123pass")
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )

    def test_redirects_to_edit_when_review_exists(self):
        Review.objects.create(user=self.user, accommodation=self.accommodation, rating=4, review_text="Nice")
        self.client.login(username="testuser", password="test123pass")

        response = self.client.get(reverse('write_review', args=[self.accommodation.id]))
        existing_review = Review.objects.get(user=self.user, accommodation=self.accommodation)
        self.assertRedirects(response, reverse('edit_review', args=[existing_review.id]))

    def test_get_review_form_if_no_existing_review(self):
        self.client.login(username="testuser", password="test123pass")
        response = self.client.get(reverse('write_review', args=[self.accommodation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/write-review.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['accommodation'], self.accommodation)

    def test_post_valid_review_creates_review(self):
        self.client.login(username="testuser", password="test123pass")
        response = self.client.post(
            reverse('write_review', args=[self.accommodation.id]),
            data={
                'title': 'Great stay!',
                'rating': 5,
                'review_text': 'Really enjoyed the place!'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, accommodation=self.accommodation).exists())

class OperatorLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testUser", password="testpass")
        self.operator = Operator.objects.create(name="testOperator", password="testpass")
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Main Street",
            postcode="G1"
        )

    def test_user_logged_in_cannot_access_operator_login(self):
        self.client.login(username='testUser', password="testpass")
        response = self.client.get(reverse('operator_login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-login.html')
        self.assertContains(response, 'Please log out as user first')

    def test_get_invalid_accommodation_id_shows_error(self):
        invalid_id = 9999
        response = self.client.get(reverse('operator_login') + f'?accommodation_id={invalid_id}')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-login.html')
        self.assertContains(response, 'Accommodation not found')

    def test_valid_operator_login_without_accommodation(self):
        response = self.client.post(reverse('operator_login'), {
            'property_name': "testOperator",
            'password': "testpass"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('management'))

        session = self.client.session
        self.assertEqual(session.get('operator_id'), self.operator.id)
        self.assertEqual(session.get('operator_name'), self.operator.name)

    def test_invalid_operator_login_shows_error(self):
        response = self.client.post(reverse('operator_login'), {
            'property_name': "wrongTestOperator",  # invalid operator not exist
            'password': "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-login.html')
        self.assertContains(response, 'Invalid property name or password')

    def test_operator_does_not_manage_accommodation(self):
        # create an operator
        operator = Operator.objects.create(name="unrelatedOperator", password="op12345")

        # creat an accommodation，but not related an operator
        accommodation = Accommodation.objects.create(
            name="Unrelated Hotel",
            address="999 Test Street",
            postcode="G5"
        )

        response = self.client.post(
            reverse('operator_login') + f'?accommodation_id={accommodation.id}',
            {
                'property_name':"unrelatedOperator",
                'password': "op12345",
                'accommodation_id': accommodation.id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-login.html')
        self.assertContains(response, 'You are not authorized to manage this accommodation')


class OperatorDashboardViewTest(TestCase):
    def setUp(self):
        self.operator = Operator.objects.create(name="op1", password="12345")
        self.accom = Accommodation.objects.create(
            name="Test Hotel",
            address="123 Street",
            postcode="G1"
        )
        self.accom.operators.add(self.operator)

    def login_operator(self, operator):
        session = self.client.session
        session['operator_id'] = operator.id
        session['operator_name'] = operator.name
        session.save()

    def test_dashboard_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('operator_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('operator_login'))

    def test_dashboard_redirects_if_operator_does_not_manage_accommodation(self):
        other_accom = Accommodation.objects.create(
            name="Unrelated Hotel",
            address="456 Avenue",
            postcode="G5"
        )
        self.login_operator(self.operator)
        response = self.client.get(reverse('operator_dashboard') + f'?accommodation_id={other_accom.id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('management'))

    def test_dashboard_renders_if_operator_manages_accommodation(self):
        self.login_operator(self.operator)
        response = self.client.get(reverse('operator_dashboard') + f'?accommodation_id={self.accom.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-dashboard.html')

    def test_dashboard_renders_first_accommodation_if_none_provided(self):
        self.login_operator(self.operator)
        response = self.client.get(reverse('operator_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/operator-dashboard.html')

    def test_dashboard_redirects_if_operator_has_no_accommodation(self):
        new_operator = Operator.objects.create(name="no_accom_op", password="pass123")
        self.login_operator(new_operator)
        response = self.client.get(reverse('operator_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('management'))


# My Listings test

class AddAccommodationView(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_accommodation'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('operator_login'))

    def test_logged_in_operator_can_access_add_accommodation_page(self):
        operator = Operator.objects.create(name="Testoperater", password="pass123")
        session = self.client.session
        session['operator_id'] = operator.id
        session['operator_name'] = operator.name
        session.save()

        response = self.client.get(reverse('add_accommodation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'romaccom/addnewaccommodation.html')
        self.assertEqual(response.context['operator'], operator)

    def test_invalid_operator_id_clears_session_and_redirects(self):
        session = self.client.session
        session['operator_id'] = 9999  # not exist
        session['operator_name'] = "Bob"
        session.save()

        response = self.client.get(reverse('add_accommodation'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('operator_login'))

        # check clear invalid session data
        session = self.client.session
        self.assertIsNone(session.get('operator_id'))
        self.assertIsNone(session.get('operator_name'))

class CreateAccommodationViewTest(TestCase):
    def setUp(self):
        self.url = reverse('create_accommodation')
        self.operator = Operator.objects.create(name="op1", password="12345")
        self.valid_data = {
            'name': "My Accom",
            'address': "123 Test Street",
            'postcode': "G1",
            'map_link': "https://maps.example.com",
            'description': "A nice place"
        }

    def login_operator(self):
        session = self.client.session
        session['operator_id'] = self.operator.id
        session['operator_name'] = self.operator.name
        session.save()

    def test_rejects_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request method", response.json()['error'])

    def test_requires_authentication(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Authentication required", response.json()['error'])

    def test_missing_fields_return_error(self):
        self.login_operator()
        incomplete_data = self.valid_data.copy()
        incomplete_data.pop('name')
        response = self.client.post(self.url, incomplete_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json()['error'])

    def test_valid_submission_creates_accommodation(self):
        self.login_operator()
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertIn('redirect_url', response.json())
        self.assertTrue(Accommodation.objects.filter(name="My Accom").exists())

    def test_operator_does_not_exist(self):
        session = self.client.session
        session['operator_id'] = 2345  #invalid ID
        session['operator_name'] = "Jack"
        session.save()

        data = self.valid_data.copy()
        data['postcode'] = "G1"
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Operator not found", response.json()['error'])

    def test_invalid_postcode_raises_validation_error(self):
        self.login_operator()
        data = self.valid_data.copy()
        data['postcode'] = "INVALID"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not a valid Glasgow postcode", response.json()['error'])

#manage_accom_info_view

class UpdatePrivacyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.url = reverse('update-privacy')

    def test_only_post_allowed(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.json()['error'])

    def test_updates_privacy_to_private(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            self.url,
            data=json.dumps({'private': True}),
            content_type='application/json'
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertFalse(self.user.profile_visibility)  # private → profile_visibility=False

    def test_updates_privacy_to_public(self):
        self.user.profile_visibility = False
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            self.url,
            data=json.dumps({'private': False}),
            content_type='application/json'
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.profile_visibility)

    def test_invalid_json_returns_400(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, data="not_json", content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON data", response.json()['error'])

    def test_unauthenticated_user_still_redirected(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'private': True}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 302)


class UploadAccommodationImagesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Operator
        self.operator = Operator.objects.create(name='Test Operator', email='test@op.com', password='pass123')
        # OperatorProfile
        OperatorProfile.objects.create(operator=self.operator)

        # Accommodation，without operator
        self.accommodation = Accommodation.objects.create(
            name="Test Accom",
            address="123 Street",
            postcode="G1"
        )
        # relate operator
        self.accommodation.operators.add(self.operator)

        self.url = reverse('upload_accommodation_images')

    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn("Invalid request method", response.json()['error'])

    def test_upload_images_successfully(self):
        self.client.force_login(self.user)

        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(
            self.url,
            {'accommodation_id': self.accommodation.id, 'images': [image]},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(AccommodationImage.objects.count(), 1)

    def test_upload_to_invalid_accommodation(self):
        self.client.force_login(self.user)

        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(
            self.url,
            {'accommodation_id': 1234, 'images': [image]},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn("error", response.json())




class UpdateAccommodationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.operator = Operator.objects.create(name='op',email='op@example.com', password='pass')
        self.accom = Accommodation.objects.create(
            name="Old Name",
            address="12 Queen Street",
            postcode="G1",
            description="Old description",
            map_link="http://map.link"
        )
        self.accom.operators.add(self.operator)
        self.url = reverse('update_accommodation')

    def login_as_operator(self):
        session = self.client.session
        session['operator_id'] = self.operator.id
        session.save()

    def test_successful_update(self):
        self.login_as_operator()
        response = self.client.post(self.url, {
            'accommodation_id': self.accom.id,
            'name': 'New Name',
            'address': '34 King Street',
            'postcode': 'G2',
            'description': 'Updated',
            'map_link': 'http://new.map'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.accom.refresh_from_db()
        self.assertEqual(self.accom.name, 'New Name')
        self.assertEqual(self.accom.postcode, 'G2')

    def test_missing_fields(self):
        self.login_as_operator()
        response = self.client.post(self.url, {
            'accommodation_id': self.accom.id,
            'name': '',
            'address': '',
            'postcode': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json()['error'])

    def test_invalid_postcode(self):
        self.login_as_operator()
        response = self.client.post(self.url, {
            'accommodation_id': self.accom.id,
            'name': 'New Name',
            'address': '34 King Street',
            'postcode': 'INVALID'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('not a valid Glasgow postcode', response.json()['error'])

    def test_not_owner(self):
        other_operator = Operator.objects.create(name='op2', password='pass')
        session = self.client.session
        session['operator_id'] = other_operator.id
        session.save()
        response = self.client.post(self.url, {
            'accommodation_id': self.accom.id,
            'name': 'New Name',
            'address': '34 King Street',
            'postcode': 'G1',
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn('Not authorized', response.json()['error'])

    def test_not_authenticated(self):
        response = self.client.post(self.url, {
            'accommodation_id': self.accom.id,
            'name': 'New Name',
            'address': '34 King Street',
            'postcode': 'G1',
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn('Authentication required', response.json()['error'])



class DeleteAccommodationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.operator = Operator.objects.create(name='Test Operator', email='op@example.com', password='pass')
        self.accom = Accommodation.objects.create(
            name="To Be Deleted",
            address="1 Main St",
            postcode="G1",
            description="nice",
            map_link="http://map.link"
        )
        self.accom.operators.add(self.operator)
        self.url = reverse('delete_accommodation')

    def login_operator(self):
        session = self.client.session
        session['operator_id'] = self.operator.id
        session.save()

    def test_successful_deletion(self):
        self.login_operator()
        response = self.client.post(
            self.url,
            data=json.dumps({'accommodation_id': self.accom.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'redirect_url': reverse('management')})
        self.assertFalse(Accommodation.objects.filter(id=self.accom.id).exists())

    def test_unauthenticated_access(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'accommodation_id': self.accom.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn('Authentication required', response.json()['error'])

    def test_operator_does_not_exist(self):
        session = self.client.session
        session['operator_id'] = 1234  # invalid operator ID
        session.save()
        response = self.client.post(
            self.url,
            data=json.dumps({'accommodation_id': self.accom.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('Operator not found', response.json()['error'])

    def test_accommodation_does_not_exist(self):
        self.login_operator()
        response = self.client.post(
            self.url,
            data=json.dumps({'accommodation_id': 1234}),  # invalid accom ID
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('Accommodation not found', response.json()['error'])

    def test_operator_not_authorized(self):
        other_operator = Operator.objects.create(name='Other', email='x@x.com', password='pass')
        session = self.client.session
        session['operator_id'] = other_operator.id
        session.save()
        response = self.client.post(
            self.url,
            data=json.dumps({'accommodation_id': self.accom.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn('Not authorized', response.json()['error'])



class DeleteAccommodationImageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.accom = Accommodation.objects.create(
            name="Test Accom",
            address="1 Street",
            postcode="G1",
            description="Good!",
            map_link="http://map"
        )
        self.review = Review.objects.create(
            user=self.user,
            accommodation=self.accom,
            rating=5,
            title="Great",
            review_text="Nice place!"
        )
        self.image = Image.objects.create(
            review=self.review,
            image='test.jpg'
        )
        self.url = reverse('delete_accommodation_image')

    def test_successful_image_deletion(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'image_id': self.image.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.assertFalse(Image.objects.filter(id=self.image.id).exists())

    def test_image_not_found(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'image_id': 999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['success'], False)

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('Invalid request method', response.json()['error'])

    def test_invalid_json(self):
        response = self.client.post(
            self.url,
            data="not json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('Expecting value', response.json()['error'])

    def test_missing_image_id(self):
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('error', response.json())



class SetMainImageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.accom = Accommodation.objects.create(
            name="Test Accom",
            address="1 Test Street",
            postcode="G1",
            description="Nice place",
            map_link="http://example.com"
        )
        self.image1 = AccommodationImage.objects.create(accommodation=self.accom, image='image1.jpg', is_main=False)
        self.image2 = AccommodationImage.objects.create(accommodation=self.accom, image='image2.jpg', is_main=True)
        self.url = reverse('set_main_image')

    def test_set_main_image_successfully(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            data=json.dumps({'image_id': self.image1.id, 'accommodation_id': self.accom.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.image1.refresh_from_db()
        self.image2.refresh_from_db()
        self.assertTrue(self.image1.is_main)
        self.assertFalse(self.image2.is_main)

    def test_image_does_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            data=json.dumps({'image_id': 1234}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('error', response.json())

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('Invalid request method', response.json()['error'])

    def test_missing_image_id(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            data=json.dumps({}),  # no image_id
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('error', response.json())


class DeleteReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.accom = Accommodation.objects.create(
            name="Test Accom",
            address="1 Street",
            postcode="G1",
            description="Nice",
            map_link="http://map"
        )

        self.review = Review.objects.create(
            user=self.user1,
            accommodation=self.accom,
            title="Review title",
            rating=4,
            review_text="Good stay!"
        )

        self.url = reverse('delete_review')

    def test_successful_review_deletion(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            self.url,
            data=json.dumps({'review_id': self.review.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_user_not_authorized(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            self.url,
            data=json.dumps({'review_id': self.review.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', response.json())
        self.assertIn('not authorized', response.json()['error'])

    def test_review_not_found(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            self.url,
            data=json.dumps({'review_id': 9999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Review not found')

    def test_missing_review_id(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_not_authenticated(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'review_id': self.review.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/accounts/login/', response.url)












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
        cls.accommodation1 = Accommodation.objects.create(name="Accom 1", view_count=100, average_rating=4.5, postcode="G1 1AA")
        cls.accommodation2 = Accommodation.objects.create(name="Accom 2", view_count=200, average_rating=3.0, postcode="G1 2BB")
        cls.accommodation3 = Accommodation.objects.create(name="Accom 3", view_count=50, average_rating=5.0, postcode="G2 3CC")
        cls.accommodation4 = Accommodation.objects.create(name="Accom 4", view_count=250, average_rating=2.0, postcode="G3 4DD")
        cls.accommodation5 = Accommodation.objects.create(name="Accom 5", view_count=150, average_rating=4.8, postcode="G4 5EE")
        cls.accommodation6 = Accommodation.objects.create(name="Accom 6", view_count=300, average_rating=3.5, postcode="G4 5FF")

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

    def test_search_results_view_with_query(self):
        
        response = self.client.get(reverse('search_results'), {'query': 'Accom 1'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accom 1')
        self.assertNotContains(response, 'Accom 2')
        self.assertNotContains(response, 'Accom 3')
        self.assertNotContains(response, 'Accom 4')
        self.assertNotContains(response, 'Accom 5')

    def test_search_results_view_with_postcode(self):
        
        response = self.client.get(reverse('search_results'), {'postcode': 'G1'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accom 1')
        self.assertContains(response, 'Accom 2')
        self.assertNotContains(response, 'Accom 3')
        self.assertNotContains(response, 'Accom 4')
        self.assertNotContains(response, 'Accom 5')

    def test_search_results_view_with_query_and_postcode(self):
        """Ensure the search results filter by both query and postcode."""
        response = self.client.get(reverse('search_results'), {'query': 'Accom', 'postcode': 'G1'})
        
       
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accom 1')
        self.assertContains(response, 'Accom 2')
        self.assertNotContains(response, 'Accom 3')


    def test_search_results_view_no_results(self):
        query = 'Nonexistent'
        postcode = 'ZZZ'
        response = self.client.get(reverse('search_results'), {'query': query, 'postcode': postcode})

        self.assertContains(response, 'No results found for') #couldn't figure out how to include postcode withing testing respons
            
    def test_search_results_view_ajax_returns_correct_HTML(self):
        response = self.client.get(reverse('search_results'), {'query': 'Accom 1'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertIn('Accom 1', response.content.decode('utf-8'))
        self.assertNotIn('Accom 2', response.content.decode('utf-8'))

class TrendingViewTests(TestCase):

    def setUp(self):
        """Create test accommodations with varying view counts."""
        self.accommodation1 = Accommodation.objects.create(name="Accom 1", view_count=100, average_rating=4.5)
        self.accommodation2 = Accommodation.objects.create(name="Accom 2", view_count=200, average_rating=3.8)
        self.accommodation3 = Accommodation.objects.create(name="Accom 3", view_count=50, average_rating=4.0)
        self.accommodation4 = Accommodation.objects.create(name="Accom 4", view_count=250, average_rating=4.7)
        self.accommodation5 = Accommodation.objects.create(name="Accom 5", view_count=150, average_rating=4.2)
        self.accommodation6 = Accommodation.objects.create(name="Accom 6", view_count=300, average_rating=3.9)
        self.accommodation7 = Accommodation.objects.create(name="Accom 7", view_count=350, average_rating=4.3)
        self.accommodation8 = Accommodation.objects.create(name="Accom 8", view_count=400, average_rating=4.1)
        self.accommodation9 = Accommodation.objects.create(name="Accom 9", view_count=500, average_rating=4.6)
        self.accommodation10 = Accommodation.objects.create(name="Accom 10", view_count=600, average_rating=4.9)
        self.accommodation11 = Accommodation.objects.create(name="Accom 11", view_count=450, average_rating=4.4)

    def test_trending_view_top_ten(self):
        response = self.client.get(reverse('trending'))
        trending_accoms = response.context['trending_accommodations']
        self.assertEqual(len(trending_accoms), 10)

        # Check that the accommodations are ordered by view_count
        self.assertEqual(trending_accoms[0], self.accommodation10)
        
        self.assertNotIn(self.accommodation3, trending_accoms)

class TopRatedPageViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.accom1 = Accommodation.objects.create(name="Accom 1", average_rating=4.5)
        cls.accom2 = Accommodation.objects.create(name="Accom 2", average_rating=3.8)
        cls.accom3 = Accommodation.objects.create(name="Accom 3", average_rating=5.0)
        cls.accom4 = Accommodation.objects.create(name="Accom 4", average_rating=2.0)
        cls.accom5 = Accommodation.objects.create(name="Accom 5", average_rating=4.8)
        cls.accom6 = Accommodation.objects.create(name="Accom 6", average_rating=3.5)
        cls.accom7 = Accommodation.objects.create(name="Accom 7", average_rating=4.7)
        cls.accom8 = Accommodation.objects.create(name="Accom 8", average_rating=4.1)
        cls.accom9 = Accommodation.objects.create(name="Accom 9", average_rating=5.0)
        cls.accom10 = Accommodation.objects.create(name="Accom 10", average_rating=4.3)
        cls.accom11 = Accommodation.objects.create(name="Accom 11", average_rating=4.0)

    def test_top_rated_view(self):
        """Ensure the page shows the top 10 rated accommodations."""
        response = self.client.get(reverse('top_rated'))
        self.assertEqual(response.status_code, 200)
        top_rated = response.context['top_rated_accommodations']
        
        self.assertEqual(len(top_rated), 10)  # Should only return 10
        self.assertEqual(top_rated[0], self.accom3)  # Highest rating should be first

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        
        self.assertTemplateUsed(response, 'romaccom/contact.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        
        self.assertTemplateUsed(response, 'romaccom/about.html')

class UserRegisterViewTests(TestCase):

    def test_user_registration_success(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration

    def test_user_registration_duplicate(self):
        User.objects.create_user(username='existinguser', password='password123')
        response = self.client.post(reverse('user_register'), {
            'username': 'existinguser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertContains(response, "Username already exists")

class UserLoginLogoutViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirects after login

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")
    
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout
        self.assertNotIn('_auth_user_id', self.client.session)

class UserProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_my_account_page_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('myaccount'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_page(self):
        response = self.client.get(reverse('user_profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        



