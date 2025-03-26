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

def create_operators(n=6):  
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

    # Create the new operator "Unite Students"
    unite_students_operator = Operator.objects.create(
        name="Unite Students",
        password="securepassword"
    )
    logo_filename = get_random_image(OPERATOR_LOGOS_DIR)
    if logo_filename:
        OperatorProfile.objects.create(
            operator=unite_students_operator,
            logo=f"populate_images/operator_logos/{logo_filename}"
        )
    operators.append(unite_students_operator)

    # Create the new operator "Prestige Student Living"
    prestige_operator = Operator.objects.create(
        name="Prestige Student Living",
        password="securepassword"
    )
    logo_filename = get_random_image(OPERATOR_LOGOS_DIR)
    if logo_filename:
        OperatorProfile.objects.create(
            operator=prestige_operator,
            logo=f"populate_images/operator_logos/{logo_filename}"
        )
    operators.append(prestige_operator)

    # Create the new operator "University of Glasgow"
    uofg_operator = Operator.objects.create(
        name="University of Glasgow",
        password="securepassword"
    )
    logo_filename = get_random_image(OPERATOR_LOGOS_DIR)
    if logo_filename:
        OperatorProfile.objects.create(
            operator=uofg_operator,
            logo=f"populate_images/operator_logos/{logo_filename}"
        )
    operators.append(uofg_operator)

    
    # Create other random student accommodation operators
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

    AccommodationImage.objects.create(
        accommodation=aparto_accom,
        image="populate_images/accommodation_images/aparto.jpg",
        is_main=True
    )
    accommodations.append(aparto_accom)

    # Create "Tramworks" accommodation
    tramworks_accom = Accommodation.objects.create(
        name="Tramworks",
        address="123 Tramway Street, Glasgow",
        postcode="G3 8PX",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d71645.23212395531!2d-4.443710802734387!3d55.864167099999996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d6f498b3e9%3A0x1e6381840a4b627a!2sUnite%20Students%20-%20Tramworks!5e0!3m2!1sru!2suk!4v1742938155867!5m2!1sru!2suk",
        average_rating=4.5,
        view_count=random.randint(50, 1000)
    )
    tramworks_accom.operators.add(operators[1])  # Link to Unite Students operator

    AccommodationImage.objects.create(
        accommodation=tramworks_accom,
        image="populate_images/accommodation_images/tramworks.jpg",
        is_main=True
    )
    accommodations.append(tramworks_accom)

     # Create "Kelvin Court" accommodation
    kelvin_court_accom = Accommodation.objects.create(
        name="Kelvin Court",
        address="456 Kelvin Way, Glasgow",
        postcode="G12 8PX",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.7864403431895!2d-4.2961715232743085!3d55.86637158323814!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d7302a6f19%3A0x53d850520d3068da!2sUnite%20Students%20-%20Kelvin%20Court!5e0!3m2!1sru!2suk!4v1742938357575!5m2!1sru!2suk",
        average_rating=4.5,
        view_count=random.randint(50, 1000)
    )
    kelvin_court_accom.operators.add(operators[1])  # Link to Unite Students operator

    AccommodationImage.objects.create(
        accommodation=kelvin_court_accom,
        image="populate_images/accommodation_images/kelvincourt.jpg",
        is_main=True
    )
    accommodations.append(kelvin_court_accom)

     # Create "Merchant City House" accommodation
    merchant_city_house = Accommodation.objects.create(
        name="MERCHANT CITY HOUSE",
        address="59 Miller Street, Glasgow",
        postcode="G1 1EB",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2239.2053630649016!2d-4.254595723274681!3d55.85910328379861!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488846a1d6ab78cb%3A0x6b7e9422db20eb8f!2sUnite%20Students%20-%20Merchant%20City%20House!5e0!3m2!1sru!2suk!4v1742938410887!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    merchant_city_house.operators.add(operators[1])  # Link to Unite Students operator
    
    AccommodationImage.objects.create(
        accommodation=merchant_city_house,
        image="populate_images/accommodation_images/merchant_city_house.jpg",
        is_main=True
    )
    accommodations.append(merchant_city_house)

    # Create "Thurso Street" accommodation
    thurso_street = Accommodation.objects.create(
        name="THURSO STREET",
        address="1-3 Thurso Street, Glasgow",
        postcode="G11 6PE",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.5947105036557!2d-4.2994522232740335!3d55.86969788298155!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845da70163709%3A0x38a8dadb64827e4a!2sUnite%20Students%20-%20Thurso%20Street!5e0!3m2!1sru!2suk!4v1742938444019!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    thurso_street.operators.add(operators[1])  # Link to Unite Students operator

    AccommodationImage.objects.create(
        accommodation=thurso_street,
        image="populate_images/accommodation_images/thurso_street.jpg",
        is_main=True
    )
    accommodations.append(thurso_street)

    # Create "Kyle Park House" accommodation
    kyle_park_house = Accommodation.objects.create(
        name="KYLE PARK HOUSE",
        address="171 Kyle Street, Glasgow",
        postcode="G4 0DS",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.661828045738!2d-4.2479932232741175!3d55.86853348307136!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48884419559b3a1d%3A0x9fe6217d8b919c2!2sUnite%20Students%20-%20Kyle%20Park%20House!5e0!3m2!1sru!2suk!4v1742938473539!5m2!1sru!2suk",
        average_rating=4.5,
        view_count=random.randint(500, 1200)
    )
    kyle_park_house.operators.add(operators[1])  # Link to Unite Students operator

    AccommodationImage.objects.create(
        accommodation=kyle_park_house,
        image="populate_images/accommodation_images/kyle_park_house.jpg",
        is_main=True
    )

    accommodations.append(kyle_park_house)

    # Create "Blackfriars" accommodation
    blackfriars = Accommodation.objects.create(
        name="BLACKFRIARS",
        address="4 Blackfriars Road, Glasgow",
        postcode="G1 1QL",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2239.221898369722!2d-4.24338142327471!3d55.858816383820766!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488846a6f3261d01%3A0xbb2c9e6c99ceda07!2sUnite%20Students%20-%20Blackfriars!5e0!3m2!1sru!2suk!4v1742938501029!5m2!1sru!2suk",
        average_rating=4.1,
        view_count=random.randint(500, 1200)
    )
    blackfriars.operators.add(operators[1])  # Link to Unite Students operator
    AccommodationImage.objects.create(
        accommodation=blackfriars,
        image="populate_images/accommodation_images/blackfriars.jpg",
        is_main=True
    )
    accommodations.append(blackfriars)

    # Create "Foundry Courtyard" accommodation
    foundry_courtyard = Accommodation.objects.create(
        name="Foundry Courtyard",
        address="214 Kennedy Street, Glasgow",
        postcode="G4 0DB",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.7603526631306!2d-4.246181923274214!3d55.86682418320317!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888441c46d51b2f%3A0x9db5f5606ea74de3!2sPrestige%20Student%20Living%20Foundry%20Courtyard!5e0!3m2!1sru!2suk!4v1742938537706!5m2!1sru!2suk",
        average_rating=4.7,
        view_count=random.randint(500, 1200)
    )
    foundry_courtyard.operators.add(operators[2])  # Link to Prestige Student Living operator

    AccommodationImage.objects.create(
        accommodation=foundry_courtyard,
        image="populate_images/accommodation_images/foundry_courtyard.jpg",
        is_main=True
    )
    accommodations.append(foundry_courtyard)

    # Create "Bridle Works" accommodation
    bridle_works = Accommodation.objects.create(
        name="Bridle Works",
        address="350 Cathedral Street, Glasgow",
        postcode="G1 2BQ",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.9623008619856!2d-4.251508423274399!3d55.86332048347348!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48884514c8c347cf%3A0x5ae32161b9e3fec1!2sPrestige%20Student%20Living%20Bridle%20Works!5e0!3m2!1sru!2suk!4v1742938566676!5m2!1sru!2suk",
        average_rating=4.5,
        view_count=random.randint(500, 1200)
    )
    bridle_works.operators.add(operators[2])  # Link to Prestige Student Living operator

    AccommodationImage.objects.create(
        accommodation=bridle_works,
        image="populate_images/accommodation_images/bridle_works.jpg",
        is_main=True
    )
    accommodations.append(bridle_works)

    # Create "Scotway House" accommodation
    scotway_house = Accommodation.objects.create(
        name="Scotway House",
        address="165 Castlebank Street, Glasgow",
        postcode="G11 6EU",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.7064995489823!2d-4.3103980232741685!3d55.86775848313112!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888450fbffcd8c5%3A0x308f4ce9cd8a8ee0!2sPrestige%20Student%20Living%20Scotway%20House!5e0!3m2!1sru!2suk!4v1742938623589!5m2!1sru!2suk",
        average_rating=4.8,
        view_count=random.randint(500, 1200)
    )
    scotway_house.operators.add(operators[2])  # Link to Prestige Student Living operator

    AccommodationImage.objects.create(
        accommodation=scotway_house,
        image="populate_images/accommodation_images/scotway_house.jpg",
        is_main=True
    )

    accommodations.append(scotway_house)

    # Create "Clyde Court" accommodation
    clyde_court = Accommodation.objects.create(
        name="Clyde Court",
        address="Jocelyn Square, Glasgow",
        postcode="G1 5JY",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2239.4857582738164!2d-4.249128623275009!3d55.85423808417384!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488847003f54642d%3A0xb4ac24bddfee71e8!2sClyde%20Court!5e0!3m2!1sru!2suk!4v1742938678365!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    clyde_court.operators.add(operators[2])  # Link to Prestige Student Living operator

    AccommodationImage.objects.create(
        accommodation=clyde_court,
        image="populate_images/accommodation_images/clyde_court.jpg",
        is_main=True
    )

    accommodations.append(clyde_court)

    # Create "Cairncross House" accommodation
    cairncross_house = Accommodation.objects.create(
        name="Cairncross House",
        address="20 Kelvinhaugh Place, Glasgow",
        postcode="G3 8NH",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.854702252877!2d-4.290194323274291!3d55.86518728332935!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d439564e13%3A0xf5378e6457f72312!2sCairncross%20House!5e0!3m2!1sru!2suk!4v1742940562822!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    cairncross_house.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=cairncross_house,
        image="populate_images/accommodation_images/cairncross_house.jpg",
        is_main=True
    )

    accommodations.append(cairncross_house)


# Create "Kelvinhaugh Gate" accommodation
    kelvinhaugh_gate = Accommodation.objects.create(
        name="Kelvinhaugh Gate",
        address="5 Kelvinhaugh Gate, Glasgow",
        postcode="G3 8PE",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.9394475957606!2d-4.2939972232743955!3d55.86371698344283!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d439564e13%3A0x6f4330536b82b0b3!2sKelvinhaugh%20Gate!5e0!3m2!1sru!2suk!4v1742940784675!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    kelvinhaugh_gate.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=kelvinhaugh_gate,
        image="populate_images/accommodation_images/kelvinhaugh_gate.jpg",
        is_main=True
    )

    accommodations.append(kelvinhaugh_gate)


    # Create "Kelvinhaugh Street" accommodation
    kelvinhaugh_street = Accommodation.objects.create(
        name="Kelvinhaugh Street",
        address="27 - 91 Kelvinhaugh Street, Glasgow",
        postcode="G3 8PE",
        map_link="hhttps://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.939103678619!2d-4.293997223398767!3d55.863722950327826!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d6f35048bf%3A0xf88d66c3cb54c075!2sKelvinhaugh%20Street!5e0!3m2!1sru!2suk!4v1742941053803!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    kelvinhaugh_street.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=kelvinhaugh_street,
        image="populate_images/accommodation_images/kelvinhaugh_street.jpg",
        is_main=True
    )

    accommodations.append(kelvinhaugh_street)

    # Create "Maclay Residences" accommodation
    maclay_residences = Accommodation.objects.create(
        name="Maclay Residences",
        address="9 Cooperage Place, Glasgow",
        postcode="G3 8QP",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.8968589656206!2d-4.300133923274342!3d55.86445588338582!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d9cf8a88ef%3A0xf0ad52bf3c521f40!2sMaclay%20Residences!5e0!3m2!1sru!2suk!4v1742942247639!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    maclay_residences.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=maclay_residences,
        image="populate_images/accommodation_images/maclay_residences.jpg",
        is_main=True
    )

    accommodations.append(maclay_residences)


    # Create "Brooke House" accommodation
    brooke_house = Accommodation.objects.create(
        name="Brooke House",
        address="31 Brooke Street, Glasgow",
        postcode="DG1 2JL",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1731.3914446382976!2d-3.6070967941261873!3d55.06801276979857!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4862ca6c037f4d63%3A0xf083bb1290b6dea1!2s31%20Brooke%20St%2C%20Dumfries%20DG1%202JL!5e0!3m2!1sru!2suk!4v1742942747377!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    brooke_house.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=brooke_house,
        image="populate_images/accommodation_images/brooke_house.jpg",
        is_main=True
    )

    accommodations.append(brooke_house)


    # Create "Winton Drive" accommodation
    winton_drive = Accommodation.objects.create(
        name="Winton Drive",
        address="9 Cooperage Place, Glasgow",
        postcode="G3 8QP",
        map_link="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1118.8570779233992!2d-4.302202410981977!3d55.88497284761754!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845b7a30b00ab%3A0x6de4cbbbc3460722!2sWinton%20Drive!5e0!3m2!1sru!2suk!4v1742942980473!5m2!1sru!2suk",
        average_rating=5.0,
        view_count=random.randint(500, 1200)
    )
    maclay_residences.operators.add(operators[3])  # Link to University of Glasgow operator

    AccommodationImage.objects.create(
        accommodation=winton_drive,
        image="populate_images/accommodation_images/winton_drive.jpg",
        is_main=True
    )

    accommodations.append(winton_drive)



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
            average_rating=random.uniform(2.5, 4.0),  
            view_count=random.randint(50, 1000) # Some should be highly viewed
)

        
        # When creating random accommodations, exclude the real operators
        excluded_operators = {operators[0], operators[1], operators[2], operators[3]}  # Exclude aparto, Unite Students, and Prestige Student Living
        other_operators = [op for op in operators if op not in excluded_operators]

        accommodation.operators.set(random.sample(other_operators, random.randint(1, len(other_operators))))
        accommodations.append(accommodation)


        # Add images
        for _ in range(random.randint(1, 3)):  # Assign 1-3 images per accommodation
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
