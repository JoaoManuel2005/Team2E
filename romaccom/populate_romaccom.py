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
    for _ in range(n):
        name = fake.company()
        email = fake.email()
        password = "securepassword"
        operator = Operator.objects.create(name=name, email=email, password=password)
        operators.append(operator)
    return operators

def create_accommodations(operators, n=10):
    accommodations = []
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
    for _ in range(n):
        user = random.choice(users)
        accommodation = random.choice(accommodations)
        rating = random.randint(1, 5)
        review_text = fake.paragraph()
        Review.objects.create(user=user, accommodation=accommodation, rating=rating, review_text=review_text)

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