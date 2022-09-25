from django.contrib import admin

from .models import (Ingredients,
                     Tags,
                     Recipes,
                     IngredientsAmount,
                     Favorite,
                     Basket)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(IngredientsAmount)
class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipes', 'amount')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'author')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'author')
