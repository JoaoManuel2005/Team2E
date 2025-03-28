from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout 
from .models import Accommodation, Review, Image, Operator, UserProfile, AccommodationImage
from .forms import ReviewForm, OperatorProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import User, Operator, OperatorProfile, validate_glasgow_postcode, validate_uk_address
from django.urls import reverse
import json
import logging
from django.core.exceptions import ValidationError
from django.db import transaction
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

# list of all valid Glasgow postcodes
GLASGOW_POSTCODES = ["G1", "G2", "G3", "G4", "G5", "G11", "G12", "G13", "G14", "G15", "G20", "G21", "G22", "G23", "G31", "G32", "G33", "G34", "G40", "G41", "G42", "G43", "G44", "G45", "G46", "G51", "G52", "G53", "G61", "G62", "G64", "G65", "G66", "G67", "G68", "G69", "G70"]

"""
Index page 
shows 5 most viewed accoms and 5 best rated accoms
"""
def index(request):
    trending_accommodations = Accommodation.objects.order_by('-view_count')[:5]
    top_rated_accommodations = Accommodation.objects.order_by('-average_rating')[:5]
    return render(request, 'romaccom/home.html', {
        'trending_accommodations': trending_accommodations,
        'top_rated_accommodations': top_rated_accommodations
    })

"""
Home page 
shows 5 most viewed accoms and 5 best rated accoms
"""
def home_view(request):
    trending_accommodations = Accommodation.objects.order_by('-view_count')[:5]
    top_rated_accommodations = Accommodation.objects.order_by('-average_rating')[:5]
    
    operator_id = request.session.get('operator_id')
    operator_name = request.session.get('operator_name')
    operator_logged_in = bool(operator_id and operator_name)
        
    return render(request, 'romaccom/home.html', {
        'trending_accommodations': trending_accommodations,
        'top_rated_accommodations': top_rated_accommodations,
        'operator_logged_in': operator_logged_in,
        'operator_name': operator_name,
        'glasgow_postcodes': GLASGOW_POSTCODES 
    })

def search_results_view(request):
    query = request.GET.get('query', '').strip()
    postcode_prefix = request.GET.get('postcode', '').strip()

    results = Accommodation.objects.all()

    if postcode_prefix in GLASGOW_POSTCODES:
        results = results.filter(postcode__startswith=postcode_prefix)

    if query:
        results = results.filter(name__icontains=query)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        html = render(request, 'romaccom/search_results_partial.html', {'results': results}).content.decode('utf-8')
        return JsonResponse({'html': html})

    return render(request, 'romaccom/search_results.html', {
        'results': results,
        'query': query,
        'postcode_prefix': postcode_prefix,
        'glasgow_postcodes': GLASGOW_POSTCODES,
    })

"""
Trending page 
shows 10 most viewed accoms
"""
def trending_view(request):
    trending_accommodations = Accommodation.objects.order_by('-view_count')[:10]
    return render(request, 'romaccom/trending.html', {'trending_accommodations': trending_accommodations})

"""
Top rated page 
shows 10 best rated accoms
"""
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
            return render(request, 'romaccom/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'romaccom/register.html')

# Operator Registration
def operator_register_view(request):
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        password = request.POST.get('password')
        accommodation_id = request.POST.get('accommodation_id')
        
        operator = Operator.objects.create(
            name=property_name,
            password=password 
        )
        
        # Associate with accommodation if ID provided
        if accommodation_id:
            try:
                accommodation = Accommodation.objects.get(id=accommodation_id)
                accommodation.operators.add(operator)
            except Accommodation.DoesNotExist:
                return render(request, 'romaccom/register.html', {
                    'error': 'Accommodation not found'
                })
                
        # Store operator info in session
        request.session['operator_id'] = operator.id
        request.session['operator_name'] = operator.name
        
        return redirect('operator_dashboard')
        
    return render(request, 'romaccom/register.html')

# User Login
def login_view(request):
    # check if operator is logged in, if so, they have to log out of operator
    if 'operator_id' in request.session:
        return render(request, 'romaccom/login.html', {'error': 'Please log out as operator first'})
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('myaccount')
        else:
            return render(request, 'romaccom/login.html', {'error': 'Invalid username or password'})
    return render(request, 'romaccom/login.html')

# User Logout
def logout_view(request):
    logout(request)
    
    if 'operator_id' in request.session:
        request.session.pop('operator_id', None)
    if 'operator_name' in request.session:
        request.session.pop('operator_name', None)
    
    return redirect('home')

# User Account
def my_account_view(request):
    return render(request, 'romaccom/myaccount.html')

# ANy User Account
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'romaccom/account.html', {'profile_user': profile_user})

