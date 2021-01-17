from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request, 'index.html') 


def signup(request):
    return HttpResponse("signup")


def login(request):
    return HttpResponse("login")
