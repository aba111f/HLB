import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import User, ExchangeRequest
from .serializers import ExchangeRequestSerializer


logger = logging.getLogger(__name__)


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
    

