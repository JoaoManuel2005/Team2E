from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile, Review

User = get_user_model()

# User Registration Form
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website', 'picture']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }