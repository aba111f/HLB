import logging
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Book, ExchangeRequest
from .serializers import UserSerializer, BookSerializer, ExchangeRequestSerializer

logger = logging.getLogger(__name__)
User = get_user_model()

# --- User ViewSet ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        elif self.action in ["list", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid user registration: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        logger.info(f"User created: {serializer.data['email']}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --- Book ViewSet ---
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            return Book.objects.all()
        return Book.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"], url_path="search")
    def search_books(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(title__icontains=query).select_related("owner")
        data = BookSerializer(books, many=True).data
        return Response(data, status=status.HTTP_200_OK)


# --- ExchangeRequest ViewSet ---
class ExchangeRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeRequest.objects.filter(
            sender=self.request.user
        ) | ExchangeRequest.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        receiver_id = self.request.data.get("receiver_id")
        receiver = get_object_or_404(User, id=receiver_id)

        if receiver == self.request.user:
            return Response({"error": "You cannot send a request to yourself"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(sender=self.request.user, receiver=receiver)
        logger.info(f"Exchange request from {self.request.user} to {receiver}")


    @action(detail=True, methods=["post"], url_path="accept")
    def accept_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.receiver != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        exchange_request.status = "accepted"
        exchange_request.save()
        logger.info(f"Exchange request {exchange_request.id} accepted")
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.receiver != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        exchange_request.status = "rejected"
        exchange_request.save()
        logger.info(f"Exchange request {exchange_request.id} rejected")
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)
