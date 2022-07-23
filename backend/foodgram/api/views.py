import pdb

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Ingredients, Tags, Recipes, Favorite
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, TagsSerializer,
                          FavoriteSerializer,
                          RecipesCreateSerializer, IngredientsAmountSerializer, RecipesSerializer)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для модели Ingredients"""
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)
    permission_classes = []
    pagination_class = None


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для модели Tags"""
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)
    permission_classes = []
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Recipes"""

    queryset = Recipes.objects.all()
    permission_classes = []
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        """Метод отвечающий за выбор selializer в зависимости от метода"""
        if self.request.method in ('POST', 'PATCH',):
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Favorite"""
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Метод отвечающий за получение множества объектов Favorite"""
        author = self.request.user
        favorite_queryset = Favorite.objects.filter(author=author)

        return favorite_queryset

    def create(self, request, *args, **kwargs):
        """Метод отвечающий за создание объектов Favorite"""
        recipes_id = self.kwargs.get("recipes_id")
        author = self.request.user
        if not Favorite.objects.filter(favorite=recipes_id, author=author).exists():
            Favorite.objects.filter(favorite=recipes_id, author=author).create()
        else:
            Favorite.objects.filter(favorite=recipes_id, author=author).delete()
