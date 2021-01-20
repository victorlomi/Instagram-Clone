from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Profile, Following


def homepage(request):
    return render(request, 'index.html') 


def profile(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.filter(user__username=request.user.username)[0]
        following = Following.objects.filter(following_profile_id=current_user.id)
        followers = Following.objects.filter(profile_id=current_user.id)
        posts = Image.objects.filter(profile=current_user.id)
        return render(request, "profile.html", {"posts": posts, "following": following, "followers": followers})
    else:
        return redirect("homepage") 


def post(request, post):
    return HttpResponse(f"here's your post: {post}") 


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
