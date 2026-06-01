from django.urls import path
from .views import (
    BookingConfirmView,
    BookingListCreateView,
    TourListView,
    TourDetailView,
    TourSimilarView,
)

urlpatterns = [
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:id>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
    
    path('tours/', TourListView.as_view(), name='tour-list'),
    path('tours/<int:tour_id>/', TourDetailView.as_view(), name='tour-detail'),
    path('tours/<int:tour_id>/similar/', TourSimilarView.as_view(), name='tour-similar'),
]
