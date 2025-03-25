import os
import django
import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "romaccom.settings")
django.setup()

from web_app.models import User, Operator, Accommodation, Review, AccommodationImage, Image, OperatorProfile


fake = Faker()

BASE_MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "populate_images")
OPERATOR_LOGOS_DIR = os.path.join(BASE_MEDIA_DIR, "operator_logos")
ACCOMMODATION_IMAGES_DIR = os.path.join(BASE_MEDIA_DIR, "accommodation_images")
REVIEW_IMAGES_DIR = os.path.join(BASE_MEDIA_DIR, "review_images")

"""
Returns a random image file path from a given directory
"""
def get_random_image(directory):
    if not os.path.exists(directory) or not os.listdir(directory):
        return None  
    return random.choice(os.listdir(directory))

"""
Creates 20 users
All of their passwords are set to password123 so that we can enter their accounts while testing
"""
def create_users(n=20):
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        user = User.objects.create_user(username=username, email=email, password=password)
        users.append(user)
    return users

"""
Creates 6 operators
All of their passwords are set to securepassword so that we can enter their accounts while testing
"""
def create_operators(n=5):
    operators = []
    
    aparto_operator = Operator.objects.create(
        name="aparto Student",
        password="securepassword"
    )
    logo_filename = get_random_image(OPERATOR_LOGOS_DIR)
    if logo_filename:
        aparto_profile = OperatorProfile.objects.create(
            operator=aparto_operator,
            logo=f"populate_images/operator_logos/{logo_filename}"  
        )

    operators.append(aparto_operator)
    
    for _ in range(n):
        name = fake.company() + " Accommodation"
        password = "securepassword"
        operator = Operator.objects.create(
            name=name,
            password=password
        )
        logo_filename = get_random_image(OPERATOR_LOGOS_DIR)
        if logo_filename:
            OperatorProfile.objects.create(
                operator=operator,
                logo=f"populate_images/operator_logos/{logo_filename}"
            )

        operators.append(operator)
    
    return operators

"""
Creates 30 accoms
Randomly assigns them to one of the operators other than apartos operator
"""
def create_accommodations(operators, n=30):
    accommodations = []

    # Featured real accommodation (aparto)
    aparto_accom = Accommodation.objects.create(
        name="aparto Glasgow West End",
        address="Kelvinhaugh Street, Glasgow",
        postcode="G3 8PX",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.9210848058406!2d-4.295280023052101!3d55.86403557312559!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d7081005ad%3A0x817dbb0b34ec784d!2saparto%20Glasgow%20West%20End!5e0!3m2!1sen!2suk!4v1742061791797!5m2!1sen!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    aparto_accom.operators.add(operators[0])  # Assign to aparto operator
    accommodations.append(aparto_accom)

    for _ in range(n):
        name = fake.company() + " Student Living"
        address = fake.street_address() + ", Glasgow"
        postcode = random.choice(["G1", "G2", "G3", "G4", "G5", "G11", "G12", "G13", "G14", "G20", "G21", "G31", "G32", "G40", "G41", "G51"])
        map_link = fake.url()
        
        accommodation = Accommodation.objects.create(
            name=name,
            address=address,
            postcode=postcode,
            map_link=map_link,
            average_rating=random.uniform(2.5, 5.0),
            view_count=random.randint(50, 1000)
        )
        # when creating random accommodations, exclude the aparto operator
        other_operators = [op for op in operators if op != operators[0]]
        accommodation.operators.set(random.sample(other_operators, random.randint(1, len(other_operators))))
        accommodations.append(accommodation)

        for _ in range(random.randint(1, 3)):  # assign 1-3 images per accommodation
            image_filename = get_random_image(ACCOMMODATION_IMAGES_DIR)
            if image_filename:
                AccommodationImage.objects.create(
                    accommodation=accommodation,
                    image=f"populate_images/accommodation_images/{image_filename}",
                    is_main=False
                )

    return accommodations

"""
Creates 50 reviews
Randomly assigns them to accomodations
Aparto gets its own special reviews
"""
def create_reviews(users, accommodations, n=50):
    def random_date():
        now = timezone.now()
        days_ago = random.randint(1, 365)
        return now - timedelta(days=days_ago)

    # 5 Star Reviews for aparto
    aparto_accom = accommodations[0]
    
    premium_reviews = [
        "Absolutely loved my stay here! Great staff and facilities.",
        "The rooms are spacious and well maintained.",
        "Would highly recommend this place to any student in Glasgow.",
        "Amazing location and easy access to everything.",
        "Best student accommodation in Glasgow hands down."
    ]
    
    for i in range(5):
        user = random.choice(users)
        review = Review.objects.create(
            user=user,
            accommodation=aparto_accom,
            rating=5,
            title="Fantastic Experience",
            review_text=premium_reviews[i]
        )
        image_filename = get_random_image(REVIEW_IMAGES_DIR)
        if image_filename:
            Image.objects.create(
                review=review,
                image=f"populate_images/review_images/{image_filename}"
            )

    # create a mix of good and bad reviews for accommodations
    for _ in range(n):
        user = random.choice(users)
        accommodation = random.choice(accommodations)
        rating = random.randint(1, 5)
        
        review_text = (
            fake.sentence() if rating >= 4 
            else "Would not recommend this place, bad management." if rating <= 2
            else fake.paragraph()
        )

        review = Review.objects.create(
            user=user,
            accommodation=accommodation,
            rating=rating,
            title=fake.sentence(nb_words=4),
            review_text=review_text,
            created_at=random_date() 
        )

        # assign an image
        image_filename = get_random_image(REVIEW_IMAGES_DIR)
        if image_filename:
            Image.objects.create(
                review=review,
                image=f"populate_images/review_images/{image_filename}"
            )

def populate():
    print("Creating users...")
    users = create_users()
    print("Creating operators...")
    operators = create_operators()
    print("Creating accommodations...")
    accommodations = create_accommodations(operators)
    print("Creating reviews...")
    create_reviews(users, accommodations)
    print("Database population complete!")

if __name__ == "__main__":
    populate()
