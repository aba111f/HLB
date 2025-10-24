import uuid
from django.db import models
from apps.users.models import User

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    book_image = models.ImageField(default='book_images/template.png', upload_to='book_images/')
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
