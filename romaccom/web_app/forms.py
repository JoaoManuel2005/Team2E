from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Review, Image, OperatorProfile

User = get_user_model()

"""
Form for user registtration
"""
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

"""
Form to update user profile details
allows updating website and profile pocture
"""
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website', 'picture']

"""
Form for submitting reciews
Allows submitting title, rating, a review description
Supports multiple image uploads
"""
class ReviewForm(forms.ModelForm):
    images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Review
        fields = ['title', 'rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }

"""
Form for updating operator profile details
Allows updating operator description, webiste and logo
"""
class OperatorProfileForm(forms.ModelForm):
    class Meta:
        model = OperatorProfile
        fields = ['description', 'website', 'logo']