from django.contrib import admin

from Book_Exchange.HLB.backend.book_exchange.apps.api.models import *

# Register your models here.

admin.register(User, Book, ExchangeRequest, ExchangeRequest, Review, Deal)

