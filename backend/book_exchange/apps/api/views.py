import logging
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Book, ExchangeRequest
from .serializers import UserSerializer, BookSerializer, ExchangeRequestSerializer

logger = logging.getLogger(__name__)

class CustomLoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            logger.warning("Login failed: Missing email or password")
            return Response({"error": "Email and password required"}, status=400)

        user = authenticate(email=email, password=password)
        if user is None:
            logger.warning(f"Login failed for email={email}")
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        logger.info(f"User {user.email} logged in successfully")

        return Response({
            "id": user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"User creation failed: {serializer.errors}")
            return Response(serializer.errors, status=400)
        try:
            self.perform_create(serializer)
            logger.info(f"User created: {serializer.data['email']}")
        except Exception as e:
            logger.exception("Unexpected error during user creation")
            return Response({"error": str(e)}, status=500)
        return Response(serializer.data, status=201)

    def destroy(self, request, *args, **kwargs):
        uuid = kwargs.get("pk")
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            logger.warning("Delete failed: Missing email or password")
            return Response({"error": "Email and password required"}, status=400)

        user = authenticate(email=email, password=password)
        if user is None:
            logger.warning(f"Delete failed: Invalid credentials for email={email}")
            return Response({"error": "Invalid credentials"}, status=401)

        if str(user.id) != str(uuid) and not request.user.is_staff:
            logger.warning(f"Unauthorized delete attempt by {user.email} on {uuid}")
            return Response({"detail": "Permission denied."}, status=403)

        instance = get_object_or_404(User, pk=uuid)
        self.perform_destroy(instance)
        logger.info(f"User deleted: {instance.email}")
        return Response(status=204)

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        logger.info(f"User list requested by {request.user.email}")
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def filter_users(self, request):
        cities = request.data.get("cities", [])
        books = request.data.get("books", [])

        if not isinstance(cities, list) or not isinstance(books, list):
            logger.warning(f"Invalid filter input: {request.data}")
            return Response({"error": "Cities and books must be lists"}, status=400)

        users = User.objects.all()
        if cities:
            users = users.filter(city__in=cities)
        if books:
            users = users.filter(books__title__in=books).distinct()

        logger.info(f"User filter applied: cities={cities}, books={books}")
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"Book created by {self.request.user.email}: {serializer.data['title']}")

    @action(detail=False, methods=["get"])
    def search_books(self, request):
        query = request.query_params.get("q")
        if not query:
            logger.warning("Book search failed: Missing 'q' parameter")
            return Response({"error": "Missing search query"}, status=400)

        books = Book.objects.filter(title__icontains=query)
        logger.info(f"Book search query: '{query}' -> {len(books)} results")
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class ExchangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        to_user_id = self.request.data.get("to_user_id")
        to_user = get_object_or_404(User, id=to_user_id)
        if to_user == self.request.user:
            logger.warning(f"User {self.request.user.email} tried to send request to self")
            raise ValidationError({"error": "You cannot send a request to yourself"})
        serializer.save(from_user=self.request.user, to_user=to_user)
        logger.info(f"Exchange request created: from {self.request.user.email} to {to_user.email}")

    @action(detail=True, methods=["post"])
    def accept_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.to_user != request.user:
            logger.warning(f"Unauthorized accept attempt by {request.user.email}")
            return Response({"error": "You cannot accept this request"}, status=403)
        exchange_request.status = "accepted"
        exchange_request.save()
        logger.info(f"Exchange request accepted by {request.user.email}")
        return Response({"status": "accepted"})

    @action(detail=True, methods=["post"])
    def reject_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.to_user != request.user:
            logger.warning(f"Unauthorized reject attempt by {request.user.email}")
            return Response({"error": "You cannot reject this request"}, status=403)
        exchange_request.status = "rejected"
        exchange_request.save()
        logger.info(f"Exchange request rejected by {request.user.email}")
        return Response({"status": "rejected"})
