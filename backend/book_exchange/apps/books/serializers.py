from rest_framework import serializers
from .models import Book
from apps.users.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "owner",
            "title",
            "author",
            "genre",
            "description",
            "condition",
            "availability",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "owner"]
