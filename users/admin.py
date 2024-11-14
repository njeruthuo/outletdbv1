from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'phone_number', 'access_level', 'is_staff', 'is_active')

    # Specify which fields can be searched in the admin interface
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'phone_number')

    # Specify which fields to filter by in the admin interface
    list_filter = ('access_level', 'is_staff', 'is_active', 'phone_number')

    # Define the fieldsets to control the layout of the user edit form
    fieldsets = (
        (None, {'fields': ('photo', 'email', 'phone_number')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        # Include the custom access_level field
        ('Access Level', {'fields': ('access_level',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fieldsets for adding a new user in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('photo', 'username', 'phone_number', 'password1', 'password2', 'access_level', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
