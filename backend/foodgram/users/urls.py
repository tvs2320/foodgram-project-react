from django.urls import include, path
from rest_framework import routers

from .views import subscribe

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/<int:pk>/subscribe', subscribe)
]
