import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.books.models import Book
from .models import ExchangeRequest
from .serializers import ExchangeRequestSerializer

logger = logging.getLogger(__name__)


class ExchangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Expects JSON (or form) with:
         - from_email (optional, defaults to request.user.email)
         - to_email (required)
         - exchange_type (optional)
         - offered_book_id (optional)
         - requested_book_id (required)
         - message (optional)
        """
        from_email = request.data.get("from_email") or getattr(request.user, "email", None)
        to_email = request.data.get("to_email")
        exchange_type = request.data.get("exchange_type")
        offered_book_id = request.data.get("offered_book_id")
        requested_book_id = request.data.get("requested_book_id")
        message = request.data.get("message", "")

        if not from_email:
            return Response({"error": "from_email is required or user must be authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        if not to_email:
            return Response({"error": "to_email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not requested_book_id:
            return Response({"error": "requested_book_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_user = User.objects.get(email=from_email)
        except User.DoesNotExist:
            return Response({"error": "from_user not found"}, status=status.HTTP_404_NOT_FOUND)

        # ensure the requester actually is from_user (prevent forging)
        if from_user != request.user:
            return Response({"error": "from_email must match authenticated user"}, status=status.HTTP_403_FORBIDDEN)

        try:
            to_user = User.objects.get(email=to_email)
        except User.DoesNotExist:
            return Response({"error": "to_user not found"}, status=status.HTTP_404_NOT_FOUND)

        if to_user == from_user:
            return Response({"error": "You cannot send a request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        offered_book = None
        if offered_book_id:
            try:
                offered_book = Book.objects.get(id=offered_book_id)
            except Book.DoesNotExist:
                return Response({"error": "offered_book not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            requested_book = Book.objects.get(id=requested_book_id)
        except Book.DoesNotExist:
            return Response({"error": "requested_book not found"}, status=status.HTTP_404_NOT_FOUND)

        # build kwargs dynamically to avoid errors if model doesn't have exchange_type
        create_kwargs = {
            "from_user": from_user,
            "to_user": to_user,
            "requested_book": requested_book,
            "message": message,
        }
        if offered_book:
            create_kwargs["offered_book"] = offered_book

        model_field_names = {f.name for f in ExchangeRequest._meta.get_fields()}
        if "exchange_type" in model_field_names and exchange_type is not None:
            create_kwargs["exchange_type"] = exchange_type

        exchange_request = ExchangeRequest.objects.create(**create_kwargs)
        logger.info(f"Exchange request created: from {from_user.email} to {to_user.email}")

        serializer = self.get_serializer(exchange_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # keep default behavior for other code paths if needed
        serializer.save(from_user=self.request.user)

    @action(detail=True, methods=["post"])
    def accept_request(self, request, pk=None):
        exchange_request = self.get_object()
        if exchange_request.to_user != request.user:
            logger.warning(f"Unauthorized accept attempt by {request.user.email}")
            return Response({"error": "You cannot accept this request"}, status=403)
        # set status if such field exists
        if hasattr(exchange_request, "status"):
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
        if hasattr(exchange_request, "status"):
            exchange_request.status = "rejected"
            exchange_request.save()
        logger.info(f"Exchange request rejected by {request.user.email}")
        return Response({"status": "rejected"})