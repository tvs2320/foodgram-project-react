from django.contrib import admin

from .models import (Basket, Favorite, Ingredients, IngredientsAmount, Recipes,
                     Tags)


class IngredientsAmountInline(admin.TabularInline):
    model = IngredientsAmount
    min_num = 1
    extra = 0


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(IngredientsAmount)
class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipes', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'author')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'author')


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name',
                     'author__username',
                     'tags__name',
                     )
    empty_value_display = '-пусто-'
    inlines = (IngredientsAmountInline,)
    exclude = ['ingredients']

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
