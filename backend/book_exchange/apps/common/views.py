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

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core.cache import cache

logger = logging.getLogger(__name__)

login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING),
        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
        'access': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


class CustomLoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=login_request_schema,
        responses={200: login_response_schema},
        operation_description="Custom login returning JWT tokens + user id"
    )

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

   


class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        method='post',
        operation_description="Search books in Elasticsearch",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'author': openapi.Schema(type=openapi.TYPE_STRING),
                'genre': openapi.Schema(type=openapi.TYPE_STRING),
                'availability': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                )
            }
        )}
    )
    @action(detail=False, methods=['post'])
    def search_books(self, request):

        # Redis Limit request Per Minute
        user_id = request.user.id
        rate_limit_key = f"user:{user_id}_common_search_books_minute"

        request_count = cache.get(rate_limit_key)

        MAX_REQUESTS_PER_MINUTE = 10

        if request_count is not None and int(request_count) >= MAX_REQUESTS_PER_MINUTE:
            logger.warning(f"Rate limit exceeded for user {request.user.email}")
            return Response({"error": "Too many requests for an hour"}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        if request_count is None:
            cache.set(rate_limit_key, 1, timeout=60)
        else:
            cache.incr(rate_limit_key)

        title = request.data.get('title')
        author = request.data.get('author')
        genre = request.data.get('genre')
        availability = request.data.get('availability')

        search = BookDocument.search()

        if title:
            search = search.query('match', title={'query': title, 'fuzziness': 'AUTO'})
        if author:
            search = search.query('match', author={'query': author, 'fuzziness': 'AUTO'})
        if genre:
            search = search.query('match', genre={'query': genre, 'fuzziness': 'AUTO'})
        if availability:
            search = search.query('match', availability={'query': availability, 'fuzziness': 'AUTO'})

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
                'book_image': hit.book_image,
            }
            for hit in response
        ]

        return Response({'results': results}, status=200)
