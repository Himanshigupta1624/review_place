from django.urls import path
from .views import RegisterView,LoginView,AddReviewView,PlaceDetailView,PlaceSearchView
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('add-review/',AddReviewView.as_view(),name='add-review'),
    path('places/<int:pk>/',PlaceDetailView.as_view(),name='place-detail'),
    path('places/',PlaceSearchView.as_view(),name='place-search'),
]