from django.contrib import admin
from django.urls import path
from user_app.api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.api_view, name='register'),
]
