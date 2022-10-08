# from django.contrib import admin
# from django.forms.models import BaseInlineFormSet
# from .models import (Basket, Favorite, Ingredients, IngredientsAmount, Recipes,
#                      Tags)
#
#
# class IngredientsAmountInlineFormset(BaseInlineFormSet):
#     def clean_ingredients(self):
#         # ingredients = self.cleaned_data['ingredients']
#         if len(self.cleaned_data['ingredients']) < 1:
#             return 'Укажите хотя бы один ингредиент в рецепте'
#         return self.cleaned_data['ingredients']
#
#
# class IngredientsAmountInline(admin.TabularInline):
#     model = IngredientsAmount
#     formset = IngredientsAmountInlineFormset
#     extra = 0
#
#
# @admin.register(Ingredients)
# class IngredientsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'measurement_unit',)
#     list_filter = ('name',)
#     search_fields = ('name',)
#
#
# @admin.register(IngredientsAmount)
# class IngredientsAmountAdmin(admin.ModelAdmin):
#     list_display = ('ingredients', 'recipes', 'amount')
#
#
# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ('recipes', 'author')
#
#
# @admin.register(Basket)
# class BasketAdmin(admin.ModelAdmin):
#     list_display = ('recipes', 'author')
#
#
# @admin.register(Recipes)
# class RecipesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'author', 'favorites_count',)
#     list_filter = ('name', 'author', 'tags',)
#     search_fields = ('name', 'author', 'tags',)
#     empty_value_display = '-пусто-'
#     inlines = (IngredientsAmountInline,)
#
#     def favorites_count(self, obj):
#         return obj.favorites.count()
#
#
# @admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
