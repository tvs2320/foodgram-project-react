from django.urls import include, path
from rest_framework import routers

from .views import FollowApiView, FollowListAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListAPIView.as_view(),
         name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'))
]