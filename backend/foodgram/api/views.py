import pdb

from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Ingredients, Tags, Recipes, Favorite
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, TagsSerializer,
    # FavoriteSerializer,
                          RecipesCreateSerializer, IngredientsAmountSerializer, RecipesSerializer,
                          FavoriteSerializer, FavoriteListSerializer)


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

    @action(detail=True, methods=['post', ],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        data = {'author': request.user.id, 'recipes': pk}
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        author = request.user
        recipes = get_object_or_404(Recipes, id=pk)
        favorite = get_object_or_404(
            Favorite, author=author, recipes=recipes
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
