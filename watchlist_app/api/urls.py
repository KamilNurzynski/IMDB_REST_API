from django.contrib import admin
from django.urls import path, include
from watchlist_app.api import views

urlpatterns = [
    # path('list/', views.movie_list, name='movie_list'),
    # path('<int:pk>/', views.movie_details, name='movie_details')
    path('list/', views.WatchListAV.as_view(), name='movie_list'),
    path('<int:pk>/', views.WatchListDetailsAV.as_view(), name='movie_details'),
    path('stream_platform/list/', views.StreamPlatformListAV.as_view(), name='stream_platform_list'),
    path('stream_platform/<int:pk>/', views.StreamPlatformDetailsAV.as_view(), name='stream_platform_details'),
]
