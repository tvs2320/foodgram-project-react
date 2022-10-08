from rest_framework.pagination import PageNumberPagination

from foodgram.settings import PAGE_COUNT


class FoodgramPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_COUNT
