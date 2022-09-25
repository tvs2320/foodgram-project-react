from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework import viewsets, filters

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

from .filters import IngredientsFilter, RecipesFilter
from .models import Ingredients, Tags, Recipes, Favorite, Basket, IngredientsAmount
from .pagination import FoodgramPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, TagsSerializer,
                          RecipesCreateSerializer, RecipesSerializer,
                          FavoriteSerializer, BasketSerializer)


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

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Метод отвечающий за выгрузку файла со списком ингридиентов
        из рецептов, сохраненных в список покупок"""
        basket = IngredientsAmount.objects.filter(
            recipes__basket__author=request.user)
        ingredients_list = basket.values('ingredients__name',
                                         'ingredients__measurement_unit'
                                         ).annotate(total=Sum('amount'))
        file = ''
        shopping_cart = list()
        for ingredient in ingredients_list:
            if ingredient["ingredients__name"] not in shopping_cart:
                value = (f'{ingredient["ingredients__name"]} - '
                         f'{ingredient["total"]} '
                         f'{ingredient["ingredients__measurement_unit"]}')
                shopping_cart.append(ingredient["ingredients__name"])
                file += value + '\n'
        filename = 'shopping_cart.txt'
        response = HttpResponse(file, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
