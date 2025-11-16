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

from django.core.cache import cache

from apps.kafka.producers.producer_general import send_message

logger = logging.getLogger(__name__)


class ExchangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        from_email = request.user.email
        to_email = request.data.get("to_email")
        requested_book_id = request.data.get("requested_book_id")
        offered_book_id = request.data.get("offered_book_id")
        message = request.data.get("message", "")
        exchange_type = request.data.get("exchange_type")

        if not to_email or not requested_book_id:
            return Response({"error": "to_email and requested_book_id required"}, status=400)

        payload = {
            "from_email": from_email,
            "to_email": to_email,
            "requested_book_id": requested_book_id,
            "offered_book_id": offered_book_id,
            "message": message,
            "exchange_type": exchange_type
        }

        send_message("exchange_requests", payload)
        return Response({"status": "Exchange request sent to Kafka"}, status=202)


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