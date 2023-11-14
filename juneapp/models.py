from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.dispatch import receiver



# Create your models here.
# Creating a user profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    follows = models.ManyToManyField("self",
                                    related_name = "followed_by",  
                                    symmetrical = False,     
                                    blank = True)
    date_modified = models.DateTimeField(User, auto_now = True)
    profile_image = models.ImageField(null = True, blank = True, upload_to = 'images/')

    profile_bio = models.CharField(null = True, blank = True, max_length = 500)
    website_link = models.CharField(null = True, blank = True, max_length = 100)
    facebook_link = models.CharField(null = True, blank = True, max_length = 100)
    instagram_link = models.CharField(null = True, blank = True, max_length = 100)
    linkedin_link = models.CharField(null = True, blank = True, max_length = 100)
    def __str__(self):
        return self.user.username


class June(models.Model):

    user = models.ForeignKey(
        User, 
        related_name = "junes",
        on_delete = models.DO_NOTHING
    )
    body = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name = "june_likes", blank = True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user}" + f" {self.created_at:%Y-%m-%d %H-%M}: " + f"{self.body}" 
        



# Using signals, Django signals - It is used whenever we need certain task to be performed when another thing somewhere changes!
# Creating a Profile for the new user as they sign up!


# @receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

        # Have the new user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender = User)
'''The post_save is the 'signal' here!'''




'''
From models module:

The code defines a Django model named Profile.
This Profile model has a one-to-one relationship with the built-in User model from django.contrib.auth.models.
It also has a many-to-many relationship with itself, representing a follow/follower relationship.
The __str__ method is overridden to return the username of the associated user.

'''