from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from tours.models import Booking, Tour


def create_booking(user, tour_id, people_count):
    try:
        tour_id = int(tour_id)
    except (TypeError, ValueError):
        raise ValidationError({'error': 'tour_id must be a valid integer.'})

    try:
        people_count = int(people_count)
    except (TypeError, ValueError):
        raise ValidationError(
            {'error': 'people_count must be a positive integer.'}
        )

    if people_count <= 0:
        raise ValidationError(
            {'error': 'people_count must be greater than 0.'}
        )

    if user is None:
        raise ValidationError({'error': 'User is required.'})

    with transaction.atomic():
        try:
            tour = Tour.objects.select_for_update().get(id=tour_id)
        except Tour.DoesNotExist:
            raise ValidationError({'error': 'Tour not found.'})

        booked_people = (
            Booking.objects.filter(
                tour=tour,
                status__in=['pending', 'confirmed'],
            ).aggregate(total=Sum('people_count'))['total']
            or 0
        )
        available_places = tour.max_people - booked_people

        if people_count > available_places:
            raise ValidationError(
                {'error': 'Not enough available places.'}
            )

        total_price = tour.price * Decimal(people_count)
        available_places_after_booking = available_places - people_count
        booking = Booking.objects.create(
            user=user,
            tour=tour,
            people_count=people_count,
            status='pending',
        )

    return booking, total_price, available_places_after_booking
