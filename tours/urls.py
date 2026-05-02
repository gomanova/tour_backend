from django.urls import path

from .views import BookingConfirmView, BookingListCreateView

urlpatterns = [
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:id>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
]
