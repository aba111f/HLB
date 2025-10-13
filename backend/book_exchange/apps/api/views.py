import logging
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .models import Book, ExchangeRequest
from .serializers import UserSerializer, BookSerializer, ExchangeRequestSerializer

logger = logging.getLogger(__name__)
User = get_user_model()

# --- Login view ---

class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "id": str(user.id),
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


# --- User ViewSet ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #Permission check
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    #Create
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid user registration: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        logger.info(f"User created: {serializer.data['email']}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #Delete 
    def destroy(self, request, *args, **kwargs):
        uuid = kwargs.get("pk")
        email = request.data.get("email")
        password = request.data.get("password")

        # print(uuid, email, password)


        if not all([uuid, email, password]):
            return Response({"detail": "UUID, email, and password are required."}, status=400)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=403)

        try:
            target_user = User.objects.get(id=uuid)
        except User.DoesNotExist:
            # print(uuid)
            return Response({"detail": "User not found."}, status=404)

        target_user.delete()
        return Response({"detail": "User deleted successfully."}, status=204)
    # Get all
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Get data of specific user
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Filter users by cities/book
    @action(detail=False, methods=['post'], url_path='filter')
    def filter_users(self, request):
        cities = request.data.get('cities', [])
        books = request.data.get('books', [])

        users = User.objects.all()

        #Uses "OR" filtering
        if cities:
            users = users.filter(city__in=cities)

        #Uses "AND" filtering
        if books:
            for book_title in books:
                users = users.filter(books__title=book_title)

        users = users.distinct()

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            from_user=self.request.user
        ) | ExchangeRequest.objects.filter(to_user=self.request.user)

    def perform_create(self, serializer):
        to_user_id = self.request.data.get("to_user_id")
        to_user = get_object_or_404(User, id=to_user_id)

        if to_user == self.request.user:
            return Response({"error": "You cannot send a request to yourself"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=self.request.user, to_user=to_user)
        logger.info(f"Exchange request from {self.request.user} to {to_user}")

    @action(detail=True, methods=["post"], url_path="accept")
    def accept_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.to_user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        exchange_request.status = "accepted"
        exchange_request.save()
        logger.info(f"Exchange request {exchange_request.id} accepted")
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.to_user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        exchange_request.status = "rejected"
        exchange_request.save()
        logger.info(f"Exchange request {exchange_request.id} rejected")
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)
