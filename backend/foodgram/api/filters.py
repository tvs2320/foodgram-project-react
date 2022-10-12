from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter

from recipes.models import Recipes


class IngredientsFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(filter.FilterSet):
    tags = filter.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filter.BooleanFilter(method='get_favorited')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipes
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__author=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(basket__author=self.request.user)
        return queryset
