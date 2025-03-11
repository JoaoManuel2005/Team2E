import os
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Team2E.settings")
django.setup()

from romaccom.models import User, Operator, Accommodation, Review

fake = Faker()

def create_users(n=5):
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        user = User.objects.create_user(username=username, email=email, password=password)
        users.append(user)
    return users

def create_operators(n=3):
    operators = []
    # Create real operator
    aparto_operator = Operator.objects.create(
        name="aparto Student",
        email="glasgow@apartostudent.com",
        password="securepassword"
    )
    operators.append(aparto_operator)
    
    # Create random operators
    for _ in range(n):
        name = fake.company()
        email = fake.email()
        password = "securepassword"
        operator = Operator.objects.create(name=name, email=email, password=password)
        operators.append(operator)
    return operators

def create_accommodations(operators, n=10):
    accommodations = []
    
    # Create real accommodation
    aparto_accom = Accommodation.objects.create(
        name="aparto Glasgow West End",
        address="Kelvinhaugh Street, Glasgow",
        postcode="G3 8PX",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2237.6997033286593!2d-4.301292!3d55.867908!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888441d32566293%3A0x10a2a350cac75e4a!2saparto%20Glasgow%20West%20End!5e0!3m2!1sen!2suk!4v1646147020959!5m2!1sen!2suk",
        average_rating=5.0,
        view_count=random.randint(200, 700)
    )
    
    # Assign the aparto operator to the real accommodation
    # Assuming the first operator in the list is the aparto operator we created
    aparto_accom.operators.add(operators[0])
    accommodations.append(aparto_accom)
    
    # Create random accommodations
    for _ in range(n):
        name = fake.company() + " Hotel"
        address = fake.address()
        postcode = fake.postcode()
        map_link = fake.url()
        accommodation = Accommodation.objects.create(
            name=name,
            address=address,
            postcode=postcode,
            map_link=map_link,
            average_rating=random.uniform(1.0, 5.0),
            view_count=random.randint(0, 500)
        )
        accommodation.operators.set(random.sample(operators, random.randint(1, len(operators))))
        accommodations.append(accommodation)
    return accommodations

def create_reviews(users, accommodations, n=20):
    # First create some good reviews for aparto Glasgow West End specifically
    aparto_accom = accommodations[0]  # The first accommodation should be our aparto one
    
    review_texts = [
        "The ultimate place to be yourself! Their gold room type provided everything I needed.",
        "I loved the platinum room. The amenities were top-notch and the community is great.",
        "The diamond room was worth every penny! Best student accommodation in Glasgow.",
        "Really nice facilities and the staff are super helpful. Would recommend to anyone!",
        "Love the location - so convenient for getting to classes and the city center."
    ]
    
    # Create 5 five-star reviews for aparto
    for i in range(5):
        user = random.choice(users)
        review_text = review_texts[i] if i < len(review_texts) else fake.paragraph()
        Review.objects.create(
            user=user, 
            accommodation=aparto_accom, 
            rating=5, 
            title="Excellent accommodation",
            review_text=review_text
        )
    
    # Create random reviews for all accommodations
    for _ in range(n):
        user = random.choice(users)
        accommodation = random.choice(accommodations)
        rating = random.randint(1, 5)
        review_text = fake.paragraph()
        Review.objects.create(
            user=user, 
            accommodation=accommodation, 
            rating=rating, 
            review_text=review_text
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
