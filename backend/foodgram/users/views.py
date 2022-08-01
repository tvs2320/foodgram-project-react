from urllib import request
import pdb
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from djoser.views import UserViewSet
from .models import CustomUser
from .permissions import IsAuthorOrReadOnly
from .serializers import CustomUserSerializer, PasswordSerializer


# class CustomUserViewSet(viewsets.ModelViewSet):
#     """Вьюсет данных пользователей.
#     Полный доступ к данным пользователей у администратора,
#     чтение/изменение данных своей учетной записи юзером"""
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = (AllowAny,)
#     pagination_class = PageNumberPagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter)
#     search_fields = ('username',)
#     ordering_fields = 'username'
#
#     @action(methods=['get', ], detail=False,
#             permission_classes=(IsAuthenticated,))
#     def me(self, request):
#         """Метод "me" отвечает за чтение пользователем
#         собственных учетных данных"""
#         me_user = self.request.user
#         serializer = self.get_serializer(me_user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#



class FollowViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Follow"""
