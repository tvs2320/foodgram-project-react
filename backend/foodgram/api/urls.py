from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
