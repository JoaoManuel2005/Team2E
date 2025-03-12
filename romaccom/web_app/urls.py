from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('trending/', views.trending_view, name='trending'),
    path('top-rated/', views.top_rated_view, name='top_rated'),
    path('contact-us/', views.contact_view, name='contact'),
    path('about-us/', views.about_view, name='about'),
    
    path('register/', views.user_register_view, name='user_register'),
    path('operator/register/', views.operator_register_view, name='operator_register'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/myaccount/', views.my_account_view, name='myaccount'),
    path('user/myaccount/myreviews/', views.my_reviews_view, name='myreviews'),
    # path('user/myaccount/privacy-settings/', views.privacy_settings_view, name='privacy_settings'),

    path('search/', views.search_view, name='search'),
    path('search/results/', views.search_results_view, name='search_results'),
    path('search/accomlist/', views.accom_list_view, name='accomlist'),
    path('search/accomlist/accompage/<int:accom_id>/', views.accom_page_view, name='accommodation_detail'),
    path('search/accomlist/accompage/info/<int:accom_id>/', views.accom_page_view, name='accom_info'),
    path('search/accomlist/accompage/<int:accom_id>/reviews/<int:review_id>/', views.accom_reviews_view, name='accom_review_detail'),
    path('search/accomlist/accompage/map/<int:accom_id>/', views.accom_map_view, name='accom_map'),
    path('search/accomlist/accompage/write-review/<int:accom_id>/', views.write_review_view, name='write_review'),

    path('accom/<int:accom_id>/', views.accom_page_view, name='accom_page_view'),
    path('accom/<int:accom_id>/write-review/', views.write_review_view, name='write_review'),

    path('operator/login/', views.operator_login_view, name='operator_login'),
    path('operator/dashboard/', views.operator_dashboard_view, name='operator_dashboard'),
    path('operator/dashboard/mylistings/', views.my_listings_view, name='mylistings'),
    path('operator/dashboard/addnewaccommodation/', views.add_accommodation_view, name='add_accommodation'),
    path('operator/dashboard/manageaccommodationinfo/', views.manage_accom_info_view, name='manage_accom_info'),
]
