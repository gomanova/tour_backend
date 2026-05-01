
from rest_framework import serializers
from .models import User, Tour, Booking

# Сериализатор профиля (Задача 1)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        read_only_fields = ['id', 'email'] # Почту менять нельзя

# Сериализатор бронирования (Задача 2 и 3)
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'tour', 'people_count', 'status']
        # Статус и юзер — только для чтения, их ставим в коде (perform_create)
        read_only_fields = ['id', 'status', 'user']