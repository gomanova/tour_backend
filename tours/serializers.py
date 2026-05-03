from rest_framework import serializers
from .models import Tour


class TourSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    
    class Meta:
        model = Tour
        fields = [
            'id',
            'title',
            'description',
            'price',
            'location',
            'duration',
            'difficulty',
            'max_people',
            'image',
        ]
