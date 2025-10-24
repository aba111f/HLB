import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer


logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"Book created by {self.request.user.email}: {serializer.data['title']}")

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