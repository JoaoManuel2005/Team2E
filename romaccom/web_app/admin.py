from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Accommodation, Review, Operator, UserProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("account_type", "profile_visibility")}),
    )

admin.site.register(Accommodation)
admin.site.register(Review)
admin.site.register(Operator)
admin.site.register(UserProfile)

admin.site.site_header = "RomAccom Admin Panel"
admin.site.site_title = "RomAccom Admin"
admin.site.index_title = "Welcome to the RomAccom Admin Panel"