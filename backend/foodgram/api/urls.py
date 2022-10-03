from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
