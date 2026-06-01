from django.contrib import admin
from .models import User, Tour, Booking, Payment, Review, TourDate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "location", "difficulty", "accommodation")
    search_fields = ("title", "location")
    list_filter = ("difficulty",)


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ("id", "tour", "start_date", "end_date", "available_spots")
    list_filter = ("tour",)
    list_select_related = ("tour",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tour", "people_count", "status")
    list_filter = ("status",)
    list_select_related = ("user", "tour")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "status")
    list_filter = ("status",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tour", "rating")
    list_filter = ("rating",)
    list_select_related = ("user", "tour")