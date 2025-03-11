from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Accommodation
# from django.contrib.auth.models import User
from .models import User

# Home Page
def home_view(request):
    trending_accommodations = Accommodation.objects.order_by('-view_count')[:5]
    top_rated_accommodations = Accommodation.objects.order_by('-average_rating')[:5]
    return render(request, 'romaccom/home.html', {
        'trending_accommodations': trending_accommodations,
        'top_rated_accommodations': top_rated_accommodations
    })

#Search results view
def search_results_view(request):
    query = request.GET.get('query', '')
    results = Accommodation.objects.filter(name__icontains=query)
    return render(request, 'romaccom/search_results.html', {'results': results, 'query': query})

# Trending Accommodations
def trending_view(request):
    trending_accommodations = Accommodation.objects.order_by('-view_count')[:10]
    return render(request, 'romaccom/trending.html', {'trending_accommodations': trending_accommodations})

# Top Rated Accommodations
def top_rated_view(request):
    top_rated_accommodations = Accommodation.objects.order_by('-average_rating')[:10]
    return render(request, 'romaccom/toprated.html', {'top_rated_accommodations': top_rated_accommodations})

# Contact Page
def contact_view(request):
    return render(request, 'romaccom/contact.html')

# About Page
def about_view(request):
    return render(request, 'romaccom/about.html')

# User Registration
def user_register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'romaccom/register.html')

# Operator Registration
def operator_register_view(request):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        password = request.POST.get('password')
        operator = User.objects.create_user(username=property_name, password=password)
        return redirect('operator_dashboard')
    return render(request, 'romaccom/register.html')

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'romaccom/login.html', {'error': 'Invalid username or password'})
    return render(request, 'romaccom/login.html')

# User Account
def my_account_view(request):
    return render(request, 'romaccom/myaccount.html')

# User Reviews
def my_reviews_view(request):
    return render(request, 'romaccom/myreviews.html')

# Privacy Settings
def privacy_settings_view(request):
    return render(request, 'romaccom/privacy-settings.html')

# Accommodation Search
def search_view(request):
    query = request.GET.get('query', '')
    results = Accommodation.objects.filter(name__icontains=query)
    return render(request, 'romaccom/search.html', {'results': results})

# Accommodation List
def accom_list_view(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'romaccom/accomlist.html', {'accommodations': accommodations})

# Accommodation Details Page
def accom_page_view(request, accom_id):
    accommodation = Accommodation.objects.get(id=accom_id)
    return render(request, 'romaccom/accomdetail.html', {'accommodation': accommodation})

# Accommodation Reviews
def accom_reviews_view(request, accom_id):
    accommodation = Accommodation.objects.get(id=accom_id)
    return render(request, 'romaccom/reviews.html', {'accommodation': accommodation})

# Accommodation Map
def accom_map_view(request, accom_id):
    accommodation = Accommodation.objects.get(id=accom_id)
    return render(request, 'romaccom/map.html', {'accommodation': accommodation})

# Write a Review
def write_review_view(request, accom_id):
    accommodation = Accommodation.objects.get(id=accom_id)
    
    # Handle form submission if it's a POST request
    if request.method == 'POST':
        # Process form data
        # Create a new review
        # Redirect to accommodation detail page
        pass
        
    return render(request, 'romaccom/write-review.html', {'accommodation': accommodation})

# Operator Login
def operator_login_view(request):
    return render(request, 'romaccom/operator-login.html')

# Operator Dashboard
def operator_dashboard_view(request):
    return render(request, 'romaccom/operator-dashboard.html')

# My Listings
def my_listings_view(request):
    return render(request, 'romaccom/mylistings.html')

# Add New Accommodation
def add_accommodation_view(request):
    return render(request, 'romaccom/addnewaccommodation.html')

# Manage Accommodation Info
def manage_accom_info_view(request):
    return render(request, 'romaccom/manageaccommodationinfo.html')
