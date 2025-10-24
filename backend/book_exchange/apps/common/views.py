import logging
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Book, ExchangeRequest
from .serializers import UserSerializer, BookSerializer, ExchangeRequestSerializer

from django.views.decorators.csrf import csrf_exempt
from django_elasticsearch_dsl.search import Search
from apps.api.documents import BookDocument

logger = logging.getLogger(__name__)


@action(detail=False, methods=['Create'], permission_classes=[AllowAny])
class CustomLoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            logger.warning("Login failed: Missing email or password")
            return Response({"error": "Email and password required"}, status=400)

        user = authenticate(email=email, password=password)
        if user is None:
            logger.warning(f"Login failed for email={email}")
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        logger.info(f"User {user.email} logged in successfully")

        return Response({
            "id": user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=200)



@csrf_exempt
@action(detail=False, methods=['post'], permission_classes=[AllowAny])
def search_books(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        availability = request.POST.get('availability')

        search = BookDocument.search()

        if title:
            search = search.query('match', title={'query': title, 'fuzziness': 'AUTO'})
        if author: 
            search = search.query('match', author={'query': author, 'fuzziness': "AUTO"})
        if genre:
            search = search.query('match', genre={'query': genre, 'fuzziness': "AUTO"})
        if availability:
            search = search.query('match', availability={'query': availability, 'fuzziness': "AUTO"})

        response = search.execute()
        
        results = [ 
            {
                'title': hit.title,
                'author': hit.author,
                'genre': hit.genre,
                'username': hit.owner_username,
                'email': hit.owner_email,
                'condition': hit.condition,
                'description': hit.description,
                'availability': hit.availability,
                'created_at': hit.created_at,
                'book_image': hit.book_image

            }
            for hit in response
        ]
        return JsonResponse({'results': results}, status=200)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


