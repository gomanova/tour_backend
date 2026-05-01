from django.urls import path
from .views import ProfileView, BookingListCreateView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-api'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-api'),
]