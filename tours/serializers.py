from rest_framework import serializers
from .models import Tour, Review, TourDate, Booking


class ItineraryDaySerializer(serializers.Serializer):
    day = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = ['id', 'start_date', 'end_date', 'available_spots']


class TourSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    average_rating = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    itinerary = ItineraryDaySerializer(many=True, required=False)
    booking_url = serializers.SerializerMethodField()
    dates = TourDateSerializer(many=True, read_only=True)
    available_spots = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            'id',
            'title',
            'description',
            'price',
            'location',
            'duration',
            'duration_display',
            'difficulty',
            'max_people',
            'image',
            'average_rating',
            'gallery',
            'itinerary',
            'included',
            'excluded',
            'equipment',
            'accommodation',
            'booking_url',
            'guide_name',
            'guide_bio',
            'dates',
            'available_spots',
        ]

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(tour=obj)
        if not reviews.exists():
            return None
        total = sum(r.rating for r in reviews)
        return round(total / reviews.count(), 1)

    def get_duration_display(self, obj):
        days = obj.duration
        nights = days - 1
        return f"{days} дней / {nights} ночей"

    def get_booking_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/bookings/?tour_id={obj.id}')
        return f'/api/bookings/?tour_id={obj.id}'

    def get_available_spots(self, obj):
        booked = Booking.objects.filter(
            tour=obj,
            status='confirmed'
        ).values_list('people_count', flat=True)
        total_booked = sum(booked)
        return max(obj.max_people - total_booked, 0)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'tour_id', 'rating', 'comment']
        read_only_fields = ['id', 'user_id']