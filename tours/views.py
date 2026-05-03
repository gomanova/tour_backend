from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, User, Tour
from .services import booking_service

from .serializers import TourSerializer

def get_booking_user(request):
    request_user = getattr(request, 'user', None)
    if request_user and not getattr(request_user, 'is_anonymous', False):
        return request_user

    # TODO: replace with real auth later
    return User.objects.first()


class BookingListCreateView(APIView):
    def post(self, request):
        tour_id = request.data.get('tour_id')
        people_count = request.data.get('people_count')
        user = get_booking_user(request)

        (
            booking,
            total_price,
            available_places_after_booking,
        ) = booking_service.create_booking(
            user=user,
            tour_id=tour_id,
            people_count=people_count,
        )

        return Response(
            {
                'booking_id': booking.id,
                'status': booking.status,
                'total_price': total_price,
                'available_places': available_places_after_booking,
            },
            status=status.HTTP_201_CREATED,
        )


class BookingConfirmView(APIView):
    def post(self, request, id):
        with transaction.atomic():
            try:
                booking = Booking.objects.select_for_update().get(id=id)
            except Booking.DoesNotExist:
                return Response(
                    {'error': 'Booking not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if booking.status == 'confirmed':
                return Response(
                    {'error': 'Booking is already confirmed.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = get_booking_user(request)
            if user is not None and booking.user_id != getattr(user, 'id', None):
                return Response(
                    {'error': 'You cannot confirm this booking.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

            booking.status = 'confirmed'
            booking.save()

        return Response(
            {
                'booking_id': booking.id,
                'status': booking.status,
            }
        )
class TourListView(APIView):
    def get(self, request):
        tours = Tour.objects.all()

        location = request.query_params.get('location')
        difficulty = request.query_params.get('difficulty')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        if location:
            tours = tours.filter(location=location)
        if difficulty:
            tours = tours.filter(difficulty=difficulty)
        if price_min:
            tours = tours.filter(price__gte=float(price_min))
        if price_max:
            tours = tours.filter(price__lte=float(price_max))

        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        skip = (page - 1) * limit
        tours = tours[skip: skip + limit]

        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)


class TourDetailView(APIView):
    def get(self, request, tour_id):
        try:
            tour = Tour.objects.get(id=tour_id)
        except Tour.DoesNotExist:
            return Response(
                {'detail': 'Тур не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TourSerializer(tour)
        return Response(serializer.data)