"""
My reviews page 
shows all reviews by a user
"""
@login_required
def my_reviews_view(request):
    user_reviews = Review.objects.filter(user=request.user).select_related('accommodation')
    return render(request, 'romaccom/myreviews.html', {'reviews': user_reviews})

# Accommodation Search
def search_view(request):
    query = request.GET.get('query', '')
    results = Accommodation.objects.filter(name__icontains=query)
    return render(request, 'romaccom/search.html', {'results': results})

# Accommodation List
def accom_list_view(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'romaccom/accomlist.html', {'accommodations': accommodations})

""" 
Accommodation Details Page
Shows accomodatiosn reviews and image
"""
def accom_page_view(request, accom_id):
    accommodation = get_object_or_404(Accommodation, id=accom_id)
    accommodation.increment_view_count() 
    
    # get reviews for this accommodation
    reviews = Review.objects.filter(accommodation=accommodation).order_by('-created_at')
    
    # get main image or fallback to any image
    main_image = accommodation.images.filter(is_main=True).first()    
    if not main_image:
        main_image = accommodation.images.first()
    
    # check if an operator is logged in
    operator_id = request.session.get('operator_id')
    operator_logged_in = False
    operator_manages_accommodation = False
    
    if operator_id:
        try:
            operator = Operator.objects.get(id=operator_id)
            operator_logged_in = True
            # check if this operator manages this specific accommodation
            if operator in accommodation.operators.all():
                operator_manages_accommodation = True
        except Operator.DoesNotExist:
            # invalid operator ID
            pass
    
    return render(request, 'romaccom/accomdetail.html', {
        'accommodation': accommodation,
        'reviews': reviews,
        'main_image': main_image,
        'operator_logged_in': operator_logged_in,
        'operator_manages_accommodation': operator_manages_accommodation
    })

# Accommodation Reviews
def accom_reviews_view(request, accom_id, review_id):
    accommodation = get_object_or_404(Accommodation, id=accom_id)
    review = get_object_or_404(Review, id=review_id, accommodation=accommodation)
    
    return render(request, 'romaccom/reviews.html', {'accommodation': accommodation, 'review': review})

# Accommodation Map
def accom_map_view(request, accom_id):
    accommodation = Accommodation.objects.get(id=accom_id)
    return render(request, 'romaccom/map.html', {'accommodation': accommodation})

