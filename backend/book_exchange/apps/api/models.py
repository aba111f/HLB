import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['city']),
        ]


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('good', 'Good'),
        ('used', 'Used'),
    ])
    availability = models.CharField(max_length=20, choices=[
        ('exchange', 'Exchange'),
        ('lend', 'Lend'),
        ('giveaway', 'Giveaway'),
    ], default='exchange')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
        ]

class ExchangeRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    offered_book = models.ForeignKey(Book, related_name="offered_in_requests", on_delete=models.CASCADE, null=True, blank=True)
    requested_book = models.ForeignKey(Book, related_name="requested_in_requests", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)  # "Можно ли взять на неделю?"
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
    rating = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
