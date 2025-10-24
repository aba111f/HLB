import logging
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

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
        return Response({f"User deleted: {instance.email}"}, status=200)

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