"""
Write a Review page
Users can give a review title, rating, text and image
"""
@login_required
def write_review_view(request, accom_id):
    accommodation = get_object_or_404(Accommodation, id=accom_id)
    
    # check if the user already has a review for this accommodation
    existing_review = Review.objects.filter(user=request.user, accommodation=accommodation).first()
    if (existing_review):
        # if a review exists, redirect to the edit page
        return redirect('edit_review', review_id=existing_review.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  
            review.accommodation = accommodation  
            review.save()  

            # Handle image upload - only save the first image
            images = request.FILES.getlist('images')
            if images:
                Image.objects.create(review=review, image=images[0])

            accommodation.update_average_rating() 
            return redirect('accom_page_view', accom_id=accommodation.id)  

    else:
        form = ReviewForm()

    return render(request, 'romaccom/write-review.html', {'accommodation': accommodation, 'form': form})

# Operator Login
def operator_login_view(request):
    # check if user is logged in
    if request.user.is_authenticated:
        return render(request, 'romaccom/operator-login.html', {'error': 'Please log out as user first'})
        
    accom_id = request.GET.get('accommodation_id')
    error = None
    accommodation = None
    
    if accom_id:
        try:
            accommodation = Accommodation.objects.get(id=accom_id)
        except Accommodation.DoesNotExist:
            error = "Accommodation not found"
    
    if request.method == "POST":
        property_name = request.POST.get('property_name')
        password = request.POST.get('password')
        post_accom_id = request.POST.get('accommodation_id')
        
        operator = Operator.objects.filter(name=property_name, password=password).first()
        
        if not operator:
            error = "Invalid property name or password"
        else:
            if post_accom_id:
                # verify operator manages this accommodation
                try:
                    accommodation = Accommodation.objects.get(id=post_accom_id)
                    if operator in accommodation.operators.all():
                        # store operator info in session
                        request.session['operator_id'] = operator.id
                        request.session['operator_name'] = operator.name
                        return redirect('operator_dashboard')
                    else:
                        error = "You are not authorized to manage this accommodation"
                except Accommodation.DoesNotExist:
                    error = "Accommodation not found"
            else:
                # feneral operator login - no specific accommodation
                # Store operator info in session
                request.session['operator_id'] = operator.id
                request.session['operator_name'] = operator.name
                return redirect('management')
    
    return render(request, 'romaccom/operator-login.html', {
        'accommodation': accommodation,
        'error': error,
        'from_homepage': not accom_id  
    })

# Operator Dashboard
def operator_dashboard_view(request):
    operator_id = request.session.get('operator_id')
    if not operator_id:
        return redirect('operator_login')
    
    try:
        operator = Operator.objects.get(id=operator_id)
        
        accom_id = request.GET.get('accommodation_id')
        if accom_id:
            try:
                accommodation = Accommodation.objects.get(id=accom_id)
                if operator in accommodation.operators.all():
                    return render(request, 'romaccom/operator-dashboard.html', {
                        'accommodation': accommodation,
                        'operator': operator
                    })
                else:
                    return redirect('management')
            except Accommodation.DoesNotExist:
                return redirect('management')
        
        accommodation = operator.accommodations.first()
        
        if accommodation:
            return render(request, 'romaccom/operator-dashboard.html', {
                'accommodation': accommodation,
                'operator': operator
            })
        else:
            return redirect('management')
            
    except Operator.DoesNotExist:
        # Clear invalid session data
        request.session.pop('operator_id', None)
        request.session.pop('operator_name', None)
        return redirect('operator_login')

# My Listings
def my_listings_view(request):
    return render(request, 'romaccom/mylistings.html')

# Add New Accommodation
def add_accommodation_view(request):
    operator_id = request.session.get('operator_id')
    if not operator_id:
        return redirect('operator_login')
    
    try:
        operator = Operator.objects.get(id=operator_id)
        return render(request, 'romaccom/addnewaccommodation.html', {
            'operator': operator
        })
    except Operator.DoesNotExist:
        # clear invalid session data
        request.session.pop('operator_id', None)
        request.session.pop('operator_name', None)
        return redirect('operator_login')

"""
Creare accomoation page
Operators can add accom name, address, postcode, description and google maps embedded link
"""
@csrf_exempt
def create_accommodation_view(request):
    if request.method == 'POST':
        operator_id = request.session.get('operator_id')
        if not operator_id:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=403)
        
        name = request.POST.get('name')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        description = request.POST.get('description', '') 
        map_link = request.POST.get('map_link')
        
        missing_fields = []
        if not name: missing_fields.append("name")
        if not address: missing_fields.append("address")
        if not postcode: missing_fields.append("postcode")
        if not map_link: missing_fields.append("map_link")

        if missing_fields:
            return JsonResponse({'success': False, 'error': f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
        
        try:
            validate_uk_address(address)
            validate_glasgow_postcode(postcode)            

            operator = Operator.objects.get(id=operator_id)
            
            accommodation = Accommodation.objects.create(
                name=name,
                address=address,
                postcode=postcode,
                description=description,
                map_link=map_link,
                average_rating=0.0,
                view_count=0
            )
            
            # associate the accom with the operator
            accommodation.operators.add(operator)
            
            # generate URL to redirect to dashboard for this accomm
            redirect_url = reverse('operator_dashboard') + f'?accommodation_id={accommodation.id}'
            
            return JsonResponse({
                'success': True,
                'accommodation_id': accommodation.id,
                'redirect_url': redirect_url
            })
            
        except ValidationError as e:
            print(f"Validation Error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Operator.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Operator not found'}, status=404)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Manage Accommodation Info
def manage_accom_info_view(request):
    return render(request, 'romaccom/manageaccommodationinfo.html')

logger = logging.getLogger(__name__)

"""
View for users to be able to change between public and private profiles
"""
@csrf_exempt
@login_required
def update_privacy_view(request):
    if request.method == 'POST':
        try:
            logger.info(f"Updating privacy for user: {request.user.username}")
            data = json.loads(request.body)
            private = data.get('private', False)
            logger.info(f"Received private value: {private}")

            request.user.profile_visibility = not private
            request.user.save()

            logger.info(f"Successfully updated privacy to: {request.user.profile_visibility}")

            return JsonResponse({
                'success': True,
                'new_visibility': request.user.profile_visibility
            })
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Error updating privacy: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': str(e)}
            , status=500)

    logger.warning("Invalid request method or unauthenticated user")
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)

"""
View to allowadding images to accoms
"""
@csrf_exempt
def upload_accommodation_images_view(request):
    if request.method == 'POST':
        accommodation_id = request.POST.get('accommodation_id')
        images = request.FILES.getlist('images')
        
        try:
            accommodation = Accommodation.objects.get(id=accommodation_id)
            
            for img in images:
                AccommodationImage.objects.create(
                    accommodation=accommodation,
                    image=img,
                    is_main=False  # set image as not the main one by default
                )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

"""
VIew to allow operators to update their accoms
Have to submit name, address, postcode, description and map link and validates these before updating
Handles invalid attempts gracefully
"""
@csrf_exempt
def update_accommodation_view(request):
    if request.method == 'POST':
        operator_id = request.session.get('operator_id')
        if not operator_id:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=403)
        
        accommodation_id = request.POST.get('accommodation_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        description = request.POST.get('description')
        map_link = request.POST.get('map_link')

        missing_fields = []
        if not name: missing_fields.append("name")
        if not address: missing_fields.append("address")
        if not postcode: missing_fields.append("postcode")

        if missing_fields:
            return JsonResponse({'success': False, 'error': f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
        
        try:
            validate_uk_address(address)
            validate_glasgow_postcode(postcode)

            operator = Operator.objects.get(id=operator_id)
            accommodation = Accommodation.objects.get(id=accommodation_id)
            
            # Verify the operator owns this accommodation
            if operator not in accommodation.operators.all():
                return JsonResponse({'success': False, 'error': 'Not authorized to manage this accommodation'}, status=403)
            
            accommodation.name = name
            accommodation.address = address
            accommodation.postcode = postcode
            accommodation.description = description
            accommodation.map_link = map_link
            accommodation.save()
            
            return JsonResponse({'success': True})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Operator.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Operator not found'}, status=404)
        except Accommodation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Accommodation not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

"""
VIew to allow operators to delete their accoms
Handles invalid attempts gracefully
Deleting the accomodation here cascade delete related objects
"""
@csrf_exempt
def delete_accommodation_view(request):
    if request.method == 'POST':
        operator_id = request.session.get('operator_id')
        if not operator_id:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=403)
        
        try:
            data = json.loads(request.body)
            accommodation_id = data.get('accommodation_id')
            
            operator = Operator.objects.get(id=operator_id)
            accommodation = Accommodation.objects.get(id=accommodation_id)
            
            # Verify the operator owns his accommodation
            if operator not in accommodation.operators.all():
                return JsonResponse({'success': False, 'error': 'Not authorized to delete this accommodation'}, status=403)
            
            accommodation.delete()
            
            if 'current_accommodation' in request.session:
                request.session.pop('current_accommodation', None)
            
            return JsonResponse({
                'success': True, 
                'redirect_url': reverse('management')
            })
            
        except Operator.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Operator not found'}, status=404)
        except Accommodation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Accommodation not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_accommodation_image_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            image = Image.objects.get(id=image_id)
            image.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def set_main_image_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            accommodation_id = data.get('accommodation_id')
            
            AccommodationImage.objects.filter(accommodation_id=accommodation_id).update(is_main=False)
            
            image = AccommodationImage.objects.get(id=image_id)
            image.is_main = True
            image.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

"""
VIew to allow users to delete their reviews
Handles invalid attempts gracefully
Deleting the review here cascade delete related objects
"""
@login_required
@require_POST
def delete_review(request):
    try:
        data = json.loads(request.body)
        review_id = data.get('review_id')
        
        review = Review.objects.get(id=review_id)
        
        # Security check to see if user is trying to delette someone elses review
        if review.user != request.user:
            return JsonResponse({'success': False, 'error': 'You are not authorized to delete this review'}, status=403)
        
        accommodation = review.accommodation
        
        review.delete()
        
        if accommodation:
            accommodation.update_average_rating()
        
        return JsonResponse({'success': True})
    
    except Review.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

"""
VIew to allow users to delete their accounts
Handles invalid attempts gracefully
Deleting the account here will cascade delete related objects
"""
@csrf_exempt
@login_required
@require_POST
def delete_account(request):
    try:
        user = request.user
        logger.info(f"Attempting to delete user: {user.username}")
        
        if not user.is_authenticated:
            logger.warning("Unauthenticated deletion attempt")
            return JsonResponse({
                'success': False,
                'error': 'User not authenticated'
            }, status=401)
        
        logger.info("Logging out user before deletion")
        logout(request)
        
        logger.info("Deleting user account")
        user.delete()
        logger.info("User account deleted successfully")
        
        return JsonResponse({
            'success': True,
            'message': 'Account and associated reviews deleted successfully',
            'redirect_url': '/'
        })
        
    except Exception as e:
        logger.error(f"Error deleting account: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while deleting your account'
        }, status=500)

"""
VIew to allow users to edit their reviews
Handles invalid attempts gracefully
"""
@login_required
def edit_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
        # security check to see if user is trying to edit someone elses review
    if review.user != request.user:
        return redirect('myreviews')
    
    accommodation = review.accommodation
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.save()
            
            new_images = request.FILES.getlist('images')
            if new_images:
                review.images.all().delete()
                
                Image.objects.create(review=review, image=new_images[0])
                
            accommodation.update_average_rating()
            return redirect('accom_review_detail', accom_id=accommodation.id, review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'romaccom/edit-review.html', {
        'form': form,
        'review': review,
        'accommodation': accommodation
    })

def management_view(request):
    operator_id = request.session.get('operator_id')
    if not operator_id:
        return redirect('operator_login')
    
    operator = Operator.objects.get(id=operator_id)
    accommodations = operator.accommodations.all()
    
    return render(request, 'romaccom/management.html', {
        'accommodations': accommodations,
        'operator': operator 
    })

def operator_profile_view(request, operator_id):
    operator = get_object_or_404(Operator, id=operator_id)
    profile = getattr(operator, "profile", None) 
    
    return render(request, "romaccom/operator_profile.html", {
        "operator": operator,
        "profile": profile
    })

"""
VIew to allow operators to edit their profukes
Handles invalid attempts gracefully
"""
def edit_operator_profile_view(request):
    operator_id = request.session.get('operator_id')

    if not operator_id:
        return redirect('operator_login')

    operator = get_object_or_404(Operator, id=operator_id)
    profile, created = OperatorProfile.objects.get_or_create(operator=operator)

    if request.method == "POST":
        form = OperatorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('management')
    else:
        form = OperatorProfileForm(instance=profile)

    return render(request, 'romaccom/edit_operator_profile.html', {
        'form': form,
        'operator': operator
    })

@login_required
def edit_user_profile_view(request):
    return render(request, 'romaccom/edit_user_profile.html')

"""
VIew to allow users to update their accounts
Handles invalid attempts gracefully
"""
@csrf_exempt
@login_required
def update_user_profile_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            
            username = request.POST.get('username')
            if username:
                user.username = username
            
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                
                if user.profile.picture:
                    try:
                        old_picture_path = user.profile.picture.path
                        if os.path.exists(old_picture_path):
                            os.remove(old_picture_path)
                    except Exception as e:
                        logger.warning(f"Failed to delete old profile picture: {str(e)}")
                
                try:
                    picture_name = f"profile_pictures/{user.id}_{int(time.time())}.jpg"
                    picture_path = default_storage.save(picture_name, profile_picture)
                    user.profile.picture = picture_path
                except Exception as e:
                    logger.error(f"Failed to save new profile picture: {str(e)}")
                    raise Exception("Failed to upload profile picture. Please try again.")
            
            user.save()
            user.profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully',
                'username': user.username,
                'profile_picture_url': user.profile.picture.url if user.profile.picture else None
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=400)

"""
VIew to allow operators to delete their accounts
Handles invalid attempts gracefully
Deleting the account here will cascade delete related objects
Database transactuon done atomically
"""
@csrf_exempt
def delete_operator_account_view(request):
    if request.method == 'POST':
        operator_id = request.session.get('operator_id')
        if not operator_id:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=403)

        try:
            with transaction.atomic(): # ensures data consistency across database
                operator = Operator.objects.get(id=operator_id)

                # delete all accommodations associated with the operator
                accommodations = operator.accommodations.all()
                for accommodation in accommodations:
                    accommodation.reviews.all().delete()  # delete reviews
                    accommodation.images.all().delete()  # delete images
                    accommodation.delete()  # delete accommodation

                # Delete th profile
                if hasattr(operator, "profile"):
                    operator.profile.delete()

                # Delete account
                operator.delete()

                request.session.flush()

            return JsonResponse({'success': True, 'redirect_url': '/'})  # redirects to homepage after 

        except Operator.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Operator not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
