from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import *
from .models import Image, Profile, Following

def homepage(request):
    # Homepage view displaying the user's timeline and suggestions for people they can 
    # choose to follow
    if request.user.is_authenticated:
        users = User.objects.all()[:3]
        return render(request, 'index.html', {"users": users}) 
    else:
        return render(request, 'index.html') 


def profile(request, user_id):
    # Profile view that shows a user's page with information regarding followers,
    # following, and their photos
    current_user = User.objects.get(id=user_id)
    followers = Following.objects.filter(following_id=current_user.id)
    following = Following.objects.filter(follower_id=current_user.id)
    posts = Image.objects.filter(user_id=current_user.id)

    return render(request, "profile.html", {"posts": posts, "following": following, "followers": followers, "current_user": current_user})


def profile_follow(request):
    followed_user = User.objects.get(id=request.POST['id'])
    follow = Following(follower=request.user, following=followed_user) 
    follow.save()

    # get the information for the user's profile
    followers = Following.objects.filter(following_id=followed_user.id)
    following = Following.objects.filter(follower_id=followed_user.id)
    posts = Image.objects.filter(user_id=followed_user.id)

    return render(request, "profile.html", {"posts": posts, "following": following, "followers": followers, "current_user": followed_user})


def profile_unfollow(request):
    return HttpResponse(request.POST)


def post(request, post):
    image = Image.objects.get(id=post)
    return render(request, "post.html", {"post": image}) 


def search_results(request):
	# Search results view that searches for users and allows you to go to 
    # their profile page
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_usernames = User.objects.filter(username__icontains=search_term)
        return render(request, 'search.html',{"search_term": search_term,"searched_usernames": searched_usernames})
    else:
        message = "No Results"
        return render(request, 'all-news/search.html',{"message":message})


def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
