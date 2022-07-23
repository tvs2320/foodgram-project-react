from urllib import request

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


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет данных пользователей.
    Полный доступ к данным пользователей у администратора,
    чтение/изменение данных своей учетной записи юзером"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny | IsAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    ordering_fields = 'username'

    @action(methods=['get', ], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Метод "me" отвечает за чтение пользователем
        собственных учетных данных"""
        me_user = self.request.user
        serializer = self.get_serializer(me_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False,
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        """Метод "set_password" отвечает за смену пользователем
    пароля доступа к сайту"""
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        current_password = serializer.validated_data.get('current_password')
        user = request.user
        if user.check_password(raw_password=current_password):
            user.set_password(raw_password=new_password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response('Invalid password')



class FollowViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Follow"""

# @api_view(['POST', ])
# @permission_classes((IsAuthenticated,))
# def set_password(self, request):
#     """Метод "set_password" отвечает за смену пользователем
#     пароля доступа к сайту"""
#     # me_user = self.request.user
#     serializer = PasswordSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     new_password = serializer.validated_data.get('new_password')
#     current_password = serializer.validated_data.get('current_password')
#     new_user = get_object_or_404(CustomUser,
#                                  password=new_password)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST', ])
# @permission_classes((AllowAny,))
# def login(self, request):
#     serializer = LoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     password = serializer.initial_data.get('password')
#     username = serializer.initial_data.get('username')
#     user = get_object_or_404(CustomUser,
#                              password=password, username=username)
#     token = Token.objects.create(user=user)
#     return Response({'token': str(token)}, status=status.HTTP_200_OK)

# @api_view(['POST', ])
# @permission_classes((AllowAny, ))
# def login(request):
#     """Метод "login" отвечает за получение зарегистрированным пользователем
#     токена для доступа к сайту"""
#     serializer = LoginSerializer(data=request.data)
#     password = serializer.initial_data.get('password')
#     email = serializer.initial_data.get('email')
#     user = get_object_or_404(CustomUser, password=password, email=email)
#
#     if default_token_generator.check_token(user):
#         token = AccessToken.for_user(user)
#         return Response({"token": str(token)}, status=status.HTTP_200_OK)
#     return Response({"token": "неверный token"
#                      }, status=status.HTTP_400_BAD_REQUEST)
