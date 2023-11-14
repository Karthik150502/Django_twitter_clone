from django.contrib import admin
from django.contrib.auth.models import Group, User
from juneapp.models import Profile, June
# Register your models here.




# Mixing Profile info with User Info
class ProfileInline(admin.StackedInline):
    model = Profile


# Unregistering Group
admin.site.unregister(Group)


# Extending the User model, we use (admin.ModelAdmin) as the super class for inheritance.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

# Unregistering initial User
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)

'''
From admin module:

The code starts with importing necessary modules from the Django admin.
The ProfileInline class is defined to represent the Profile model inline within the User model in the Django admin interface.
The Group model is unregistered from the Django admin interface.
The UserAdmin class is created to customize the way the User model is displayed in the admin interface.
The fields attribute specifies which fields of the User model should be displayed.
The inlines attribute specifies that the ProfileInline should be displayed inline with the User model.
The initial User model is unregistered from the Django admin.
Then, the User model and the Profile model are reregistered with the customized UserAdmin class.
In summary, the code is creating a custom profile model with a one-to-one relationship with the built-in Django User model. It is configuring the Django admin interface to display the Profile model inline with the User model, thereby extending the functionality of the Django admin interface.

'''


#Registering the june/ tweet model to the Admin panel
admin.site.register(June)