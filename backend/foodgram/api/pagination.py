from foodgram.settings import PAGE_COUNT
from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_COUNT
