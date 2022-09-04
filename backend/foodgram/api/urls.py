from django.urls import include, path
from rest_framework import routers

from .views import (IngredientsViewSet, TagsViewSet, RecipesViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'ingredients',
    IngredientsViewSet,
    basename='ingredients',
)
router.register(
    r'tags',
    TagsViewSet,
    basename='tags'
)
router.register(
    r'recipes',
    RecipesViewSet,
    basename='recipes'
)

# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments',
# )

urlpatterns = [
    path('', include(router.urls)),
]
