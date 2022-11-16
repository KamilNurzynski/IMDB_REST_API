from django.contrib import admin
from django.urls import path, include
from watchlist_app import views

urlpatterns = [
    path('list/', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_details, name='movie_details')
]
