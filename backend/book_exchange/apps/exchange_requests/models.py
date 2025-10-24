import uuid
from django.db import models
from users.models import User
from books.models import Book

class ExchangeRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    offered_book = models.ForeignKey(Book, related_name="offered_in_requests", on_delete=models.CASCADE, null=True, blank=True)
    requested_book = models.ForeignKey(Book, related_name="requested_in_requests", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True) 
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['from_user', 'to_user']),
        ]


class Deal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exchange_request = models.OneToOneField(ExchangeRequest, on_delete=models.CASCADE, related_name="deal")
    completed_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, related_name="reviews_written", on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name="reviews_received", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField() 
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


