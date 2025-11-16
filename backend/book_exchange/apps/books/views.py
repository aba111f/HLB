import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer

from django.core.cache import cache

logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"Book created by {self.request.user.email}: {serializer.data['title']}")

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_book_by_user(self, request):

        # -----------Redis Limit request Per Minute-------------
        user_id = request.user.id
        rate_limit_key = f"user:{user_id}_books_get_book_by_user_minute"

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
        
        # --------Redis limit code end-------------


        owner = request.user
        
        books = self.queryset.filter(owner = owner)
        serializer = self.get_serializer(books, many=True)
        print(serializer.data)
        return Response(serializer.data)
    

    @action(detail=False, methods=["get"])
    def search_books(self, request):
        query = request.query_params.get("q")
        if not query:
            logger.warning("Book search failed: Missing 'q' parameter")
            return Response({"error": "Missing search query"}, status=400)

        books = Book.objects.filter(title__icontains=query)
        logger.info(f"Book search query: '{query}' -> {len(books)} results")
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)