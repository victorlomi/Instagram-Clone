from django.urls import path, include

from . import views 

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('', include('django.contrib.auth.urls'))
] 
