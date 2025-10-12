import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)

        if not username:
            username = email.split("@")[0]

        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_image = models.ImageField(default='user.png', upload_to='user_images/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    book_image = models.ImageField(default='template.png', upload_to='book_images/')
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



