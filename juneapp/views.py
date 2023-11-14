from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, June
from django.contrib import messages
from .forms import JuneForm, SignUpForm, TheUpdateForm, TheProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



# Create your views here.



def home(request):
    if request.user.is_authenticated:
        form = JuneForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                june = form.save(commit = False)
                june.user = request.user
                june.save()
                messages.success(request, ("You have juned it!"))
                return redirect('home')
        junes = June.objects.all().order_by("-created_at")
        return render(request, "home.html", {"junes":junes, "form":form})
    else:
        junes = June.objects.all().order_by("-created_at")
        return render(request, "home.html", {"junes":junes})



def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, "profile_list.html", {'profiles':profiles})  
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        junes = June.objects.filter(user_id = pk).order_by("-created_at")
        # POST form logic
        if request.method == "POST":

            # Get current user
            current_user_profile = request.user.profile

            # Get form data
            action = request.POST['follow']
            
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            # save the profile
            current_user_profile.save()
        return render(request, 'profile.html',{"profile":profile,"junes":junes})
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        
        return redirect('home')
    


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in, get Junin!"))
            return redirect('home')
        else:
            messages.error(request, ("An error occured while logging in, please verify the crendentials and try again..! "))
            return redirect('login')

    else:
        return render(request, 'login.html', {})
    ...
def logout_user(request):
    logout(request)
    messages.info(request, ('You have been Logged out!'))
    return redirect('home')


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            
            #Login the user right away after they are done registering! 
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('You have successfully registered, Welcome..!'))
            return redirect('home')
    return render(request, "register.html",{"form":form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)

        # Get forms
        user_form = TheUpdateForm(request.POST or None, request.FILES or None, instance = current_user)
        profile_form = TheProfilePicForm(request.POST or None, request.FILES or None, instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your Profile has been updated!"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, "profile_form":profile_form})
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')
    
def june_like(request, pk):
    if request.user.is_authenticated:
        june = get_object_or_404(June, id = pk)
        if june.likes.filter(id = request.user.id):
            
            june.likes.remove(request.user)
        else:
            june.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))





    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')
    

def june_share(request, pk):
    june = get_object_or_404(June, id = pk)
    if june:
        return render(request, "show_june.html",{"june":june})
    else:
        messages.warning(request, ("That June does not exist...!"))
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)

        # Unfollow the user 
        request.user.profile.follows.remove(profile)
        # Save the profile
        request.user.profile.save()
        messages.warning(request, (f"Unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
        pass
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')



def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id = pk)

        # Unfollow the user 
        request.user.profile.follows.add(profile)
        # Save the profile
        request.user.profile.save()
        messages.warning(request, (f"Followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
        pass
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')



def followers_page(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, "followers_page.html", {'profiles':profiles})  
        else:
            messages.warning(request, ("That is not your profile page.!!"))
            return redirect('home')
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')
    

def following_page(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, "following_page.html", {'profiles':profiles})  
        else:
            messages.warning(request, ("That is not your profile page!"))
            return redirect('home')
    else:
        messages.warning(request, ("You must be logged in to view this page!"))
        return redirect('home')
    

def delete_june(request, pk):
    if request.user.is_authenticated:
        june = get_object_or_404(June, id = pk)
        # Check to see, if you own the june
        if request.user.username == june.user.username:
            # Delete the june
            june.delete()
            messages.warning(request, ("The june has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.warning(request, ("Not your june buddy!"))
            return redirect('home')
    else:
        messages.warning(request, ("Please login to continue!"))
        return redirect(request.META.get("HTTP_REFERER"))
    
def edit_june(request, pk):
    if request.user.is_authenticated:

        # Grab the june
        june = get_object_or_404(June, id = pk)

        # Check to see, if you own the june
        if request.user.username == june.user.username:
            form = JuneForm(request.POST or None, instance = june)
            if request.method == "POST":
                if form.is_valid():
                    june = form.save(commit = False)
                    june.user = request.user
                    june.save()
                    messages.success(request, ("Your june has been edited and updated!"))
                    return redirect('home')
            else:
                return render(request, 'edit_june.html', {'form':form, "june":june})
        else:
            messages.warning(request, ("Not your june buddy!"))
            return redirect('home')
    else:
        messages.warning(request, ("Please login to continue!"))
        return redirect('home')


def search_june(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search_june']

        # Searching the database
        searched = June.objects.filter(body__contains = search)
        return render(request, 'search_june.html',{'search':search, 'searched':searched}) 
    else:
        return render(request, 'search_june.html',{})
    

def search_user(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search_june']

        # Searching the database
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html',{'search':search, 'searched':searched}) 
    else:
        return render(request, 'search_user.html',{})
