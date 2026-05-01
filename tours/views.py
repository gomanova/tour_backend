from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import User, Booking
from .serializers import ProfileSerializer, BookingSerializer

# Задача 1: Профиль (Получение и обновление)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        # Если юзеров нет вообще, вернем None (DRF выдаст 404, что лучше, чем ошибка 500)
        return User.objects.first()

# Задача 2 и 3: Бронирования (Список и создание)
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        # Берем первого юзера
        first_user = User.objects.first() 
        
        # Если юзера нет, выдаем понятную ошибку вместо IntegrityError
        if not first_user:
            raise ValidationError({"detail": "В базе данных нет ни одного пользователя. Создайте юзера в админке или через shell."})
            
        # Сохраняем каркас: статус всегда pending (Айбек допишет логику здесь)
        serializer.save(user=first_user, status="pending")

    def get_queryset(self):
        return Booking.objects.all()