from rest_framework import serializers
from .models import ExchangeRequest, Deal, Review
from users.serializers import UserSerializer
from books.serializers import BookSerializer

class ExchangeRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    offered_book = BookSerializer(read_only=True)
    requested_book = BookSerializer(read_only=True)

    class Meta:
        model = ExchangeRequest
        fields = [
            "id",
            "from_user",
            "to_user",
            "offered_book",
            "requested_book",
            "message",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "status"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["from_user"] = request.user
        return super().create(validated_data)


class DealSerializer(serializers.ModelSerializer):
    exchange_request = ExchangeRequestSerializer(read_only=True)

    class Meta:
        model = Deal
        fields = ["id", "exchange_request", "completed_at"]
        read_only_fields = ["id", "completed_at"]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed_user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "reviewer", "reviewed_user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["reviewer"] = request.user
        return super().create(validated_data)
