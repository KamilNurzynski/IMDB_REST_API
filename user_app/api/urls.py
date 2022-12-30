from django.contrib import admin
from django.urls import path
from user_app.api import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
