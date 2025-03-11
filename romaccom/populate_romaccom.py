import os
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "romaccom.settings")
django.setup()

from web_app.models import User, Operator, Accommodation, Review

fake = Faker()

def create_users(n=20):
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        user = User.objects.create_user(username=username, email=email, password=password)
        users.append(user)
    return users

def create_operators(n=5):
    operators = []
    
    # Create a well-known operator
    aparto_operator = Operator.objects.create(
        name="aparto Student",
        email="glasgow@apartostudent.com",
        password="securepassword"
    )
    operators.append(aparto_operator)
    
    # Create other random student accommodation operators
    for _ in range(n):
        name = fake.company() + " Accommodation"
        email = fake.email()
        password = "securepassword"
        operator = Operator.objects.create(name=name, email=email, password=password)
        operators.append(operator)
    return operators

def create_accommodations(operators, n=30):
    accommodations = []

    # Featured real accommodation
    aparto_accom = Accommodation.objects.create(
        name="aparto Glasgow West End",
        address="Kelvinhaugh Street, Glasgow",
        postcode="G3 8PX",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2237.6997033286593!2d-4.301292!3d55.867908!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888441d32566293%3A0x10a2a350cac75e4a!2saparto%20Glasgow%20West%20End!5e0!3m2!1sen!2suk!4v1646147020959!5m2!1sen!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    aparto_accom.operators.add(operators[0])  # Assign to aparto operator
    accommodations.append(aparto_accom)

    # Create more accommodations
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
            view_count=random.randint(50, 1000)  # Some should be highly viewed
        )
        accommodation.operators.set(random.sample(operators, random.randint(1, len(operators))))
        accommodations.append(accommodation)

    return accommodations

def create_reviews(users, accommodations, n=50):
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
        Review.objects.create(
            user=user,
            accommodation=aparto_accom,
            rating=5,
            title="Fantastic Experience",
            review_text=premium_reviews[i]
        )

    # Create a mix of good and bad reviews for other accommodations
    for _ in range(n):
        user = random.choice(users)
        accommodation = random.choice(accommodations)
        rating = random.randint(1, 5)
        
        review_text = (
            fake.sentence() if rating >= 4 
            else "Would not recommend this place, bad management." if rating <= 2
            else fake.paragraph()
        )

        Review.objects.create(
            user=user,
            accommodation=accommodation,
            rating=rating,
            title=fake.sentence(nb_words=4),
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
