from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry 

from apps.users.models import User
from apps.books.models import Book

@registry.register_document
class BookDocument(Document):
    owner_username = fields.TextField(attr='owner.username')
    owner_email = fields.TextField(attr='owner.email')
    class Index: 
        name = 'books'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Book
        fields = [
            'title', 
            'author', 
            'genre',  
            'created_at', 
            'description', 
            'book_image', 
            'condition', 
            'availability',
            
            ]