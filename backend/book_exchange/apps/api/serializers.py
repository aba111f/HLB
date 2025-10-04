from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Book, ExchangeRequest

User = get_user_model()


# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "created_at"]
        read_only_fields = ["id", "role", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# --- Book Serializer ---
class BookSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]


# --- ExchangeRequest Serializer ---
class ExchangeRequestSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ExchangeRequest
        fields = ["id", "sender", "receiver", "book", "status", "created_at"]
        read_only_fields = ["id", "sender", "status", "created_at"]

    def validate(self, data):
        book = data.get("book")
        if book.owner == self.context["request"].user:
            raise serializers.ValidationError("You cannot request your own book")
        return data
