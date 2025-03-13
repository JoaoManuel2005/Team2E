from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Custom User Model
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='public')
    profile_visibility = models.BooleanField(default=True)

    def __str__(self):
        return self.username

# User Profile Model (One-to-One with User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Operator Model
class Operator(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # Make email optional
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Accommodation Model
class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    map_link = models.URLField(max_length=500, blank=True)
    operators = models.ManyToManyField(Operator, related_name='accommodations')
    average_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    view_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def update_average_rating(self):
        reviews = self.reviews.all()
        self.average_rating = sum(r.rating for r in reviews) / reviews.count() if reviews.count() > 0 else 0
        self.save()

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    def __str__(self):
        return self.name

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255, blank=True, help_text="Optional review title")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Use auto_now_add=True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.accommodation.update_average_rating()

    def __str__(self):
        return f"Review by {self.user.username} on {self.accommodation.name}"

# Image Model for reviews
class Image(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/', default='default.jpg')

    def __str__(self):
        return f"Image for Review {self.review.id}"

# Add a new Image model for accommodations
class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accommodation_images/', default='default.jpg')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.accommodation.name}"
