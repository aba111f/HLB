from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "owner")
    search_fields = ("title", "author")
    list_filter = ("author",)