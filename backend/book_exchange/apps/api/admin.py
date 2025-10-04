from django.contrib import admin
from .models import User, Book, ExchangeRequest, Deal, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username")
    list_filter = ("is_staff", "is_superuser", "is_active")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "owner")
    search_fields = ("title", "author")
    list_filter = ("author",)

@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "get_offered_book", "get_requested_book", "status", "created_at")

    def get_offered_book(self, obj):
        return obj.offered_book.title if obj.offered_book else "-"
    get_offered_book.short_description = "Offered Book"

    def get_requested_book(self, obj):
        return obj.requested_book.title
    get_requested_book.short_description = "Requested Book"

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "exchange_request", "completed_at")
    search_fields = ("exchange_request__id", "exchange_request__book__title")
    list_filter = ("completed_at",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "reviewed_user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("reviewer__username", "reviewed_user__username", "comment")
