from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Profile, Following


def homepage(request):
    suggestions = Profile.objects.all()
    if request.user.is_authenticated:
        current_user = Profile.objects.filter(user__username=request.user.username)[0]
        following = Following.objects.filter(profile_id=current_user.id)
        print(following)
        images = []
        for follow in following:
            follow_images = Image.objects.filter(profile__id=follow.following_profile_id.id)
            images.append(follow_images)
        return render(request, "index.html", {"following": following, "images": images, "suggestions": suggestions})
    else:
        return render(request, 'index.html') 


def profile(request, user):
    current_user = Profile.objects.get(id=user)
    followers = Following.objects.filter(following_profile_id=current_user.id)
    following = Following.objects.filter(profile_id=current_user.id)
    posts = Image.objects.filter(profile=current_user.id)

    return render(request, "profile.html", {"posts": posts, "following": following, "followers": followers, "current_user": current_user})

def post(request, post):
    image = Image.objects.get(id=post)
    return render(request, "post.html", {"post": image}) 


def search_results(request):
	#Search for a category or a location
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_usernames = Profile.objects.filter(user__username__icontains=search_term)
        message = f"{search_term}"
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
