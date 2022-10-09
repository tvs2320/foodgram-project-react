from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Basket, Favorite, Ingredients, Recipes, Tags
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipesFilter
from .pagination import FoodgramPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (BasketSerializer, FavoriteSerializer,
                          IngredientsSerializer, RecipesCreateSerializer,
                          RecipesSerializer, TagsSerializer)
from .services import report


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для модели Ingredients"""
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    filter_backends = [IngredientsFilter]
    search_fields = ('^name',)
    permission_classes = [AllowAny, ]
    pagination_class = None


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор представлений для модели Tags"""
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)
    permission_classes = [AllowAny, ]
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Recipes"""
    queryset = Recipes.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = FoodgramPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        """Метод отвечающий за выбор selializer в зависимости от метода"""
        if self.request.method in ('POST', 'PATCH',):
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        """Метод отвечающий за передачу данных об авторе в метод save"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', ],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Метод отвечающий за сохранение рецепта в избранное"""
        data = {'author': request.user.id, 'recipes': pk}
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Метод отвечающий за удаление рецепта из избранного"""
        author = request.user
        recipes = get_object_or_404(Recipes, id=pk)
        favorite = get_object_or_404(
            Favorite, author=author, recipes=recipes
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', ],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Метод отвечающий за сохранение рецепта в список покупок"""
        data = {'author': request.user.id, 'recipes': pk}
        serializer = BasketSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Метод отвечающий за удаление рецепта из списка покупок"""
        author = request.user
        recipes = get_object_or_404(Recipes, id=pk)
        shopping_cart = get_object_or_404(
            Basket, author=author, recipes=recipes
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(request):
        data = report(request)
        return data
