from django.contrib import admin

from .models import Ingredients, Tags, Recipes


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'


admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags)

# https://question-it.com/questions/2287178/django-pokazat-kolichestvo-svjazannyh-obektov-v-adminke-list_display